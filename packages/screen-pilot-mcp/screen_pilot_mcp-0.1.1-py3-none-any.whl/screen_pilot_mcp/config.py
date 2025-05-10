"""ScreenPilot MCP server configuration."""

import os
from pathlib import Path

APP_NAME = "ScreenPilot"
SERVER_NAME = "screen-pilot"

# 获取配置目录
HOME = Path.home()
CONFIG_DIR = HOME / ".screen-pilot-mcp"
SCREENS_DIR = CONFIG_DIR / "screens"

# 屏幕和鼠标配置
DEFAULT_SCREENSHOT_FORMAT = "PNG"
DEFAULT_CLICK_DURATION = 0.5
DEFAULT_DELAY = 0.5
LONG_DELAY = 1.0
MOUSE_MOVE_DURATION = 0.3
DEFAULT_CONFIDENCE = 0.9
DEFAULT_WAIT_TIMEOUT = 10

# 标准化分辨率
TARGET_WIDTH = 1366
TARGET_HEIGHT = 768 