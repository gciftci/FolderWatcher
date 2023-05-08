''' app/utils/folderwatcher.py '''
# Third party imports
import os
import time
import fnmatch
from typing import List, Optional

# Local imports
from app.utils.logger import logger


class FolderWatcher:
    """
    Class that monitors a folder for new files and processes them using a list of processes.
    """
    def __init__(self, watchpath: str,
                 outputpath: str,
                 process_list: List,
                 process_existing_files: bool = False,
                 ignore_list: Optional[List[str]] = None) -> None:
        """
        Initialize the FolderWatcher object.

        Args:
            watchpath (str): The path of the folder to monitor.
            outputpath (str): The path of the folder to output processed files to.
            process_list (List): A list of process objects to use for processing files.
            process_existing_files (bool): Whether to process existing files in the folder or not.
            ignore_list (Optional[List[str]]): List of file patterns to ignore.
        """
        self.start_time = time.time()
        self.ignore_list = ignore_list or []
        self.watchpath = watchpath
        self.outputpath = outputpath
        self.process_list = process_list
        self.process_existing_files = process_existing_files
        self.running = True

    def start(self) -> None:
        """
        Start monitoring the folder for new files and processing them.
        """
        logger.info("[bold green]Watching folder..")
        logger.info("Outputting to folder: [yellow underline]%s[/yellow underline]",
                    self.outputpath)
        logger.info("Processing existing files: [yellow underline]%s[/yellow underline]",
                    self.process_existing_files)
        logger.info("Press [yellow underline]Ctrl+C[/yellow underline] to stop")
        printed_ignore_files = set()

        while True:
            for filename in os.listdir(self.watchpath):
                if any(fnmatch.fnmatch(filename, pattern) for pattern in self.ignore_list):
                    if filename not in printed_ignore_files:
                        logger.info("[yellow]Ignored file: %s[/yellow]", filename)
                        printed_ignore_files.add(filename)
                    continue

                filepath = os.path.join(self.watchpath, filename)
                if os.path.isfile(filepath):
                    logger.info("[green]Processing file: %s[/green]", filename)
                    self.process_file(filepath)

            time.sleep(3)

    def stop(self) -> None:
        """
        Stop monitoring the folder.
        """
        self.running = False

    def process_file(self, filepath: str) -> None:
        """
        Process a file using the registered processes.

        Args:
            filepath (str): The path of the file to process.
        """
        updated_filepath = filepath

        for process in self.process_list:
            updated_filepath = process.execute(updated_filepath)
            logger.info("\t\t[bold green]+[/bold green] %s complete: %s",
                        process.__class__.__name__, updated_filepath)

class Process:
    """
    Base class for defining a process to be executed on a file.
    """
    def execute(self, filepath: str) -> str:
        """
        Execute the process on a given file.

        Args:
            filepath (str): The path of the file to process.

        Returns:
            str: The updated path of the file after processing.
        """
        raise NotImplementedError
