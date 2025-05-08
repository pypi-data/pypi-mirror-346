import ctypes
import time
import random
import math
from ctypes import wintypes

# Load required DLLs
user32 = ctypes.WinDLL('user32', use_last_error=True)
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

# Constants for key events
INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
KEYEVENTF_KEYDOWN = 0x0000
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_EXTENDEDKEY = 0x0001

# Mouse event constants
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040
MOUSEEVENTF_WHEEL = 0x0800
MOUSEEVENTF_ABSOLUTE = 0x8000

# Virtual key codes
VK_CODE = {
    'backspace': 0x08, 'tab': 0x09, 'clear': 0x0C, 'enter': 0x0D, 'return': 0x0D, 
    'shift': 0x10, 'ctrl': 0x11, 'alt': 0x12, 'pause': 0x13, 'caps_lock': 0x14, 
    'esc': 0x1B, 'escape': 0x1B, 'space': 0x20, 'page_up': 0x21, 'pgup': 0x21, 
    'page_down': 0x22, 'pgdn': 0x22, 'end': 0x23, 'home': 0x24, 'left': 0x25, 
    'up': 0x26, 'right': 0x27, 'down': 0x28, 'select': 0x29, 'print': 0x2A, 
    'execute': 0x2B, 'print_screen': 0x2C, 'prtsc': 0x2C, 'prtscr': 0x2C, 
    'insert': 0x2D, 'ins': 0x2D, 'delete': 0x2E, 'del': 0x2E, 
    '0': 0x30, '1': 0x31, '2': 0x32, '3': 0x33, '4': 0x34, '5': 0x35, 
    '6': 0x36, '7': 0x37, '8': 0x38, '9': 0x39, 
    'a': 0x41, 'b': 0x42, 'c': 0x43, 'd': 0x44, 'e': 0x45, 'f': 0x46, 
    'g': 0x47, 'h': 0x48, 'i': 0x49, 'j': 0x4A, 'k': 0x4B, 'l': 0x4C, 
    'm': 0x4D, 'n': 0x4E, 'o': 0x4F, 'p': 0x50, 'q': 0x51, 'r': 0x52, 
    's': 0x53, 't': 0x54, 'u': 0x55, 'v': 0x56, 'w': 0x57, 'x': 0x58, 
    'y': 0x59, 'z': 0x5A, 
    'win': 0x5B, 'windows': 0x5B, 'lwin': 0x5B, 'rwin': 0x5C, 
    'apps': 0x5D, 'sleep': 0x5F, 
    'numpad0': 0x60, 'numpad1': 0x61, 'numpad2': 0x62, 'numpad3': 0x63, 
    'numpad4': 0x64, 'numpad5': 0x65, 'numpad6': 0x66, 'numpad7': 0x67, 
    'numpad8': 0x68, 'numpad9': 0x69, 
    'multiply': 0x6A, 'add': 0x6B, 'separator': 0x6C, 'subtract': 0x6D, 
    'decimal': 0x6E, 'divide': 0x6F, 
    'f1': 0x70, 'f2': 0x71, 'f3': 0x72, 'f4': 0x73, 'f5': 0x74, 
    'f6': 0x75, 'f7': 0x76, 'f8': 0x77, 'f9': 0x78, 'f10': 0x79, 
    'f11': 0x7A, 'f12': 0x7B, 'f13': 0x7C, 'f14': 0x7D, 'f15': 0x7E, 
    'f16': 0x7F, 'f17': 0x80, 'f18': 0x81, 'f19': 0x82, 'f20': 0x83, 
    'f21': 0x84, 'f22': 0x85, 'f23': 0x86, 'f24': 0x87, 
    'num_lock': 0x90, 'scroll_lock': 0x91, 
    'lshift': 0xA0, 'rshift': 0xA1, 'lctrl': 0xA2, 'rctrl': 0xA3, 
    'lalt': 0xA4, 'ralt': 0xA5, 
    ';': 0xBA, '=': 0xBB, ',': 0xBC, '-': 0xBD, '.': 0xBE, '/': 0xBF, '`': 0xC0, 
    '[': 0xDB, '\\': 0xDC, ']': 0xDD, "'": 0xDE,
    # Additional key names
    'plus': 0xBB, 'comma': 0xBC, 'minus': 0xBD, 'period': 0xBE, 'slash': 0xBF
}

# Special characters mapping
SHIFT_CHARS = {
    '!': '1', '@': '2', '#': '3', '$': '4', '%': '5', '^': '6', '&': '7', '*': '8',
    '(': '9', ')': '0', '_': '-', '+': '=', '{': '[', '}': ']', '|': '\\', ':': ';',
    '"': "'", '<': ',', '>': '.', '?': '/', '~': '`'
}

# Structures for input events
class MOUSEINPUT(ctypes.Structure):
    _fields_ = (
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(wintypes.ULONG)),
    )

class KEYBDINPUT(ctypes.Structure):
    _fields_ = (
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(wintypes.ULONG)),
    )

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (
        ("uMsg", wintypes.DWORD),
        ("wParamL", wintypes.WORD),
        ("wParamH", wintypes.WORD),
    )

class INPUT_UNION(ctypes.Union):
    _fields_ = (
        ("mi", MOUSEINPUT),
        ("ki", KEYBDINPUT),
        ("hi", HARDWAREINPUT),
    )

class INPUT(ctypes.Structure):
    _fields_ = (
        ("type", wintypes.DWORD),
        ("union", INPUT_UNION),
    )

# Function declarations
user32.GetSystemMetrics.restype = ctypes.c_int
user32.GetSystemMetrics.argtypes = [ctypes.c_int]
user32.SendInput.restype = wintypes.UINT
user32.SendInput.argtypes = [wintypes.UINT, ctypes.POINTER(INPUT), ctypes.c_int]
user32.GetCursorPos.argtypes = [ctypes.POINTER(wintypes.POINT)]
user32.SetCursorPos.argtypes = [ctypes.c_int, ctypes.c_int]
user32.SetCursorPos.restype = ctypes.c_bool

# Get screen dimensions
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

def _generate_human_curve(start_x, start_y, end_x, end_y, control_points=2):
    """Generate a Bezier curve for more human-like movement."""
    points = [(start_x, start_y), (end_x, end_y)]
    
    # Add random control points to make the curve more natural
    for _ in range(control_points):
        # Control points closer to the direct path but with some randomness
        ctrl_x = start_x + random.uniform(0.3, 0.7) * (end_x - start_x)
        ctrl_y = start_y + random.uniform(0.3, 0.7) * (end_y - start_y)
        
        # Add some perpendicular offset for curve shape
        perpendicular_x = -(end_y - start_y) * random.uniform(0.05, 0.15)
        perpendicular_y = (end_x - start_x) * random.uniform(0.05, 0.15)
        
        ctrl_x += perpendicular_x
        ctrl_y += perpendicular_y
        
        # Insert control point in the middle
        points.insert(1, (ctrl_x, ctrl_y))
    
    return points

def _bezier_curve(points, steps):
    """Calculate points along a Bezier curve with the given control points."""
    curve_points = []
    for t in range(steps + 1):
        t = t / steps
        
        # De Casteljau's algorithm for Bezier curves
        new_points = points.copy()
        while len(new_points) > 1:
            temp = []
            for i in range(len(new_points) - 1):
                x = (1 - t) * new_points[i][0] + t * new_points[i + 1][0]
                y = (1 - t) * new_points[i][1] + t * new_points[i + 1][1]
                temp.append((x, y))
            new_points = temp
        
        curve_points.append(new_points[0])
    
    return curve_points

def _add_micro_movements(path, intensity=0.3):
    """Add tiny movements to the path to simulate human hand tremors."""
    result = []
    for point in path:
        x, y = point
        # Small random deviations to make movement look natural
        x += random.uniform(-intensity, intensity)
        y += random.uniform(-intensity, intensity)
        result.append((x, y))
    return result

def _get_random_delay(min_delay=0.001, max_delay=0.003, speed_factor=1.0):
    """Get a random delay to simulate human timing variations."""
    base_delay = random.uniform(min_delay, max_delay)
    # Occasionally add a longer pause to make it seem more natural
    if random.random() < 0.05:
        base_delay *= random.uniform(2, 4)
    return base_delay / speed_factor

def get_cursor_pos():
    """Get the current cursor position."""
    point = wintypes.POINT()
    user32.GetCursorPos(ctypes.byref(point))
    return (point.x, point.y)

def _send_mouse_event(flags, x=None, y=None, data=0):
    """Send a mouse event to the system."""
    extra = ctypes.pointer(wintypes.ULONG(0))
    
    if flags == MOUSEEVENTF_LEFTDOWN or flags == MOUSEEVENTF_LEFTUP or \
       flags == MOUSEEVENTF_RIGHTDOWN or flags == MOUSEEVENTF_RIGHTUP or \
       flags == MOUSEEVENTF_WHEEL:
        # For click events, don't include coordinates - use current position
        input_struct = INPUT(
            type=INPUT_MOUSE,
            union=INPUT_UNION(
                mi=MOUSEINPUT(
                    dx=0, dy=0,
                    mouseData=data,
                    dwFlags=flags,
                    time=0,
                    dwExtraInfo=extra
                )
            )
        )
    else:
        # For movement events, include normalized coordinates
        if x is None or y is None:
            # Use current cursor position if coordinates not provided
            point = wintypes.POINT()
            user32.GetCursorPos(ctypes.byref(point))
            x, y = point.x, point.y
        
        # Convert to normalized coordinates (0-65535)
        norm_x = int(x * 65535 / screen_width)
        norm_y = int(y * 65535 / screen_height)
        
        input_struct = INPUT(
            type=INPUT_MOUSE,
            union=INPUT_UNION(
                mi=MOUSEINPUT(
                    dx=norm_x, dy=norm_y,
                    mouseData=data,
                    dwFlags=MOUSEEVENTF_ABSOLUTE | MOUSEEVENTF_MOVE | flags,
                    time=0,
                    dwExtraInfo=extra
                )
            )
        )
    
    # Send input
    user32.SendInput(1, ctypes.byref(input_struct), ctypes.sizeof(INPUT))

def move_cursor_to(x, y, speed=1.0, randomize=True):
    """Move cursor to specified coordinates with human-like movement."""
    start_x, start_y = get_cursor_pos()
    
    # Calculate distance for determining steps
    distance = math.sqrt((x - start_x)**2 + (y - start_y)**2)
    
    # If the distance is very small, just move directly
    if distance < 5:
        # Direct move for small distances
        # We're using SetCursorPos for direct moves as it's more reliable for small distances
        user32.SetCursorPos(int(x), int(y))
        return
    
    # Adjust number of steps based on distance and speed
    steps = max(int(distance / 10), 10)
    
    if randomize:
        # Generate a human-like curve
        control_points = _generate_human_curve(start_x, start_y, x, y)
        
        # Generate points along the curve
        path = _bezier_curve(control_points, steps)
        
        # Add micro-movements to simulate human hand tremor
        path = _add_micro_movements(path, intensity=0.3)
    else:
        # Linear interpolation for non-randomized movement
        path = []
        for i in range(steps + 1):
            t = i / steps
            path_x = start_x + t * (x - start_x)
            path_y = start_y + t * (y - start_y)
            path.append((path_x, path_y))
    
    # Move along the path
    for idx, (point_x, point_y) in enumerate(path):
        if idx == len(path) - 1:  # Last point - ensure we reach exact destination
            user32.SetCursorPos(int(x), int(y))
        else:
            user32.SetCursorPos(int(point_x), int(point_y))
        
        # Only add delay between points, not after the last one
        if idx < len(path) - 1:
            time.sleep(_get_random_delay(speed_factor=speed))

def left_click(x=None, y=None):
    """Perform a left mouse click at the specified coordinates or current position."""
    if x is not None and y is not None:
        move_cursor_to(x, y)
    
    # Add slight delay between down and up to simulate real click
    _send_mouse_event(MOUSEEVENTF_LEFTDOWN)
    time.sleep(_get_random_delay(0.01, 0.03))  # Realistic click duration
    _send_mouse_event(MOUSEEVENTF_LEFTUP)
    
    # Sometimes add a tiny pause after clicking
    if random.random() < 0.3:
        time.sleep(_get_random_delay(0.05, 0.1))

def right_click(x=None, y=None):
    """Perform a right mouse click at the specified coordinates or current position."""
    if x is not None and y is not None:
        move_cursor_to(x, y)
    
    _send_mouse_event(MOUSEEVENTF_RIGHTDOWN)
    time.sleep(_get_random_delay(0.01, 0.03))
    _send_mouse_event(MOUSEEVENTF_RIGHTUP)
    
    # Sometimes add a tiny pause after clicking
    if random.random() < 0.3:
        time.sleep(_get_random_delay(0.05, 0.1))

def double_click(x=None, y=None):
    """Perform a double click at the specified coordinates or current position."""
    if x is not None and y is not None:
        move_cursor_to(x, y)
    
    # Alternative implementation using the system's double-click function
    # This is more reliable across different Windows systems
    MOUSEEVENTF_DOUBLECLICK = 0x0002  # Same as MOUSEEVENTF_LEFTDOWN
    
    # Method 1: Try using direct double-click simulation
    _send_mouse_event(MOUSEEVENTF_LEFTDOWN)
    time.sleep(0.01)
    _send_mouse_event(MOUSEEVENTF_LEFTUP)
    time.sleep(0.05)  # Shorter delay for double-click
    _send_mouse_event(MOUSEEVENTF_LEFTDOWN)
    time.sleep(0.01)
    _send_mouse_event(MOUSEEVENTF_LEFTUP)

def scroll_up(ticks=1):
    """Scroll up by the specified number of ticks."""
    for _ in range(ticks):
        # Mouse wheel data is specified in multiples of WHEEL_DELTA (120)
        wheel_delta = 120
        _send_mouse_event(MOUSEEVENTF_WHEEL, data=wheel_delta)
        time.sleep(_get_random_delay(0.02, 0.06))

def scroll_down(ticks=1):
    """Scroll down by the specified number of ticks."""
    for _ in range(ticks):
        # Negative value for scrolling down
        wheel_delta = -120
        _send_mouse_event(MOUSEEVENTF_WHEEL, data=wheel_delta)
        time.sleep(_get_random_delay(0.02, 0.06))

def drag_cursor_to(x, y, speed=1.0):
    """Click and drag from current position to specified coordinates."""
    start_x, start_y = get_cursor_pos()
    
    # Press mouse button down
    _send_mouse_event(MOUSEEVENTF_LEFTDOWN)
    time.sleep(_get_random_delay(0.05, 0.1))
    
    # Move to destination with button held down
    move_cursor_to(x, y, speed, randomize=True)
    
    # Add slight pause before releasing to make it more natural
    time.sleep(_get_random_delay(0.05, 0.1))
    
    # Release mouse button
    _send_mouse_event(MOUSEEVENTF_LEFTUP)

def _send_keyboard_event(key_code, flags=0):
    """Send a keyboard event to the system."""
    extra = ctypes.pointer(wintypes.ULONG(0))
    input_struct = INPUT(
        type=INPUT_KEYBOARD,
        union=INPUT_UNION(
            ki=KEYBDINPUT(
                wVk=key_code,
                wScan=0,
                dwFlags=flags,
                time=0,
                dwExtraInfo=extra
            )
        )
    )
    
    user32.SendInput(1, ctypes.byref(input_struct), ctypes.sizeof(INPUT))

def key_down(key):
    """Press a key down and hold it."""
    key_code = None
    
    if isinstance(key, str) and len(key) == 1:
        # For single character keys
        if key.isupper() or key in SHIFT_CHARS.keys():
            # Press shift for uppercase or special characters
            _send_keyboard_event(VK_CODE['shift'], KEYEVENTF_KEYDOWN)
            
            if key in SHIFT_CHARS:
                # If it's a special character, get its base key
                key = SHIFT_CHARS[key]
            else:
                # Otherwise convert to lowercase for key lookup
                key = key.lower()
        
        if key.isalpha():
            key_code = ord(key.upper())
        elif key.isdigit() or key in [' ', '.', ',', ';', '/', '\\', '[', ']', '-', '=', '`']:
            key_code = ord(key.upper()) if key.isalpha() else ord(key)
        else:
            key_code = VK_CODE.get(key, None)
    else:
        # For named keys like 'shift', 'ctrl', etc.
        key_code = VK_CODE.get(key.lower(), None)
    
    if key_code is not None:
        _send_keyboard_event(key_code, KEYEVENTF_KEYDOWN)
    else:
        raise ValueError(f"Unknown key: {key}")

def key_up(key):
    """Release a previously pressed key."""
    key_code = None
    release_shift = False
    
    if isinstance(key, str) and len(key) == 1:
        # For single character keys
        if key.isupper() or key in SHIFT_CHARS.keys():
            release_shift = True
            
            if key in SHIFT_CHARS:
                # If it's a special character, get its base key
                key = SHIFT_CHARS[key]
            else:
                # Otherwise convert to lowercase for key lookup
                key = key.lower()
        
        if key.isalpha():
            key_code = ord(key.upper())
        elif key.isdigit() or key in [' ', '.', ',', ';', '/', '\\', '[', ']', '-', '=', '`']:
            key_code = ord(key.upper()) if key.isalpha() else ord(key)
        else:
            key_code = VK_CODE.get(key, None)
    else:
        # For named keys like 'shift', 'ctrl', etc.
        key_code = VK_CODE.get(key.lower(), None)
    
    if key_code is not None:
        _send_keyboard_event(key_code, KEYEVENTF_KEYUP)
        if release_shift:
            _send_keyboard_event(VK_CODE['shift'], KEYEVENTF_KEYUP)
    else:
        raise ValueError(f"Unknown key: {key}")

def send_keys(text, typing_speed=1.0):
    """Type the specified text with human-like timing."""
    for char in text:
        # Handle uppercase and special characters
        if char.isupper() or char in SHIFT_CHARS:
            key_down('shift')
            time.sleep(_get_random_delay(speed_factor=typing_speed))
            
            if char in SHIFT_CHARS:
                # Type the base character for special characters
                base_char = SHIFT_CHARS[char]
                key_down(base_char)
                time.sleep(_get_random_delay(speed_factor=typing_speed))
                key_up(base_char)
            else:
                # Type lowercase version for uppercase letters
                key_down(char.lower())
                time.sleep(_get_random_delay(speed_factor=typing_speed))
                key_up(char.lower())
            
            time.sleep(_get_random_delay(speed_factor=typing_speed))
            key_up('shift')
        else:
            # Normal character
            key_down(char)
            time.sleep(_get_random_delay(speed_factor=typing_speed))
            key_up(char)
        
        # Random delay between keystrokes to simulate human typing
        typing_delay = random.uniform(0.05, 0.15) / typing_speed
        
        # Occasionally add a longer pause (as if thinking)
        if random.random() < 0.02:
            typing_delay *= random.uniform(2, 5)
        
        time.sleep(typing_delay)

def hotkey(hold_key, press_key):
    """Press a key while holding another key."""
    # Improved implementation with better handling of modifier keys
    hold_key_code = VK_CODE.get(hold_key.lower(), None)
    if hold_key_code is None:
        raise ValueError(f"Unknown modifier key: {hold_key}")
    
    press_key_code = None
    if isinstance(press_key, str) and len(press_key) == 1:
        if press_key.isalpha():
            press_key_code = ord(press_key.upper())
        elif press_key.isdigit() or press_key in [' ', '.', ',', ';', '/', '\\', '[', ']', '-', '=', '`']:
            press_key_code = ord(press_key)
        else:
            press_key_code = VK_CODE.get(press_key.lower(), None)
    else:
        press_key_code = VK_CODE.get(press_key.lower(), None)
    
    if press_key_code is None:
        raise ValueError(f"Unknown key: {press_key}")
    
    # Direct method using _send_keyboard_event
    _send_keyboard_event(hold_key_code, KEYEVENTF_KEYDOWN)
    time.sleep(0.05)
    _send_keyboard_event(press_key_code, KEYEVENTF_KEYDOWN)
    time.sleep(0.05)
    _send_keyboard_event(press_key_code, KEYEVENTF_KEYUP)
    time.sleep(0.05)
    _send_keyboard_event(hold_key_code, KEYEVENTF_KEYUP)
