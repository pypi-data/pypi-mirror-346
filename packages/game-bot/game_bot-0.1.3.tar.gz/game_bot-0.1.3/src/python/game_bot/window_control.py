import win32gui
import win32con
import time
from typing import Tuple, Optional

def find_window_by_name(name: str) -> Optional[int]:
    """Find a window by its title (supports substring match).
    
    Args:
        name: The window title or substring to search for.
        
    Returns:
        Window handle if found, None otherwise.
    """
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            window_text = win32gui.GetWindowText(hwnd)
            if name.lower() in window_text.lower():
                windows.append(hwnd)
    
    windows = []
    win32gui.EnumWindows(callback, windows)
    return windows[0] if windows else None

def get_window_rect(hwnd: int) -> Optional[Tuple[int, int, int, int]]:
    """Get window position and size.
    
    Args:
        hwnd: Window handle.
        
    Returns:
        Tuple of (left, top, right, bottom) coordinates if window exists,
        None otherwise.
    """
    try:
        return win32gui.GetWindowRect(hwnd)
    except win32gui.error:
        return None

def move_window(hwnd: int, x: int, y: int, width: Optional[int] = None, height: Optional[int] = None, repaint: bool = True) -> bool:
    """Move and optionally resize a window. If the window is maximized, it will be restored first,
    then moved. If width and height are not specified, the window's current dimensions will be used.
    
    Args:
        hwnd: Window handle.
        x: New x-coordinate.
        y: New y-coordinate.
        width: New width (optional). If None, current width will be used.
        height: New height (optional). If None, current height will be used.
        repaint: Whether to repaint the window.
        
    Returns:
        True if successful, False otherwise.
    """
    try:
        # Check if window is maximized
        placement = win32gui.GetWindowPlacement(hwnd)
        was_maximized = placement[1] == win32con.SW_MAXIMIZE
        
        # Restore window if maximized
        if was_maximized:
            restore_window(hwnd)
        
        # Get current window dimensions if width or height is None
        if width is None or height is None:
            current_rect = get_window_rect(hwnd)
            if current_rect is None:
                return False
            if width is None:
                width = current_rect[2] - current_rect[0]
            if height is None:
                height = current_rect[3] - current_rect[1]
        
        # Move window
        win32gui.MoveWindow(hwnd, x, y, width, height, repaint)
        time.sleep(0.1)  # Small delay before state change
        
        return True
    except win32gui.error:
        return False

def set_window_state(hwnd: int, state: str) -> bool:
    """Set window state (minimize, maximize, restore).
    
    Args:
        hwnd: Window handle.
        state: One of 'minimize', 'maximize', or 'restore'.
        
    Returns:
        True if successful, False otherwise.
    """
    try:
        if state == 'minimize':
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
        elif state == 'maximize':
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        elif state == 'restore':
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        else:
            return False
        return True
    except win32gui.error:
        return False

def bring_to_front(hwnd: int) -> bool:
    """Bring window to front.
    
    Args:
        hwnd: Window handle.
        
    Returns:
        True if successful, False otherwise.
    """
    try:
        win32gui.SetForegroundWindow(hwnd)
        return True
    except win32gui.error:
        return False

def list_windows() -> dict[int, str]:
    """List all visible windows.
    
    Returns:
        Dictionary mapping window handles to window titles.
    """
    windows = {}
    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:
                windows[hwnd] = title
    
    win32gui.EnumWindows(callback, None)
    return windows

def maximize_window(hwnd: int) -> bool:
    """Maximize a window.
    
    Args:
        hwnd: Window handle.
        
    Returns:
        True if successful, False otherwise.
    """
    return set_window_state(hwnd, 'maximize')

def minimize_window(hwnd: int) -> bool:
    """Minimize a window.
    
    Args:
        hwnd: Window handle.
        
    Returns:
        True if successful, False otherwise.
    """
    return set_window_state(hwnd, 'minimize')

def restore_window(hwnd: int) -> bool:
    """Restore a window from minimized or maximized state.
    
    Args:
        hwnd: Window handle.
        
    Returns:
        True if successful, False otherwise.
    """
    set_window_state(hwnd, 'restore')

def activate_window(hwnd: int) -> bool:
    """Activate a window (bring it to front).

    Args:
        hwnd: Window handle.

    Returns:
        True if successful, False otherwise.
    """
    return bring_to_front(hwnd)