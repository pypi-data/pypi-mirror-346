import logging
import sys
from typing import TextIO

from colorama import Back, Fore, init

# Initialize colorama for Windows compatibility
init(autoreset=True)


class ColorizedFormatter(logging.Formatter):
    """
    Custom formatter for colorizing log messages based on their level.
    """

    LEVEL_COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.WHITE + Back.RED,
    }

    log_format = (
        "%(asctime)s %(name)s[%(process)d] %(levelname)s" + Fore.RESET + " %(message)s"
    )
    date_format = "%Y-%m-%d %H:%M:%S"

    def __init__(self):
        super().__init__(fmt=self.log_format, datefmt=self.date_format)

    def format(self, record):
        message = super().format(record)
        # Apply color based on the log level and if there is an attached TTY
        if sys.stdout.isatty():
            message = self.LEVEL_COLORS.get(record.levelno, Fore.RESET) + message

        return message


def init_colors(level: int = logging.INFO, output: TextIO = sys.stderr):
    """
    Initialize the logger with colorized output.

    Args:
        level (int): The logging level (default is logging.INFO).
        output (TextIO): The output stream (default is sys.stderr).
    """
    logger = logging.getLogger()
    logger.setLevel(level)

    # Create console handler (logs to stdout)
    console_handler = logging.StreamHandler(output)
    console_handler.setLevel(level)

    # Create formatter with colorized output and custom log format
    formatter = ColorizedFormatter()
    console_handler.setFormatter(formatter)

    # Add handler to the logger
    logger.addHandler(console_handler)


if __name__ == "__main__":
    # Configure the logger
    init_colors(level=logging.DEBUG)

    # Example log messages
    logger = logging.getLogger("test.logger")
    logger.debug("This is a debug message")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")
