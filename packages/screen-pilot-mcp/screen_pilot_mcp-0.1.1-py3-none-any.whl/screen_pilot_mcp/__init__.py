"""ScreenPilot MCP server package."""

__version__ = "0.1.1"

from .server import main, ScreenPilot
from .base_tool import BaseTool
from .screen_capture import ScreenCapture
from .mouse import Mouse
from .keyboard import Keyboard
from .scroll import Scroll
from .element import Element
from .action_sequence import ActionSequence

__all__ = [
    "main",
    "ScreenPilot",
    "BaseTool",
    "ScreenCapture",
    "Mouse",
    "Keyboard",
    "Scroll",
    "Element",
    "ActionSequence",
] 