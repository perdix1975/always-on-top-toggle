# Always On Top Toggle

A lightweight Windows 11 utility that lets you **middle-click the X (close) button** of any window to toggle **Always On Top** — instead of closing it.

## Screenshots

### Normal window
![Always On Top Off](screenshots/always-on-top-off.png)

### Always On Top active (green border)
![Always On Top On](screenshots/always-on-top-on.png)

## Features

- **Middle-click** the X button of any window to pin/unpin it
- **Green border** appears around the window when it is pinned
- **Popup notification** shows the current state (ON / OFF)
- **Keyboard shortcut** `Ctrl+Alt+T` toggles the active window
- Runs silently in the background, starts automatically with Windows

## Requirements

- Windows 11
- Python 3.x

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```
   pip install pywin32 pynput
   ```
3. Run at startup by placing a shortcut to `start_hidden.vbs` in:
   ```
   %APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
   ```

## Usage

| Action | Result |
|--------|--------|
| Middle-click on window's X button | Toggle Always On Top |
| `Ctrl+Alt+T` | Toggle active window |

When a window is pinned, its **border turns green** and a popup appears.
Repeat the action to unpin and the border returns to normal.

## Files

| File | Description |
|------|-------------|
| `always_on_top.py` | Main program |
| `start_hidden.vbs` | Silent launcher (no console window) |
| `restart.ps1` | Restart script |

## License

MIT
