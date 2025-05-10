# Screen Pilot MCP

A Model Context Protocol server that provides screen automation capabilities. This server enables LLMs to control and interact with the screen, keyboard, and mouse, allowing AI to navigate and manipulate graphical user interfaces.

The server provides a consistent interface regardless of the actual screen resolution, with coordinates automatically scaled between the target resolution (1366x768) and the actual screen size.

## Available Tools

- **screen_capture** - Captures screenshots and provides screen information
  - `see_screen(format: str = "PNG")`: Takes a screenshot of the current screen
  - `get_screen_info()`: Returns screen resolution and current mouse position

- **mouse** - Controls mouse actions
  - `mouse_click(x: int, y: int, button: str = "left", clicks: int = 1, take_screenshot: bool = True, format: str = "PNG")`: Moves the mouse to specified coordinates and performs a click

- **keyboard** - Controls keyboard inputs
  - `keyboard_action(action_type: str, value: str, take_screenshot: bool = True, format: str = "PNG")`: Performs keyboard actions (type, press, hotkey)

- **scroll** - Controls screen scrolling
  - `scroll(direction: str = "down", amount: int = 300, take_screenshot: bool = True, format: str = "PNG")`: Scrolls the screen in specified direction
  - `scroll_to_position(percent: float = 50, take_screenshot: bool = True, format: str = "PNG")`: Scrolls to an approximate position in document

- **element** - Detects and waits for screen elements
  - `element_exists(image_path: str, confidence: float = 0.9)`: Checks if an element exists on screen
  - `wait_for_element(image_path: str, max_wait_seconds: int = 10, confidence: float = 0.9)`: Waits for an element to appear

- **action_sequence** - Performs sequences of actions
  - `perform_actions(actions: List[Dict], take_screenshots: bool = True, format: str = "PNG")`: Executes a sequence of mouse and keyboard actions

## Prompts

- **use_my_device**
  - Provides guidance on proper device interaction sequence

## Installation

### Using uv (recommended)

```bash
uvx screen-pilot-mcp
```

### Using PIP

```bash
pip install screen-pilot-mcp
```

After installation, you can run it as a script using:

```bash
python -m screen_pilot_mcp
```

## Configuration

### Configure for Claude Desktop

Add to your Claude Desktop config file `claude_desktop_config.json`:

#### Using uvx

```json
{
  "mcpServers": {
    "screen-pilot": {
      "command": "uvx",
      "args": ["run", "screen-pilot-mcp"]
    }
  }
}
```

#### Using pip installation

```json
{
  "mcpServers": {
    "screen-pilot": {
      "command": "python",
      "args": ["-m", "screen_pilot_mcp"]
    }
  }
}
```

## Example Prompts

```
Use the screen capture tool to take a screenshot of the current screen. Then analyze what's visible, and help me click the login button on the page.
```

```
Take a screenshot, find the search box, type "weather forecast", and press Enter.
```

## Notes

- Requires Python 3.10 or higher
- First run may request screen access permissions
- Do not run multiple instances simultaneously

## Contributing

We encourage contributions to help expand and improve screen-pilot-mcp. Whether you want to add new tools, enhance existing functionality, or improve documentation, your input is valuable.

For examples of other MCP servers and implementation patterns, see: https://github.com/modelcontextprotocol/servers

Pull requests are welcome! Feel free to contribute new ideas, bug fixes, or enhancements to make screen-pilot-mcp even more powerful and useful.

## License

screen-pilot-mcp is licensed under the MIT License. This means you are free to use, modify, and distribute the software, subject to the terms and conditions of the MIT License. For more details, please see the LICENSE file in the project repository. 