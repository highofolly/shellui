import logging


def create_level(level: int, name: str):
    logging.addLevelName(level, name)

    def logging_message(message, *args, **kwargs):
        if logging.root.isEnabledFor(level):
            logging.log(level, message, *args, **kwargs)

    return logging_message


EVENT = 5
logging.event = create_level(EVENT, "EVENT")
KEYBOARD = 6
logging.keyboard = create_level(KEYBOARD, "KEYBOARD")
CREATE = 7
logging.create = create_level(CREATE, "CREATE")


def debug_start(logging_filename: str = "shellui_debug.log",
                logging_level: int = CREATE,
                logging_format: str = "%(asctime)s - %(levelname)s - %(filename)s : %(message)s\n",
                save_traceback: bool = True) -> None:

    def exception_handler(exc_type, exc_value, exc_traceback):
        logging.critical(exc_value)
        if exc_traceback is not None and save_traceback:
            import traceback
            import subprocess
            open("traceback.log", "w").write(''.join(traceback.format_tb(exc_traceback)) + f"\n{exc_value}")
            subprocess.Popen(
                "start cmd /c powershell.exe -Command type traceback.log; Write-Host '\033[31mError traceback log is saved to traceback.log file\033[0m'; pause",
                shell=True)

    import sys
    sys.excepthook = exception_handler

    logging.basicConfig(level=logging_level, filename=logging_filename, filemode="w", format=logging_format)
