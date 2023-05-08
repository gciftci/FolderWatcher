""" app/processes/main/rename.py
This module provides a process for renaming a file using the current date and time. The new file
name is generated based on a syntax that you can customize to fit your needs. The syntax uses curly
braces ({}) to define placeholders for different parts of the file name. The following placeholders
are available:

    - {day}: the day of the month (01 to 31)
    - {month}: the month of the year (01 to 12)
    - {year}: the year (e.g. 2023)
    - {hour}: the hour of the day (00 to 23)
    - {minute}: the minute of the hour (00 to 59)
    - {second}: the second of the minute (00 to 59)
    - {filename}: the original file name (without the extension)
    - {ext}: the file extension (without the dot)

You can use these placeholders to define a custom syntax for your file names. For example, if you
want to rename your files in the format `YYYY-MM-DD_HH-MM-SS_filename.ext`, you can use the
following syntax:

    NEW_FILENAME_FORMAT = "{year}-{month}-{day}_{hour}-{minute}-{second}_{filename}{ext}"

To use a placeholder in the syntax, simply enclose the placeholder name in curly braces. Note that
the placeholders are case-sensitive, so you need to use the exact same spelling and capitalization
as shown above.

Once you have defined your syntax, you can use it to generate a new file name for any file that
you want to rename. The `get_filename` method in this module takes a file path as input and
returns a new file path with the same extension, but with the file name replaced by the new name
generated based on the syntax.
"""

# Third party imports
import os
import shutil
from datetime import datetime

# Local imports
from app.utils.logger import logger
from app.core.folderwatcher import Process

NEW_FILENAME_FORMAT = "[{ext}]-{day}_{month}_{year}-{hour}-{minute}-{second}_{filename}"

class Rename(Process):
    """
    Process for renaming a file using the current date and time.
    """
    def __init__(self, outputpath: str) -> None:
        """
        Constructor method for Rename.

        Args:
            outputpath (str): The path to output processed files to.
        """
        self.outputpath = outputpath

    def execute(self, filepath: str) -> str:
        """
        Rename a file using the current date and time and move it to the output folder.

        Args:
            filepath (str): The path of the file to rename.

        Returns:
            str: The updated path of the file after renaming.
        """
        try:
            return self.get_filename(filepath)
        except FileNotFoundError:
            logger.info("[bold red]Error:[/bold red] File not found: %s", filepath)
            return filepath
        except PermissionError:
            logger.info("[bold red]Error:[/bold red] Permission denied for: %s", filepath)
            return filepath
        except IsADirectoryError:
            logger.info("[bold red]Error:[/bold red] Path is a directory, not a file: %s", filepath)
            return filepath
        except OSError as err:
            logger.info("[bold red]Error:[/bold red] OS error occurred: %s", str(err))
            return filepath
        except ValueError:
            logger.info("[bold red]Error:[/bold red] Invalid path: %s", filepath)
            return filepath

    def get_filename(self, filepath: str) -> str:
        """Get the new filename based on timestamp data.

        Args:
            filepath (str): The path of the file to rename.

        Returns:
            str: The updated path of the file after renaming.
        """
        now = datetime.now()
        timestamp_data = {
            "day": now.strftime("%d"),
            "month": now.strftime("%m"),
            "year": now.strftime("%Y"),
            "hour": now.strftime("%H"),
            "minute": now.strftime("%M"),
            "second": now.strftime("%S"),
            "filename": os.path.basename(os.path.splitext(filepath)[0]),
            "ext": os.path.splitext(filepath)[1][1:],
        }
        new_filename = NEW_FILENAME_FORMAT.format(**timestamp_data) + os.path.splitext(filepath)[1]
        new_filepath = os.path.join(self.outputpath, new_filename)

        shutil.move(filepath, new_filepath)
        return new_filepath
