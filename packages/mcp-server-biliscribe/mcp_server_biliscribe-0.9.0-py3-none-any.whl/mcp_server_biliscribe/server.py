from mcp.server import FastMCP
from mcp.server.fastmcp import Context

from .process import get_video_meta, transcribe_audio
import os

app = FastMCP(
    "mcp-server-biliscribe",
    "A MCP Server that extracts and formats video content into structured text, optimized for LLM processing and analysis."
)

@app.tool()
async def bili_scribe(
    ctx: Context,
    video_url: str,
    use_audio: bool = True,    
) -> str:
    """
    Extracts and formats video content into structured text, optimized for LLM processing and analysis.
    
    Args:
        ctx (Context): The context of the request.
        video_url (str): The URL of video to process.
        use_audio (bool): Whether to use audio for transcription. Should always be True. 
    
    Returns:
        str: The formatted text content of the video.
    """

    await ctx.info("正在提取视频元数据...")
    await ctx.report_progress(0, 2)
    metadata = await get_video_meta(video_url)
    if "[Error]" in metadata:
        await ctx.error(f"提取视频元数据失败，{metadata}")
        return metadata
    await ctx.info("提取视频元数据成功！")
    await ctx.report_progress(1, 2)
    

    if use_audio:
        await ctx.info("正在转录视频音频...")
        body = await transcribe_audio(video_url)
        if "[Error]" in body:
            await ctx.error(f"转录视频音频失败，{body}")
    else:
        # 暂时不支持
        await ctx.error("仅使用字幕功能尚未实现")
        body = "[Error] 仅使用字幕功能尚未实现。"

    await ctx.info("转录视频音频成功！")
    await ctx.report_progress(2, 2)
    return f"{metadata}\n=== 内容转录 ===\n{body}"

def serve():
    """
    启动 FastMCP 服务器，如果设置了环境变量
    BILISCRIBE_SERVER_SSE，则以 sse 协议启动
    否则以 stdio 协议启动
    """

    if os.getenv("BILISCRIBE_SERVER_SSE"):
        print("Starting server with SSE protocol...")
        print("Listen to the server at: http://127.0.0.1:8000")
        app.run(transport="sse")
    else:
        app.run(transport="stdio")