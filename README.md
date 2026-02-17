# Always On Top Toggle

A lightweight Windows 11 utility that lets you **middle-click the X (close) button** of any window to toggle **Always On Top** — instead of closing it.

## Screenshots

### Normal window
![Always On Top Off](screenshots/always-on-top-off.png)

### Always On Top active (green border)
![Always On Top On](screenshots/always-on-top-on.png)

## Download & Install

### Easy install (recommended)
1. Download **[always_on_top.exe](always_on_top.exe)**
2. Double-click it — that's it!
   - Installs automatically to `C:\AlwaysOnTopToggle\`
   - Starts automatically with Windows
   - No Python required

### Manual install
1. Make sure Python 3.x is installed
2. Install dependencies:
   ```
   pip install pywin32 pynput
   ```
3. Run `always_on_top.py`
4. For autostart, place a shortcut to `start_hidden.vbs` in:
   ```
   %APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
   ```

## Features

- **Middle-click** the X button of any window to pin/unpin it
- **Green border** appears around the window when it is pinned
- **Popup notification** shows the current state (ON / OFF)
- Runs silently in the background, starts automatically with Windows

## Usage

| Action | Result |
|--------|--------|
| Middle-click on window's X button | Toggle Always On Top |

When a window is pinned, its **border turns green** and a popup appears.
Repeat the action to unpin and the border returns to normal.

## Files

| File | Description |
|------|-------------|
| `always_on_top.exe` | Standalone installer (no Python needed) |
| `always_on_top.py` | Main Python script |
| `start_hidden.vbs` | Silent launcher (no console window) |
| `restart.ps1` | Restart script |

## Requirements

- Windows 11 (Windows 10 may work but untested)
- 64-bit system

## License

MIT
