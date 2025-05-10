import pyautogui
import time
from typing import Dict, Any, List
from .base_tool import BaseTool
from mcp.server.fastmcp import Image, Text


class Element(BaseTool):
    """
    Provides functionality for detecting and waiting for elements on screen.
    """
    
    def __init__(self, mcp, screens_dir):
        """Initialize element tool."""
        super().__init__(mcp, screens_dir)
        self.name = "element"
        self.description = "Detect and wait for elements on screen"
    
    def register(self):
        """Register element tools with the MCP server."""
        @self.mcp.tool(name="element_exists",
                      description="Checks if a specific element exists on screen")
        async def element_exists_tool(image_path: str, confidence: float = 0.9) -> Dict[str, Any]:
            return await self.element_exists(image_path, confidence)
            
        @self.mcp.tool(name="wait_for_element",
                      description="Waits for a specific element to appear on screen")
        async def wait_for_element_tool(image_path: str, max_wait_seconds: int = 10, 
                                     confidence: float = 0.9) -> Dict[str, Any]:
            return await self.wait_for_element(image_path, max_wait_seconds, confidence)
    
    async def element_exists(self, image_path: str, confidence: float = 0.9) -> Dict[str, Any]:
        """
        Checks if a specific element exists on screen by comparing with an image.
        
        Args:
            image_path: Path to the image file to search for
            confidence: Confidence level for the match (0.0 to 1.0)
        
        Returns:
            Dictionary with existence status and location if found
        """
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location:
                return {
                    "exists": True,
                    "location": {
                        "left": location.left,
                        "top": location.top,
                        "width": location.width,
                        "height": location.height
                    }
                }
            else:
                return {"exists": False}
        except Exception as e:
            return self.handle_exception(e, "element detection")
    
    async def wait_for_element(self, image_path: str, max_wait_seconds: int = 10, 
                              confidence: float = 0.9) -> Dict[str, Any]:
        """
        Waits for a specific element to appear on screen by comparing with an image.
        
        Args:
            image_path: Path to the image file to search for
            max_wait_seconds: Maximum time to wait in seconds
            confidence: Confidence level for the match (0.0 to 1.0)
        
        Returns:
            Dictionary with success status and location if found
        """
        try:
            start_time = time.time()
            while time.time() - start_time < max_wait_seconds:
                location = pyautogui.locateOnScreen(image_path, confidence=confidence)
                if location:
                    return {
                        "success": True,
                        "time_taken": time.time() - start_time,
                        "location": {
                            "left": location.left,
                            "top": location.top,
                            "width": location.width,
                            "height": location.height
                        }
                    }
                time.sleep(0.5)
            
            return {
                "success": False,
                "message": f"Element not found within {max_wait_seconds} seconds"
            }
        except Exception as e:
            return self.handle_exception(e, "waiting for element")
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Any]:
        """Execute element tools based on arguments."""
        if "max_wait_seconds" in arguments:
            # This is a wait_for_element call
            image_path = arguments.get("image_path")
            max_wait_seconds = arguments.get("max_wait_seconds", 10)
            confidence = arguments.get("confidence", 0.9)
            
            result = await self.wait_for_element(image_path, max_wait_seconds, confidence)
        else:
            # This is an element_exists call
            image_path = arguments.get("image_path")
            confidence = arguments.get("confidence", 0.9)
            
            result = await self.element_exists(image_path, confidence)
        
        if "exists" in result:
            if result["exists"]:
                message = f"Element found at location: {result['location']}"
            else:
                message = "Element not found on screen"
        elif "success" in result:
            if result["success"]:
                message = f"Element appeared after {result['time_taken']:.2f} seconds at location: {result['location']}"
            else:
                message = result["message"]
        else:
            message = "Unknown result from element tool"
            
        return [Text(text=message)] 