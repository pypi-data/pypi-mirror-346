import pyautogui
from typing import Dict, Any, List
from .base_tool import BaseTool
from mcp.server.fastmcp import Image, Text


class Keyboard(BaseTool):
    """
    Provides functionality for keyboard actions.
    """
    
    def __init__(self, mcp, screens_dir):
        """Initialize keyboard tool."""
        super().__init__(mcp, screens_dir)
        self.name = "keyboard"
        self.description = "Perform keyboard actions like typing and pressing keys"
    
    def register(self):
        """Register keyboard tools with the MCP server."""
        @self.mcp.tool(name="keyboard_action",
                     description="Performs a keyboard action (type, press, or hotkey)")
        async def keyboard_action(action_type: str, value: str, 
                                take_screenshot: bool = True, format: str = "PNG") -> Dict[str, Any]:
            return await self.keyboard_action(action_type, value, take_screenshot, format)
    
    async def keyboard_action(self, action_type: str, value: str, 
                             take_screenshot: bool = True, format: str = "PNG") -> Dict[str, Any]:
        """
        Performs a keyboard action and optionally takes a screenshot.
        
        Args:
            action_type: Type of action ("type" for text input, "press" for key press, or "hotkey" for combinations)
            value: Text to type or key to press (for hotkey, use format like "ctrl+t")
            take_screenshot: Whether to take a screenshot after the action (default: True)
            format: Format of the screenshot ("PNG" or "JPEG")
        
        Returns:
            Dictionary with status message and screenshot if requested
        """
        try:
            status = ""
            action_type = action_type.lower()
            
            if action_type == "type":
                pyautogui.write(value)
                status = f"Successfully typed: {value}"
            elif action_type == "press":
                pyautogui.press(value)
                status = f"Successfully pressed key: {value}"
            elif action_type == "hotkey":
                # Split the value by '+' to get individual keys
                keys = [k.strip() for k in value.split('+')]
                pyautogui.hotkey(*keys)
                status = f"Successfully pressed hotkey combination: {value}"
            else:
                return {"error": f"Unknown action type: {action_type}. Use 'type', 'press', or 'hotkey'."}
            
            self.add_delay()

            if take_screenshot:
                screenshot = pyautogui.screenshot()
                screenshot_obj = self.save_screenshot(
                    screenshot, 
                    f"keyboard_{action_type}", 
                    format
                )
                return self.format_result(status, screenshot_obj)
            
            return self.format_result(status)
            
        except Exception as e:
            return self.handle_exception(e, "keyboard action")
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Any]:
        """Execute keyboard tools based on arguments."""
        action_type = arguments.get("action_type")
        value = arguments.get("value")
        take_screenshot = arguments.get("take_screenshot", True)
        format = arguments.get("format", "PNG")
        
        result = await self.keyboard_action(action_type, value, take_screenshot, format)
        
        response = [Text(text=result["status"] if "status" in result else result.get("error", "Unknown error"))]
        if "screenshot" in result:
            response.append(result["screenshot"])
            
        return response 