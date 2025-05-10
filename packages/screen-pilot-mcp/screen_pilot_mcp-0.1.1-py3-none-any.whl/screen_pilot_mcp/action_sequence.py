import pyautogui
import time
from typing import Dict, Any, List
from .base_tool import BaseTool
from mcp.server.fastmcp import Image, Text


class ActionSequence(BaseTool):
    """
    Provides functionality for performing sequences of actions.
    """
    
    def __init__(self, mcp, screens_dir):
        """Initialize action sequence tool."""
        super().__init__(mcp, screens_dir)
        self.name = "action_sequence"
        self.description = "Perform sequences of mouse and keyboard actions"
    
    def register(self):
        """Register action sequence tools with the MCP server."""
        @self.mcp.tool(name="perform_actions",
                      description="Performs a sequence of mouse and keyboard actions")
        async def perform_actions_tool(actions: List[Dict[str, Any]], take_screenshots: bool = True, 
                                    format: str = "PNG") -> Dict[str, Any]:
            return await self.perform_actions(actions, take_screenshots, format)
    
    async def perform_actions(self, actions: List[Dict[str, Any]], take_screenshots: bool = True, 
                             format: str = "PNG") -> Dict[str, Any]:
        """
        Performs a sequence of mouse and keyboard actions.
        
        Args:
            actions: List of action dictionaries, each containing:
                    - 'type': 'mouse_click', 'keyboard', or 'scroll'
                    - For mouse_click: 'x', 'y', 'button' (optional), 'clicks' (optional)
                    - For keyboard: 'action_type' ('type', 'press', or 'hotkey'), 'value'
                    - For scroll: 'direction', 'amount' (optional)
            take_screenshots: Whether to take screenshots after each action (default: True)
            format: Format of the screenshots ("PNG" or "JPEG")
        
        Returns:
            Dictionary with results of each action and final screenshot
        """
        try:
            results = []
            
            for i, action in enumerate(actions):
                
                action_type = action.get("type", "")
                
                if action_type == "mouse_click":
                    result = await self._handle_mouse_click(action)
                    results.append(result)
                
                elif action_type == "keyboard":
                    result = await self._handle_keyboard_action(action)
                    results.append(result)
                
                elif action_type == "scroll":
                    result = await self._handle_scroll_action(action)
                    results.append(result)
                
                else:
                    results.append({
                        "action": action_type,
                        "status": "error",
                        "message": f"Unknown action type: {action_type}"
                    })
                    continue
                
                self.add_delay(0.5)
            
            response = {"results": results}
            
            if take_screenshots:
                self.add_delay(0.5)
                screenshot = pyautogui.screenshot()
                screenshot_obj = self.save_screenshot(
                    screenshot, 
                    "actions_sequence", 
                    format
                )
                response["screenshot"] = screenshot_obj
            
            return response
            
        except Exception as e:
            return self.handle_exception(e, "actions sequence")
    
    async def _handle_mouse_click(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle a mouse click action.
        
        Args:
            action: Dictionary containing action parameters
        
        Returns:
            Dictionary with action result
        """
        x = action["x"]
        y = action["y"]
        button = action.get("button", "left")
        clicks = action.get("clicks", 1)
        
        # Move mouse and click
        pyautogui.moveTo(x, y, duration=0.3)
        pyautogui.click(x=x, y=y, button=button, clicks=clicks)
        
        return {
            "action": "mouse_click",
            "position": {"x": x, "y": y},
            "button": button,
            "clicks": clicks,
            "status": "success"
        }
    
    async def _handle_keyboard_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle a keyboard action.
        
        Args:
            action: Dictionary containing action parameters
        
        Returns:
            Dictionary with action result
        """
        action_type = action["action_type"]
        value = action["value"]
        
        if action_type.lower() == "type":
            pyautogui.write(value)
        elif action_type.lower() == "press":
            pyautogui.press(value)
        elif action_type.lower() == "hotkey":
            keys = [k.strip() for k in value.split('+')]
            pyautogui.hotkey(*keys)
        else:
            return {
                "action": "keyboard",
                "action_type": action_type,
                "value": value,
                "status": "error",
                "message": f"Unknown action type: {action_type}"
            }
        
        return {
            "action": "keyboard",
            "action_type": action_type,
            "value": value,
            "status": "success"
        }
    
    async def _handle_scroll_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle a scroll action.
        
        Args:
            action: Dictionary containing action parameters
        
        Returns:
            Dictionary with action result
        """
        direction = action.get("direction", "down")
        amount = action.get("amount", 300)
        
        if direction.lower() in ["up", "down"]:
            scroll_amount = amount if direction.lower() == "up" else -amount
            pyautogui.scroll(scroll_amount)
        elif direction.lower() in ["left", "right"]:
            scroll_amount = -amount if direction.lower() == "left" else amount
            pyautogui.hscroll(scroll_amount)
        elif direction.lower() == "top":
            pyautogui.hotkey('home')
        elif direction.lower() == "bottom":
            pyautogui.hotkey('end')
        else:
            return {
                "action": "scroll",
                "direction": direction,
                "amount": amount,
                "status": "error",
                "message": f"Unknown scroll direction: {direction}"
            }
        
        return {
            "action": "scroll",
            "direction": direction,
            "amount": amount,
            "status": "success"
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Any]:
        """Execute action sequence tools based on arguments."""
        actions = arguments.get("actions", [])
        take_screenshots = arguments.get("take_screenshots", True)
        format = arguments.get("format", "PNG")
        
        result = await self.perform_actions(actions, take_screenshots, format)
        
        # Create response with text summary and optional screenshot
        response_items = []
        
        # Add summary text
        summary = "Action sequence completed with results:\n"
        for action_result in result.get("results", []):
            status = action_result.get("status", "unknown")
            action_type = action_result.get("action", "unknown")
            
            if status == "success":
                if action_type == "mouse_click":
                    position = action_result.get("position", {})
                    button = action_result.get("button", "left")
                    clicks = action_result.get("clicks", 1)
                    summary += f"- Clicked {button} button {clicks} time(s) at ({position.get('x', '?')}, {position.get('y', '?')})\n"
                elif action_type == "keyboard":
                    action_subtype = action_result.get("action_type", "unknown")
                    value = action_result.get("value", "")
                    summary += f"- Keyboard {action_subtype}: {value}\n"
                elif action_type == "scroll":
                    direction = action_result.get("direction", "unknown")
                    amount = action_result.get("amount", 0)
                    summary += f"- Scrolled {direction} by {amount} pixels\n"
                else:
                    summary += f"- {action_type}: success\n"
            else:
                message = action_result.get("message", "Unknown error")
                summary += f"- {action_type}: ERROR - {message}\n"
        
        response_items.append(Text(text=summary))
        
        # Add screenshot if available
        if "screenshot" in result:
            response_items.append(result["screenshot"])
        
        return response_items 