from setuptools import setup, find_packages
from src.shellui import __version__, __author__, __email__, __license__
import pathlib, sys

HERE = pathlib.Path(__file__).parent
long_description = (HERE / "README.MD").read_text()

win_requirements = []
if sys.platform.startswith("win"):
    win_requirements.append("windows-curses>=2.3.3")


setup(
    name="shellui",
    version=__version__,
    author=__author__,
    author_email=__email__,
    description="library simplifies the creation of TUI (Text User Interface) in the terminal. Offers a clean and intuitive architecture to help you build interactive applications effortlessly.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/highofolly/shellui",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={"": ["README.MD"]},
    license=__license__,
    license_files=("LICENSE", ),
    install_requires=open("requirements.txt").read().splitlines() + win_requirements,
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
)