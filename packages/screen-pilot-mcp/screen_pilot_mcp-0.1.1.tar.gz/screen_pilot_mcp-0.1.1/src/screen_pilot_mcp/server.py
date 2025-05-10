"""ScreenPilot MCP server implementation."""

import asyncio
import sys
import logging
from pathlib import Path
from typing import Any, Dict, List

from mcp.server.fastmcp import FastMCP, Text
import pyautogui

from screen_pilot_mcp import config
from screen_pilot_mcp.utils import ensure_directory_exists
from screen_pilot_mcp.screen_capture import ScreenCapture
from screen_pilot_mcp.base_tool import BaseTool
from screen_pilot_mcp.mouse import Mouse
from screen_pilot_mcp.keyboard import Keyboard
from screen_pilot_mcp.scroll import Scroll
from screen_pilot_mcp.element import Element
from screen_pilot_mcp.action_sequence import ActionSequence


class ScreenPilot:
    """ScreenPilot MCP server class."""
    
    def __init__(self):
        """Initialize ScreenPilot server."""
        # 确保目录存在
        ensure_directory_exists(config.CONFIG_DIR)
        ensure_directory_exists(config.SCREENS_DIR)
        
        # 初始化MCP服务器
        self.mcp = FastMCP(config.SERVER_NAME)
        
        # 注册工具
        self.tools = [
            ScreenCapture(self.mcp, config.SCREENS_DIR),
            Mouse(self.mcp, config.SCREENS_DIR),
            Keyboard(self.mcp, config.SCREENS_DIR),
            Scroll(self.mcp, config.SCREENS_DIR),
            Element(self.mcp, config.SCREENS_DIR),
            ActionSequence(self.mcp, config.SCREENS_DIR),
        ]
        
        for tool in self.tools:
            tool.register()
    
    def run(self, transport='stdio'):
        """Run the ScreenPilot MCP server."""
        self.mcp.run(transport=transport)


async def async_main():
    """Async entry point for the server."""
    # Import here to avoid event loop issues
    from mcp.server.stdio import stdio_server
    
    # 设置基本日志
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("screen-pilot-mcp")
    logger.info("Starting ScreenPilot MCP server...")
    
    # 初始化应用
    app = ScreenPilot()
    
    # 运行服务器
    async with stdio_server() as (read_stream, write_stream):
        await app.mcp.run_async(
            read_stream,
            write_stream,
            app.mcp.create_initialization_options()
        )


def main():
    """Main entry point for the server package."""
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        print("Server stopped by user.")
    except Exception as e:
        print(f"Error running server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 