# display_utils.py

import os
import sys
import time
from contextlib import contextmanager
import threading

def colored_custom(text, r, g, b):
    """
    Returns text colored with the specified RGB values.
    """
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

def print_ascii_art():
    """
    Prints the ASCII art logo of Verblaze.
    """
    os.system('clear')
    ascii_art = [
        "                    _      _                        ___   __   _____ ",
        " /\\   /\\ ___  _ __ | |__  | |  __ _  ____ ___      / __\\ / /   \\_   \\",
        " \\ \\ / // _ \\| '__|| '_ \\ | | / _` ||_  // _ \\    / /   / /     / /\\/ ",
        "  \\ V /|  __/| |   | |_) || || (_| | / /|  __/   / /___/ /___/\\/ /_  ",
        "   \\_/  \\___||_|   |_.__/ |_| \\__,_|/___|\\___|   \\____/\\____/\\____/  ",
        "                                                                     "
    ]
    for line in ascii_art:
        print(colored_custom(line, 79, 70, 229))

def loading_animation():
    """
    Displays a simple loading animation in the console.
    """
    loading = "Strings are being extracted: [----------]"
    for i in range(10):
        progress = loading[:29] + "=" * i + "-" * (10 - i) + "]"
        sys.stdout.write('\r' + progress)
        sys.stdout.flush()
        time.sleep(0.5)
    sys.stdout.write('\n')
    
def async_loading_animation():
    """
    Displays a continuous loading animation with a spinning cursor.
    """
    spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    message = "Synchronizing strings.."
    try:
        i = 0
        while True:
            sys.stdout.write('\r' + colored_custom(f"{message} {spinner[i]}", 79, 70, 229))
            sys.stdout.flush()
            time.sleep(0.1)
            i = (i + 1) % len(spinner)
    except KeyboardInterrupt:
        sys.stdout.write('\r')
        sys.stdout.flush()

@contextmanager
def loading_animation_context():
    """
    Context manager for the loading animation.
    """
    animation_thread = threading.Thread(target=async_loading_animation)
    animation_thread.daemon = True
    try:
        animation_thread.start()
        yield
    finally:
        sys.stdout.write('\r' + ' ' * 50 + '\r')  # Clear the line
        sys.stdout.flush()