''' app/processes/custom/sort_files.py '''
# Third party imports
import os

# Local imports
from app.utils.config import _C
from app.utils.logger import _L
from app.core.folderwatcher import Process


class SortFiles(Process):
    """
    Process that sorts files based on their extension and moves them to the appropriate directory.
    """
    def execute(self, filepath: str) -> str:
        # sourcery skip: extract-method, use-next
        """
        Sorts the file based on its extension and moves it to the appropriate directory.

        Args:
            filepath (str): The path of the file to process.

        Returns:
            str: The updated path of the file after processing.
        """
        filename = os.path.basename(filepath)
        extension = os.path.splitext(filename)[1]

        for ext, folder in _C._config.items('sort_files'):
            if extension == ext:
                destination_folder = os.path.join(_C.get('watcher', 'outputpath'), folder)

                if not os.path.exists(destination_folder):
                    os.makedirs(destination_folder)

                destination_path = os.path.join(destination_folder, filename)
                os.replace(filepath, destination_path)

                _L.print(f"[bold green]File sorted: {filename} -> {destination_folder}\
                    [/bold green]")

                return destination_path

        return filepath
