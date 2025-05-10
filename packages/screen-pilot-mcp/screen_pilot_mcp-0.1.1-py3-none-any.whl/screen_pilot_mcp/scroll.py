import pyautogui
import time
from typing import Dict, Any, List
from .base_tool import BaseTool
from mcp.server.fastmcp import Image, Text


class Scroll(BaseTool):
    """
    Provides functionality for scrolling.
    """
    
    def __init__(self, mcp, screens_dir):
        """Initialize scroll tool."""
        super().__init__(mcp, screens_dir)
        self.name = "scroll"
        self.description = "Perform scrolling actions on the screen"
    
    def register(self):
        """Register scroll tools with the MCP server."""
        @self.mcp.tool(name="scroll",
                      description="Scrolls the screen in the specified direction")
        async def scroll_action(direction: str = "down", amount: int = 300, 
                             take_screenshot: bool = True, format: str = "PNG") -> Dict[str, Any]:
            return await self.scroll(direction, amount, take_screenshot, format)
            
        @self.mcp.tool(name="scroll_to_position",
                      description="Scrolls the screen to a specific position based on percentage")
        async def scroll_to_pos(percent: float = 50, 
                              take_screenshot: bool = True, format: str = "PNG") -> Dict[str, Any]:
            return await self.scroll_to_position(percent, take_screenshot, format)
    
    async def scroll(self, direction: str = "down", amount: int = 300, 
                    take_screenshot: bool = True, format: str = "PNG") -> Dict[str, Any]:
        """
        Scrolls the screen in the specified direction by the given amount.
        
        Args:
            direction: Direction to scroll ("up", "down", "left", "right", "top", "bottom")
            amount: Number of pixels to scroll (ignored for "top" and "bottom")
            take_screenshot: Whether to take a screenshot after scrolling (default: True)
            format: Format of the screenshot ("PNG" or "JPEG")
        
        Returns:
            Dictionary with status message and screenshot if requested
        """
        try:
            direction = direction.lower()
            status = ""
            
            if direction == "up":
                pyautogui.scroll(amount)
                status = f"Scrolled up by {amount} pixels"
            elif direction == "down":
                pyautogui.scroll(-amount)
                status = f"Scrolled down by {amount} pixels"
            elif direction == "left":
                pyautogui.hscroll(-amount)
                status = f"Scrolled left by {amount} pixels"
            elif direction == "right":
                pyautogui.hscroll(amount)
                status = f"Scrolled right by {amount} pixels"
            elif direction == "top":
                pyautogui.hotkey('home')
                status = "Scrolled to top of page"
            elif direction == "bottom":
                pyautogui.hotkey('end')
                status = "Scrolled to bottom of page"
            else:
                return {"error": f"Unknown scroll direction: {direction}. Use 'up', 'down', 'left', 'right', 'top', or 'bottom'."}
            
            self.add_delay()
            
            if take_screenshot:
                screenshot = pyautogui.screenshot()
                screenshot_obj = self.save_screenshot(
                    screenshot, 
                    "scroll", 
                    format, 
                    direction
                )
                return self.format_result(status, screenshot_obj)
            
            return self.format_result(status)
            
        except Exception as e:
            return self.handle_exception(e, "scroll action")
    
    async def scroll_to_position(self, percent: float = 50, 
                               take_screenshot: bool = True, format: str = "PNG") -> Dict[str, Any]:
        """
        Scrolls the screen to a specific position based on a percentage of the document length.
        
        Args:
            percent: Position to scroll to (0-100, where 0 is top and 100 is bottom)
            take_screenshot: Whether to take a screenshot after scrolling (default: True)
            format: Format of the screenshot ("PNG" or "JPEG")
        
        Returns:
            Dictionary with status message and screenshot if requested
        """
        try:
            if percent < 0 or percent > 100:
                return {"error": "Percent value must be between 0 and 100"}
                
            pyautogui.hotkey('home')
            time.sleep(0.5)
            
            if percent > 0:
                pyautogui.hotkey('end')
                time.sleep(0.5)
                
                pyautogui.hotkey('home')
                time.sleep(0.5)
                
                # This is approximate and may not work perfectly in all applications
                if percent > 0:
                    screen_height = pyautogui.size()[1]
                    estimated_doc_height = screen_height * 5
                    scroll_pixels = -int((estimated_doc_height * percent) / 100)
                    pyautogui.scroll(scroll_pixels)
            
            status = f"Scrolled to approximately {percent}% of document"
            self.add_delay(1.0)
            
            if take_screenshot:
                screenshot = pyautogui.screenshot()
                screenshot_obj = self.save_screenshot(
                    screenshot, 
                    "scroll_pos", 
                    format, 
                    str(percent)
                )
                return self.format_result(status, screenshot_obj)
            
            return self.format_result(status)
            
        except Exception as e:
            return self.handle_exception(e, "scroll to position")
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Any]:
        """Execute scroll tools based on arguments."""
        if "percent" in arguments:
            # This is a scroll_to_position call
            percent = arguments.get("percent", 50)
            take_screenshot = arguments.get("take_screenshot", True)
            format = arguments.get("format", "PNG")
            
            result = await self.scroll_to_position(percent, take_screenshot, format)
        else:
            # This is a regular scroll call
            direction = arguments.get("direction", "down")
            amount = arguments.get("amount", 300)
            take_screenshot = arguments.get("take_screenshot", True)
            format = arguments.get("format", "PNG")
            
            result = await self.scroll(direction, amount, take_screenshot, format)
        
        response = [Text(text=result["status"] if "status" in result else result.get("error", "Unknown error"))]
        if "screenshot" in result:
            response.append(result["screenshot"])
            
        return response 