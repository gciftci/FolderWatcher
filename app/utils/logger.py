''' app/utils/logger.py '''
# Third party imports
import os
from datetime import datetime
from typing import Any, Optional
from rich.console import Console
from rich.theme import Theme

# Local imports
from app.utils.config import _C


class RichLogger:
    """
    A Singleton-Class that logs every step and writes to a file.
    """
    _instance: Optional['RichLogger'] = None

    def __new__(cls) -> 'RichLogger':
        """
        Ensures that only one instance of the RichLogger class is created.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self) -> None:
        """
        Initializes the RichLogger object by creating a log file and a Rich Console instance with a custom theme.
        """
        log_file_path = os.path.join(os.path.join(os.getcwd(), _C.get("debug", "log_file_name")))
        self._log_file = open(log_file_path, "a", encoding="UTF8")

        theme = Theme({
            "info": "blue",
            "warning": "yellow",
            "error": "bold red",
            "success": "green",
        })

        self._console = Console(theme=theme)

    def _timestamp(self) -> str:
        """
        Generates a formatted timestamp string in the format [HH:MM:SS].

        Returns:
            str: The formatted timestamp string.
        """
        return datetime.now().strftime("%H:%M:%S")

    def print(self, *args: Any, **kwargs: Any) -> None:
        """
        Prints the given arguments to the console and writes them to the log file with a timestamp.

        Args:
            *args: Arguments to be printed.
            **kwargs: Keyword arguments to be passed to the Rich Console print method.
        """
        timestamp = self._timestamp()
        self._console.print(f"[{timestamp}] ", *args, **kwargs)
        self._log_file.write(f"[{timestamp}] " + " ".join(str(arg) for arg in args) + "\n")

    def log(self, *args: Any, **kwargs: Any) -> None:
        """
        Logs the given arguments to the console and writes them to the log file with a timestamp.

        Args:
            *args: Arguments to be logged.
            **kwargs: Keyword arguments to be passed to the Rich Console log method.
        """
        timestamp = self._timestamp()
        self._console.log(f"[{timestamp}] ", *args, **kwargs)
        self._log_file.write(f"[{timestamp}] " + " ".join(str(arg) for arg in args) + "\n")

    def rule(self, *args: Any, **kwargs: Any) -> None:
        """
        Creates a horizontal rule in the console and writes the rule text to the log file.

        Args:
            *args: Arguments to be used for the rule.
            **kwargs: Keyword arguments to be passed to the Rich Console rule method.
        """
        self._console.rule( *args, **kwargs)
        self._log_file.write(" ".join(str(arg) for arg in args) + "\n")

_L = RichLogger()
