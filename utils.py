import ctypes
import time

import win32.lib.win32con as win32con
from win32 import win32gui
from win32 import win32api
import pygetwindow as gw


MAX_ACTIVATE_RERTRIES = 50


def set_square_edges(hwnd: gw.Win32Window | int):
    if isinstance(hwnd, gw.Win32Window):
        hwnd = hwnd._hWnd

    # constants for window style
    GWL_STYLE = -16
    WS_BORDER = 0x00800000
    WS_OVERLAPPEDWINDOW = 0x00CF0000

    # get the current window style
    style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_STYLE)

    # modify the window style to have squared borders
    new_style = style & ~WS_OVERLAPPEDWINDOW | WS_BORDER
    ctypes.windll.user32.SetWindowLongW(hwnd, GWL_STYLE, new_style)


def set_window_opacity(hwnd: gw.Win32Window | int, opacity: float):
    if isinstance(hwnd, gw.Win32Window):
        hwnd = hwnd._hWnd

    # set window style to layered
    win32gui.SetWindowLong(
        hwnd,
        win32con.GWL_EXSTYLE,
        win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED,
    )

    # set window opacity
    win32gui.SetLayeredWindowAttributes(
        hwnd, win32api.RGB(0, 0, 0), int(255 * opacity), win32con.LWA_ALPHA
    )


def set_always_on_top(hwnd: gw.Win32Window | int):
    if isinstance(hwnd, gw.Win32Window):
        hwnd = hwnd._hWnd

    win32gui.SetWindowPos(
        hwnd,
        win32con.HWND_TOPMOST,
        0,
        0,
        0,
        0,
        win32con.SWP_NOMOVE | win32con.SWP_NOSIZE,
    )


def set_window_pos(hwnd: gw.Win32Window | int, x: int, y: int):
    if not isinstance(hwnd, gw.PyGetWindowException):
        for window in gw.getAllWindows():
            if window._hWnd == hwnd:
                hwnd = window
                break

    prev_x = hwnd.left
    prev_y = hwnd.top

    offset_x = x - prev_x - 2
    offset_y = y - prev_y

    hwnd.move(offset_x, offset_y)


def set_window_size(hwnd: gw.Win32Window | int, w: int, h: int):
    if not isinstance(hwnd, gw.PyGetWindowException):
        for window in gw.getAllWindows():
            if window._hWnd == hwnd:
                hwnd = window
                break

    prev_w = hwnd.width
    prev_h = hwnd.height

    offset_w = w - prev_w - 2
    offset_h = h - prev_h

    hwnd.resize(offset_w, offset_h)


def activate_window(hwnd: gw.Win32Window | int):
    if not isinstance(hwnd, gw.PyGetWindowException):
        for window in gw.getAllWindows():
            if window._hWnd == hwnd:
                hwnd = window
                break

    attempt_counter = 1
    while attempt_counter <= MAX_ACTIVATE_RERTRIES:
        print(f"attempt #{attempt_counter}")
        try:
            hwnd.activate()
            break

        except gw.PyGetWindowException:
            time.sleep(1 / 10)
            attempt_counter += 1
            continue

    if attempt_counter >= MAX_ACTIVATE_RERTRIES:
        msg = "Could not activate window"
        raise gw.PyGetWindowException(msg)
