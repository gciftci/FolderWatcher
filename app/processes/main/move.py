""" app/processes/main/move.py
Process for moving a file to a subfolder called "processed".

Attributes:
    outputpath (str): The path of the folder to output processed files to.

Notes:
    - This process creates the specified output folder if it does not already exist.
    - If the file already exists in the output folder, it will be overwritten.
"""
# Third party imports
import os
import shutil

# Local imports
# from app.utils.logger import logger
from app.core.folderwatcher import Process


class Move(Process):
    """
    Process for moving a file to a subfolder called "processed".
    """
    def __init__(self, outputpath: str) -> None:
        """
        Initialize the Move process.

        Args:
            outputpath (str): The path of the folder to move processed files to.
        """
        self.outputpath = outputpath

    def execute(self, filepath: str) -> str:
        """
        Move a file to the specified output folder.

        Args:
            filepath (str): The path of the file to move.

        Returns:
            str: The updated path of the file after moving.
        """
        os.makedirs(self.outputpath, exist_ok=True)
        new_filepath = os.path.join(self.outputpath, os.path.basename(filepath))
        shutil.move(filepath, new_filepath)
        return new_filepath
