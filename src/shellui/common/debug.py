import logging as _logging

logger = _logging.getLogger("shelluiStream")
logger.handlers = [h for h in logger.handlers if not isinstance(h, _logging.StreamHandler)]


def create_level(level: int, name: str):
    _logging.addLevelName(level, name)

    def logging_message(message, *args, **kwargs):
        # if _logging.root.isEnabledFor(level):
        logger.log(level, message, *args, **kwargs)

    return logging_message

EVENT = 5
logger.event = create_level(EVENT, "EVENT")
KEYBOARD = 6
logger.keyboard = create_level(KEYBOARD, "KEYBOARD")
CREATE = 7
logger.create = create_level(CREATE, "CREATE")


def debug_start(logging_filename: str = "shellui.log",
                logging_level: int = CREATE,
                logging_format: str = "%(asctime)s - %(levelname)s - %(filename)s : %(message)s\n",
                save_traceback: bool = True) -> None:

    def exception_handler(exc_type, exc_value, exc_traceback):
        _logging.critical(exc_value)
        if exc_traceback is not None and save_traceback:
            import traceback
            import subprocess
            open("traceback.log", "w").write(''.join(traceback.format_tb(exc_traceback)) + f"\n{exc_type.__name__}: {exc_value}")
            subprocess.Popen(
                "start cmd /c powershell.exe -Command type traceback.log; Write-Host '\033[31mError traceback log is saved to traceback.log file\033[0m'; pause",
                shell=True)

    import sys
    sys.excepthook = exception_handler

    file_handler = _logging.FileHandler(logging_filename, mode="w")
    file_handler.setLevel(logging_level)
    file_handler.setFormatter(_logging.Formatter(logging_format))

    logger.setLevel(logging_level)
    logger.addHandler(file_handler)
