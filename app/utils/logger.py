''' app/utils/logger.py '''
# Third party imports
import os
import logging
from rich.logging import RichHandler
from rich.console import Console

# Logfilename/path
LOG_FILE_NAME = "watcher.log"
LOGFILE_PATH = os.path.join(os.getcwd(), LOG_FILE_NAME) # or: LOGFILE_PATH = "C:\\logs\\myapp.log"

# Initialize the console
console = Console(record=True)

# Initialize the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a file handler
handler = RichHandler(
    console=console,
    rich_tracebacks=True,
    show_time=True,
    markup=True,
)
handler.setLevel(logging.INFO)
#formatter = logging.Formatter("%(message)s")
formatter = logging.Formatter(
        '%(asctime)s [%(threadName)s.{}] '
        '[%(name)s] [%(levelname)s]  '
        '%(message)s')

handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(handler)

# Create a file handler for the log file
log_file_handler = logging.FileHandler(LOGFILE_PATH)
log_file_handler.setLevel(logging.INFO)
log_file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(log_file_handler)
