''' app/utils/processmanager.py '''
# Third party import
from typing import List

# Local imports
# from app.utils.logger import logger
from app.core.folderwatcher import Process

class ProcessManager:
    """
    Class for managing a list of processes.
    """
    def __init__(self) -> None:
        """
        Initialize the ProcessManager object.
        """
        self.processes: List[Process] = []

    def add_process(self, process: Process) -> None:
        """
        Add a process to the list of processes.

        Args:
            process (Process): The process object to add.
        """
        self.processes.append(process)

    def execute_processes(self, filepath: str) -> None:
        """
        Execute the list of processes on a file.

        Args:
            filepath (str): The path of the file to process.
        """
        for process in self.processes:
            process.execute(filepath)
