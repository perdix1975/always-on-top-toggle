import win32gui
import win32con
import win32api
import threading
import time
import ctypes
from ctypes import wintypes
from pynput import mouse, keyboard

# -------------------------------------------------
# DWM API για αλλαγή χρώματος border
# -------------------------------------------------

dwmapi = ctypes.windll.dwmapi

# DWMWA_BORDER_COLOR = 34
DWMWA_BORDER_COLOR = 34

# Χρώματα σε BGR format (Blue-Green-Red)
COLOR_PINNED = 0x0000FF00    # Πράσινο φωσφοριζέ για pinned
COLOR_DEFAULT = 0xFFFFFFFF   # Επαναφορά στο default

def set_window_border_color(hwnd, is_pinned):
    """Αλλάζει το χρώμα του border του παραθύρου"""
    try:
        if is_pinned:
            color = COLOR_PINNED
        else:
            color = COLOR_DEFAULT
        
        color_ref = wintypes.DWORD(color)
        dwmapi.DwmSetWindowAttribute(
            wintypes.HWND(hwnd),
            wintypes.DWORD(DWMWA_BORDER_COLOR),
            ctypes.byref(color_ref),
            ctypes.sizeof(color_ref)
        )
    except Exception as e:
        pass

# -------------------------------------------------
# Βοηθητικά
# -------------------------------------------------

def get_window_under_cursor():
    x, y = win32api.GetCursorPos()
    hwnd = win32gui.WindowFromPoint((x, y))
    return win32gui.GetAncestor(hwnd, win32con.GA_ROOT)

def cursor_on_close_button(hwnd):
    try:
        rect = win32gui.GetWindowRect(hwnd)
        x, y = win32api.GetCursorPos()
        # Περιοχή του κουμπιού Χ (πάνω δεξιά γωνία)
        return (
            rect[2] - 45 <= x <= rect[2] - 5 and
            rect[1] + 5 <= y <= rect[1] + 35
        )
    except:
        return False

# -------------------------------------------------
# Popup infrastructure
# -------------------------------------------------

POPUP_CLASS = "AOT_POPUP_CLASS"
_popup_class_registered = False

def register_popup_class():
    global _popup_class_registered
    if _popup_class_registered:
        return
    wc = win32gui.WNDCLASS()
    wc.lpfnWndProc = win32gui.DefWindowProc
    wc.lpszClassName = POPUP_CLASS
    wc.hInstance = win32api.GetModuleHandle(None)
    win32gui.RegisterClass(wc)
    _popup_class_registered = True

# -------------------------------------------------
# Popup window (Βελτιωμένο για εμφάνιση κάτω από το Χ)
# -------------------------------------------------

def show_popup(text, target_hwnd):
    def _popup():
        register_popup_class()

        width = 180
        height = 40

        try:
            # Λήψη θέσης του παραθύρου στόχου
            rect = win32gui.GetWindowRect(target_hwnd)
            # rect[2] είναι η δεξιά πλευρά, rect[1] είναι η κορυφή
            # Τοποθετούμε το popup κάτω από το κουμπί Χ
            x = rect[2] - width - 10
            y = rect[1] + 40
        except:
            # Fallback αν το παράθυρο κλείσει απότομα
            screen_w = win32api.GetSystemMetrics(0)
            x, y = screen_w - width - 20, 40

        hwnd = win32gui.CreateWindowEx(
            win32con.WS_EX_TOPMOST | win32con.WS_EX_TOOLWINDOW | win32con.WS_EX_LAYERED,
            POPUP_CLASS, "",
            win32con.WS_POPUP | win32con.WS_BORDER,
            x, y, width, height,
            0, 0, win32api.GetModuleHandle(None), None
        )

        # Ημιδιαφάνεια για να μην είναι "σκληρό" στο μάτι
        win32gui.SetLayeredWindowAttributes(hwnd, 0, 220, win32con.LWA_ALPHA)

        static_hwnd = win32gui.CreateWindowEx(
            0, "STATIC", text,
            win32con.WS_CHILD | win32con.WS_VISIBLE | win32con.SS_CENTER,
            0, 0, width, height, hwnd, 0, win32api.GetModuleHandle(None), None
        )

        # Καθετοποίηση κειμένου
        hdc = win32gui.GetDC(static_hwnd)
        _, text_height = win32gui.GetTextExtentPoint32(hdc, text)
        win32gui.ReleaseDC(static_hwnd, hdc)
        y_offset = (height - text_height) // 2
        win32gui.MoveWindow(static_hwnd, 0, y_offset, width, text_height, True)

        win32gui.ShowWindow(hwnd, win32con.SW_SHOWNOACTIVATE)
        win32gui.UpdateWindow(hwnd)

        time.sleep(1)
        win32gui.DestroyWindow(hwnd)

    threading.Thread(target=_popup, daemon=True).start()

# -------------------------------------------------
# Always On Top toggle
# -------------------------------------------------

def toggle_always_on_top(hwnd):
    if not hwnd: return
    
    ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)

    if ex_style & win32con.WS_EX_TOPMOST:
        win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0,0,0,0, 
                             win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        set_window_border_color(hwnd, False)
        show_popup("Always On Top: OFF", hwnd)
    else:
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0,0,0,0, 
                             win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        set_window_border_color(hwnd, True)
        show_popup("Always On Top: ON", hwnd)

# -------------------------------------------------
# Listeners
# -------------------------------------------------

def on_click(x, y, button, pressed):
    if button == mouse.Button.middle and pressed:
        hwnd = get_window_under_cursor()
        if hwnd and cursor_on_close_button(hwnd):
            toggle_always_on_top(hwnd)

def hotkey_thread():
    with keyboard.GlobalHotKeys({'<ctrl>+<alt>+t': lambda: toggle_always_on_top(win32gui.GetForegroundWindow())}) as h:
        h.join()

# Εκκίνηση
threading.Thread(target=lambda: mouse.Listener(on_click=on_click).run(), daemon=True).start()
threading.Thread(target=hotkey_thread, daemon=True).start()

while True:
    time.sleep(1)
