''' app/utils/folderwatcher.py '''
# Third party imports
import os
import time
import fnmatch
from typing import List, Optional

# Local imports
from app.utils.config import _C
from app.utils.logger import _L


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

        _L.rule(title="[bold green]Stopping folder watcher..", style="bold green", align="left")
        _L.print(f"Outputting to folder: [yellow underline]{self.outputpath}[/yellow underline]")
        _L.print(f"Processing existing files: [yellow underline]{self.process_existing_files}\
                 [/yellow underline]")
        _L.print("Press [yellow underline]Ctrl+C[/yellow underline] to stop")
        printed_ignore_files = set()

        while True:
            for filename in os.listdir(self.watchpath):
                if any(fnmatch.fnmatch(filename, pattern) for pattern in self.ignore_list):
                    if filename not in printed_ignore_files:
                        _L.print(f"[yellow]Ignored file: {filename}[/yellow]")
                        printed_ignore_files.add(filename)
                    continue

                filepath = os.path.join(self.watchpath, filename)
                if os.path.isfile(filepath):
                    _L.print(f"[green]Processing file: {filename}[/green]")
                    self.process_file(filepath)

            time.sleep(int(_C.get("watcher", "refresh_rate")))

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
            _L.print(f"\t\t[bold green]+[/bold green] {process.__class__.__name__}\
                complete: {updated_filepath}")

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
