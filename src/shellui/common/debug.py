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


def debug_start(file_name: str = "shellui_debug.log", logging_level: int = logging.DEBUG, save_critical_error: bool = True):
    if save_critical_error:
        def exception_handler(exc_type, exc_value, exc_traceback):
            logging.critical(exc_value)
            if exc_traceback is not None:
                import traceback
                import subprocess
                open("critical_error.log", "w").write(''.join(traceback.format_tb(exc_traceback)))
                subprocess.Popen(
                    "start cmd /c powershell.exe -Command type critical_error.log; Write-Host '\033[31mCritical error log is saved to critical_error.log file\033[0m'; pause",
                    shell=True)

        import sys
        sys.excepthook = exception_handler

    logging.basicConfig(level=logging_level, filename=file_name, filemode="w",
                        format="%(asctime)s - %(levelname)s - %(filename)s : %(message)s\n")
