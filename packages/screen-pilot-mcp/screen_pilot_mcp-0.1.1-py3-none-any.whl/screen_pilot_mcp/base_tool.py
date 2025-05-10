"""Base class for all ScreenPilot tools."""

from pathlib import Path
from typing import Any, Dict, List, Optional
from mcp.server.fastmcp import FastMCP, Image
from abc import ABC
import time


class BaseTool(ABC):
    """
    Abstract base class for all screen interaction tools.
    Provides common functionality and defines the interface that all tools must implement.
    """
    
    def __init__(self, mcp: FastMCP, screens_dir: Path):
        """Initialize the base tool.
        
        Args:
            mcp: The MCP server instance
            screens_dir: Directory to save screenshots
        """
        self.mcp = mcp
        self.screens_dir = screens_dir
        self.name = self.__class__.__name__.lower()
        self.description = "Base screen automation tool"
        self.schema = {
            "type": "object",
            "properties": {},
            "required": []
        }
    
    def register(self) -> None:
        """Register this tool with the MCP server."""
        @self.mcp.tool(name=self.name, 
                      description=self.description,
                      input_schema=self.schema)
        async def tool_handler(arguments: Dict[str, Any]) -> List[Any]:
            """Handle tool calls by delegating to the tool's execute method."""
            return await self.execute(arguments)
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Any]:
        """Execute the tool functionality.
        
        Args:
            arguments: The arguments passed to the tool
            
        Returns:
            A list of content items (text, images, etc.)
        """
        raise NotImplementedError("Subclasses must implement execute method")
    
    @staticmethod
    def add_delay(seconds: float = 0.5):
        time.sleep(seconds)
    
    def save_screenshot(self, screenshot, prefix: str, format: str = "PNG", 
                        extra_info: Optional[str] = None) -> Image:
        """
        Save a screenshot to file and return it as an Image object.
        
        Args:
            screenshot: PIL Image object
            prefix: Prefix for the filename
            format: Format of the screenshot ("PNG" or "JPEG")
            extra_info: Additional information to include in the filename
        
        Returns:
            Image object
        """
        from screen_pilot_mcp.utils import save_screenshot_to_file
        return save_screenshot_to_file(
            screenshot, 
            self.screens_dir, 
            prefix, 
            format, 
            extra_info
        )
    
    def format_result(self, status: str, screenshot=None) -> Dict[str, Any]:
        result = {"status": status}
        if screenshot:
            result["screenshot"] = screenshot
        return result
    
    def handle_exception(self, e: Exception, operation: str) -> Dict[str, str]:
        error_msg = f"Error performing {operation}: {str(e)}"
        return {"error": error_msg} 