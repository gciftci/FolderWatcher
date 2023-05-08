''' main.py '''
# Third party imports

# Local imports
from app.utils.logger import logger
from app.core.folderwatcher import FolderWatcher
from app.core.processmanager import ProcessManager
from app.processes.main.move import Move
from app.processes.main.rename import Rename
from app.processes.custom.ocr import OCR

# Clear the console screen
# os.system('cls' if os.name == 'nt' else 'clear')

# Constants
WATCHPATH: str = "C:\\test"
PROCESS_EXISTING_FILES: bool = True
OUTPUTPATH: str = "C:\\output"
IGNORE_LIST = ["*.log", "testfile.txt"]


if __name__ == "__main__":
    # Create a ProcessManager object and add the required processes to it
    process_manager = ProcessManager()
    process_manager.add_process(Rename(outputpath=OUTPUTPATH))
    process_manager.add_process(Move(outputpath=OUTPUTPATH))
    process_manager.add_process(OCR())

    # Create a FolderWatcher object and start monitoring the folder
    watcher = FolderWatcher(
        watchpath=WATCHPATH,
        outputpath=OUTPUTPATH,
        process_list=process_manager.processes,
        process_existing_files=PROCESS_EXISTING_FILES,
        ignore_list=IGNORE_LIST
    )
    try:
        watcher.start()
    except KeyboardInterrupt:
        watcher.stop()
        logger.info("[bold red]Stopping folder watcher..[/bold red]")
