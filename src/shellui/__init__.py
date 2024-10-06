"""
shellui - library simplifies the creation of TUI (Text User Interface)
          in the terminal. Offers a clean and intuitive architecture to
          help you build interactive applications effortlessly.
            Contacts:
        Author - highofolly
        Source - https://github.com/highofolly/shellui
         Email - sw3atyspace@gmail.com
        GitHub - https://github.com/highofolly
       Youtube - https://www.youtube.com/@sw3aty702
"""

__version__ = "0.3.0a1"

import logging


def create_level(level: int, name: str):
    logging.addLevelName(level, name)

    def logging_message(message, *args, **kwargs):
        if logging.root.isEnabledFor(level):
            logging.log(level, message, *args, **kwargs)

    return logging_message


def debug_start(file_name: str = "shellui_debug.log", logging_level: int = logging.DEBUG):
    logging.basicConfig(level=logging_level, filename=file_name, filemode="w",
                        format="%(asctime)s - %(levelname)s - %(filename)s : %(message)s\n")
