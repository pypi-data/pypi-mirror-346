"""Screen capture tool for ScreenPilot MCP."""

from typing import Any, Dict, List
import pyautogui
from PIL import Image as PILImage
from mcp.server.fastmcp import Text, Image

from screen_pilot_mcp.base_tool import BaseTool
from screen_pilot_mcp.utils import save_screenshot_to_file, scale_coordinates
from screen_pilot_mcp.config import TARGET_WIDTH, TARGET_HEIGHT


class ScreenCapture(BaseTool):
    """
    Provides functionality for capturing the screen.
    """
    
    def __init__(self, mcp, screens_dir):
        """Initialize screen capture tool."""
        super().__init__(mcp, screens_dir)
        self.name = "screen_capture"
        self.description = "Capture and save screenshots of the screen"
    
    def register(self):
        """Register screen capture tools with the MCP server."""
        @self.mcp.tool(name="see_screen",
                      description="Takes a screenshot of the current screen")
        async def see_screen(format: str = "PNG") -> Image:
            return await self.see_screen(format)
            
        @self.mcp.tool(name="get_screen_info",
                      description="Gets information about the screen resolution and mouse position")
        async def get_screen_info() -> Dict[str, Any]:
            return await self.get_screen_info()

        @self.mcp.prompt()
        def use_my_device() -> str:
            """Provides guidance on proper device interaction sequence."""
            return "Use the available tools to help with my tasks. For optimal results, always start by getting device information with get_screen_info() before taking screenshots. This ensures proper scaling and positioning. After checking screen details, take screenshots to verify each interaction. You have full access to this device to help serve me and complete the required tasks."
            
    async def see_screen(self, format: str = "PNG") -> Image:
        """
        Takes a screenshot and returns it as an Image object.
        The image will be scaled to the target resolution (1366x768).
        Request device info before using this tool.        
        Args:
            format: Format of the screenshot ("PNG" or "JPEG")
            
        Returns:
            Image object
        """
        try:
            screenshot = pyautogui.screenshot()
            return self.save_screenshot(screenshot, "screenshot", format)
            
        except Exception as e:
            raise RuntimeError(f"Screenshot failed: {str(e)}")
    
    async def get_screen_info(self) -> Dict[str, Any]:
        """
        Gets information about the screen resolution and mouse position.
        Returns values scaled to the target resolution (1366x768).
        
        Returns:
            Dictionary containing screen width, height, and current mouse position
        """
        try:
            actual_width, actual_height = pyautogui.size()
            actual_x, actual_y = pyautogui.position()
            
            # Scale mouse position to target resolution
            scaled_x, scaled_y = scale_coordinates(actual_x, actual_y)
            
            return {
                "width": TARGET_WIDTH,
                "height": TARGET_HEIGHT,
                "current_mouse_position": [scaled_x, scaled_y],
                "actual_mouse_position": [actual_x, actual_y]
            }
        except Exception as e:
            return self.handle_exception(e, "get screen info")

    async def execute(self, arguments: Dict[str, Any]) -> List[Any]:
        """Capture screenshot.
        
        Args:
            arguments: Tool arguments
                - region: Optional region to capture
                - format: Image format (PNG or JPEG)
                
        Returns:
            List containing screenshot image and text description
        """
        region = arguments.get("region")
        format = arguments.get("format", "PNG")
        
        if region:
            screenshot = pyautogui.screenshot(
                region=(
                    region["left"], 
                    region["top"], 
                    region["width"], 
                    region["height"]
                )
            )
            description = f"Screenshot of region ({region['left']},{region['top']},{region['width']},{region['height']})"
        else:
            screenshot = pyautogui.screenshot()
            description = "Full screen screenshot"
        
        # Save screenshot and return as MCP Image
        image = save_screenshot_to_file(
            screenshot, 
            self.screens_dir, 
            prefix="screen",
            format=format
        )
        
        return [
            image,
            Text(text=description)
        ] 