"""Utility functions for ScreenPilot MCP."""

import io
import datetime
import os
import time
import uuid
from pathlib import Path
from typing import Optional, Tuple, Union
from mcp.server.fastmcp import Image, Text
from PIL import Image as PILImage
import pyautogui
from screen_pilot_mcp.config import TARGET_WIDTH, TARGET_HEIGHT


def ensure_directory_exists(directory: Path) -> None:
    """Create directory if it doesn't exist.
    
    Args:
        directory: Path to create
    """
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)


def get_scaling_ratio():
    """Get ratio between target and actual screen resolution."""
    actual_width, actual_height = pyautogui.size()
    x_ratio = TARGET_WIDTH / actual_width
    y_ratio = TARGET_HEIGHT / actual_height
    return (x_ratio, y_ratio)


def scale_image(image, target_width=TARGET_WIDTH, target_height=TARGET_HEIGHT):
    """Scale image to target resolution."""
    return image.resize((target_width, target_height), PILImage.LANCZOS)


def scale_coordinates(x: Union[int, float], y: Union[int, float], 
                     inverse: bool = False) -> Tuple[int, int]:
    """
    Scale coordinates between actual screen resolution and target resolution.
    
    Args:
        x: X coordinate
        y: Y coordinate
        inverse: If True, convert from target to actual resolution
                If False, convert from actual to target resolution
    
    Returns:
        Tuple of scaled (x, y) coordinates
    """
    actual_width, actual_height = pyautogui.size()
    
    if inverse:
        # Convert from target to actual resolution
        scaled_x = int(x * (actual_width / TARGET_WIDTH))
        scaled_y = int(y * (actual_height / TARGET_HEIGHT))
    else:
        # Convert from actual to target resolution
        scaled_x = int(x * (TARGET_WIDTH / actual_width))
        scaled_y = int(y * (TARGET_HEIGHT / actual_height))
    
    return scaled_x, scaled_y


def save_screenshot_to_file(
    screenshot: PILImage.Image,
    screens_dir: Path,
    prefix: str = "screenshot",
    format: str = "PNG",
    extra_info: Optional[str] = None
) -> Image:
    """Save a screenshot to file and return it as an MCP Image.
    
    Args:
        screenshot: PIL Image object
        screens_dir: Directory to save screenshots
        prefix: Prefix for the filename
        format: Format of the screenshot ("PNG" or "JPEG")
        extra_info: Additional information to include in the filename
        
    Returns:
        MCP Image object
    """
    # Create screens directory if it doesn't exist
    ensure_directory_exists(screens_dir)
    
    # Generate unique filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    
    if extra_info:
        filename = f"{prefix}_{timestamp}_{extra_info}_{unique_id}.{format.lower()}"
    else:
        filename = f"{prefix}_{timestamp}_{unique_id}.{format.lower()}"
    
    filepath = os.path.join(screens_dir, filename)
    
    # Save screenshot to file
    screenshot.save(filepath, format=format)
    
    # Create and return MCP Image object
    with open(filepath, "rb") as f:
        image_data = f.read()
    
    return Image(
        data=image_data,
        mediaType=f"image/{format.lower()}"
    ) 