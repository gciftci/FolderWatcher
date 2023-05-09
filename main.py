''' main.py '''
# Third party imports
import json

# Local imports
from app.utils.config import _C
from app.utils.logger import _L
from app.core.folderwatcher import FolderWatcher
from app.core.processmanager import ProcessManager
from app.processes.main.move import Move
from app.processes.main.rename import Rename
from app.processes.custom.sort_files import SortFiles

# Clear the console screen
# os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    # Create a ProcessManager object and add the required processes to it
    process_manager = ProcessManager()
    process_manager.add_process(Rename())
    process_manager.add_process(Move())
    process_manager.add_process(SortFiles())

    # Create a FolderWatcher object and start monitoring the folder
    watcher = FolderWatcher(
        watchpath=_C.get("watcher", "watchpath"),
        outputpath=_C.get("watcher", "outputpath"),
        process_list=process_manager.processes,
        process_existing_files=_C.get("watcher", "process_existing_files"),
        ignore_list=json.loads(_C.get("watcher", "ignore_list"))
    )
    try:
        watcher.start()
    except KeyboardInterrupt:
        watcher.stop()
        _L.rule(style="bold red", title="[bold red]Stopping folder watcher..", align="left")
