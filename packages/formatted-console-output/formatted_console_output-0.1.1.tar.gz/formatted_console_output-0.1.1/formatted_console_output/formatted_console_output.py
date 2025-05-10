import os
from enum import Enum

is_supported = True


class ForegroundColor(Enum):
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"


class BackgroundColor(Enum):
    BLACK = "\033[40m"
    RED = "\033[41m"
    GREEN = "\033[42m"
    YELLOW = "\033[43m"
    BLUE = "\033[44m"
    MAGENTA = "\033[45m"
    CYAN = "\033[46m"
    WHITE = "\033[47m"


class TextFormat(Enum):
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    NONE = ""


RESET = "\033[0m"


def output_formatted_message(
    *args,
    fg_color=ForegroundColor.WHITE,
    bg_color=BackgroundColor.BLACK,
    format=TextFormat.NONE,
    **kwargs,
):
    global is_supported
    message = " ".join(map(str, args))
    if is_supported:
        print(
            f"{bg_color.value}{fg_color.value}{format.value}{message}{RESET}", **kwargs
        )
    else:
        print(message, **kwargs)


def enable_ansi_support():
    if os.name == "nt":  # Check if the OS is Windows
        import ctypes

        kernel32 = ctypes.windll.kernel32
        # Enable ANSI escape sequences
        result = kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        if not result:
            print(
                "ANSI escape sequences for color coding is not supported or cannot be enabled."
            )
            return False
    return True


is_supported = enable_ansi_support()
