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

__version__ = "0.2a2"

import logging


def debug_start(file_name: str = "shellui_debug.log"):
    logging.basicConfig(level=logging.DEBUG, filename=file_name, filemode="w",
                        format="%(asctime)s - %(levelname)s - %(filename)s : %(message)s\n")
