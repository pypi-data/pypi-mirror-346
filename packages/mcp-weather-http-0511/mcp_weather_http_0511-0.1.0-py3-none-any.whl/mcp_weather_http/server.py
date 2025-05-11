# 导入必要的库和模块
import contextlib
import logging
import os
from collections.abc import AsyncIterator

import anyio
import click  # 用于创建命令行界面
import httpx  # 异步HTTP客户端
import mcp.types as types  # MCP类型定义
from mcp.server.lowlevel import Server  # MCP服务器基础类
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager  # 流式HTTP会话管理
from starlette.applications import Starlette  # ASGI框架
from starlette.routing import Mount  # ASGI路由
from starlette.types import Receive, Scope, Send  # ASGI类型

# ---------------------------------------------------------------------------
# 天气相关辅助函数
# ---------------------------------------------------------------------------
OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"  # OpenWeather API地址
DEFAULT_UNITS = "metric"  # 默认使用摄氏温度
DEFAULT_LANG = "zh_cn"  # 默认使用中文描述


async def fetch_weather(city: str, api_key: str) -> dict[str, str]:
    """调用OpenWeather API并返回简化后的天气数据字典
    
    参数:
        city: 城市名称
        api_key: OpenWeather API密钥
        
    返回:
        包含简化天气数据的字典
        
    异常:
        httpx.HTTPStatusError: 如果响应状态码不是2xx
    """
    params = {
        "q": city,
        "appid": api_key,
        "units": DEFAULT_UNITS,  # 使用摄氏温度
        "lang": DEFAULT_LANG,   # 使用中文描述
    }
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(OPENWEATHER_URL, params=params)
        r.raise_for_status()  # 检查HTTP状态码
        data = r.json()  # 解析JSON响应
    
    # 提取关键天气信息
    weather_main = data["weather"][0]["main"]  # 主要天气状况
    description = data["weather"][0]["description"]  # 详细描述
    temp = data["main"]["temp"]  # 温度
    feels_like = data["main"]["feels_like"]  # 体感温度
    humidity = data["main"]["humidity"]  # 湿度
    
    return {
        "city": city,
        "weather": weather_main,
        "description": description,
        "temp": f"{temp}°C",
        "feels_like": f"{feels_like}°C",
        "humidity": f"{humidity}%",
    }


@click.command()  # 定义命令行接口
@click.option("--port", default=3000, help="HTTP服务监听端口")
@click.option(
    "--api-key",
    envvar="OPENWEATHER_API_KEY",  # 可以从环境变量读取
    required=True,
    help="OpenWeather API密钥(或设置OPENWEATHER_API_KEY环境变量)",
)
@click.option(
    "--log-level",
    default="INFO",
    help="日志级别(DEBUG, INFO, WARNING, ERROR, CRITICAL)",
)
@click.option(
    "--json-response",
    is_flag=True,
    default=False,
    help="启用JSON响应而不是SSE流",
)
def main(port: int, api_key: str, log_level: str, json_response: bool) -> int:
    """运行使用流式HTTP传输的MCP天气服务器"""
    
    # ---------------------- 配置日志 ----------------------
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),  # 设置日志级别
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger("weather-server")  # 创建日志记录器

    # ---------------------- 创建MCP服务器 ----------------------
    app = Server("mcp-streamable-http-weather")  # 初始化MCP服务器

    # ---------------------- 工具实现 -------------------
    @app.call_tool()  # 注册工具调用处理器
    async def handle_get_weather(name: str, arguments: dict) -> list[types.TextContent]:
        """处理'get-weather'工具调用"""
        ctx = app.request_context  # 获取请求上下文

        # """分发处理不同的工具调用"""
        # if name == "get-weather":
        #     return await handle_get_weather(arguments)
        # elif name == "another-tool":
        #     return await handle_another_tool(arguments)
        # else:
        #     raise ValueError(f"未知工具: {name}")
      
        # 从参数中获取城市名称
        city = arguments.get("location")
        if not city:
            raise ValueError("参数中必须包含'location'")

        # 发送初始日志消息，让客户端可以早期看到流式输出
        await ctx.session.send_log_message(
            level="info",
            data=f"正在获取{city}的天气…",
            logger="weather",
            related_request_id=ctx.request_id,
        )

        try:
            # 调用OpenWeather API获取天气数据
            weather = await fetch_weather(city, api_key)
        except Exception as err:
            # 将错误信息流式传输给客户端并重新抛出
            await ctx.session.send_log_message(
                level="error",
                data=str(err),
                logger="weather",
                related_request_id=ctx.request_id,
            )
            raise

        # 发送成功通知(可选)
        await ctx.session.send_log_message(
            level="info",
            data="天气数据获取成功!",
            logger="weather",
            related_request_id=ctx.request_id,
        )

        # 组合人类可读的天气摘要作为最终返回值
        summary = (
            f"{weather['city']}：{weather['description']}，温度 {weather['temp']}，"
            f"体感 {weather['feels_like']}，湿度 {weather['humidity']}。"
        )

        return [
            types.TextContent(type="text", text=summary),  # 返回文本内容
        ]

    # ---------------------- 工具注册 -------------------------
    @app.list_tools()  # 注册工具列表
    async def list_tools() -> list[types.Tool]:
        """向LLM暴露可用工具"""
        return [
            types.Tool(
                name="get-weather",
                description="查询指定城市的实时天气（OpenWeather 数据）",
                inputSchema={
                    "type": "object",
                    "required": ["location"],
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "城市的英文名称，如 'Beijing'",
                        }
                    },
                },
            )
        ]

    # ---------------------- 会话管理器 -----------------------
    session_manager = StreamableHTTPSessionManager(
        app=app,
        event_store=None,  # 无状态服务，不保存历史事件
        json_response=json_response,  # 是否使用JSON响应
        stateless=True,  # 无状态模式
    )

    async def handle_streamable_http(scope: Scope, receive: Receive, send: Send) -> None:
        """处理流式HTTP请求的ASGI接口"""
        await session_manager.handle_request(scope, receive, send)

    # ---------------------- 生命周期管理 --------------------
    @contextlib.asynccontextmanager
    async def lifespan(app: Starlette) -> AsyncIterator[None]:
        """管理ASGI应用的生命周期"""
        async with session_manager.run():  # 启动会话管理器
            logger.info("天气MCP服务器已启动! 🚀")
            try:
                yield
            finally:
                logger.info("天气MCP服务器正在关闭…")

    # ---------------------- ASGI应用 + Uvicorn ---------------------
    starlette_app = Starlette(
        debug=False,
        routes=[Mount("/mcp", app=handle_streamable_http)],  # 挂载路由
        lifespan=lifespan,  # 设置生命周期管理器
    )

    import uvicorn

    # 启动Uvicorn服务器
    uvicorn.run(starlette_app, host="0.0.0.0", port=port)

    return 0


if __name__ == "__main__":
    main()  # 主程序入口