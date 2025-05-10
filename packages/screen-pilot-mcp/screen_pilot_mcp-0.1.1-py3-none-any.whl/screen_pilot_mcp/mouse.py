import pyautogui
from typing import Dict, Any, List
from .base_tool import BaseTool
from .utils import scale_coordinates
from mcp.server.fastmcp import Image, Text

class Mouse(BaseTool):
    """
    Provides functionality for mouse actions.
    """
    
    def __init__(self, mcp, screens_dir):
        """Initialize mouse tool."""
        super().__init__(mcp, screens_dir)
        self.name = "mouse"
        self.description = "Perform mouse actions like clicking and moving"
    
    def register(self):
        """Register mouse tools with the MCP server."""
        @self.mcp.tool(name="mouse_click",
                     description="Moves the mouse to the specified coordinates and performs a click")
        async def mouse_click(x: int, y: int, button: str = "left", clicks: int = 1, 
                            take_screenshot: bool = True, format: str = "PNG") -> Dict[str, Any]:
            return await self.mouse_click(x, y, button, clicks, take_screenshot, format)
    
    async def mouse_click(self, x: int, y: int, button: str = "left", clicks: int = 1, 
                          take_screenshot: bool = True, format: str = "PNG") -> Dict[str, Any]:
        """
        Moves the mouse to the specified coordinates, performs a click, and optionally takes a screenshot.
        
        Args:
            x: X-coordinate on screen
            y: Y-coordinate on screen
            button: Mouse button to click ("left", "right", or "middle")
            clicks: Number of clicks to perform (default: 1)
            take_screenshot: Whether to take a screenshot after the action (default: True)
            format: Format of the screenshot ("PNG" or "JPEG")
        
        Returns:
            Dictionary with status message and screenshot if requested
        """
        try:
            x, y = scale_coordinates(x, y, True)
            pyautogui.moveTo(x, y, duration=0.5)
            pyautogui.click(x=x, y=y, button=button, clicks=clicks)
            
            self.add_delay()
            
            status = f"Successfully clicked at position ({x}, {y}) with {button} button {clicks} time(s)"
            
            if take_screenshot:
                screenshot = pyautogui.screenshot()
                screenshot_obj = self.save_screenshot(
                    screenshot, 
                    "click", 
                    format, 
                    f"{x}_{y}"
                )
                return self.format_result(status, screenshot_obj)
            
            return self.format_result(status)
            
        except Exception as e:
            return self.handle_exception(e, "mouse click")
            
    async def execute(self, arguments: Dict[str, Any]) -> List[Any]:
        """Execute mouse tools based on arguments."""
        x = arguments.get("x")
        y = arguments.get("y")
        button = arguments.get("button", "left")
        clicks = arguments.get("clicks", 1)
        take_screenshot = arguments.get("take_screenshot", True)
        format = arguments.get("format", "PNG")
        
        result = await self.mouse_click(x, y, button, clicks, take_screenshot, format)
        
        response = [Text(text=result["status"])]
        if "screenshot" in result:
            response.append(result["screenshot"])
            
        return response 