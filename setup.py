from setuptools import setup, find_packages
from src.shellui import __version__, __author__, __email__, __license__

setup(
    name="shellui",
    version=__version__,
    author=__author__,
    author_email=__email__,
    description="library simplifies the creation of TUI (Text User Interface) in the terminal. Offers a clean and intuitive architecture to help you build interactive applications effortlessly.",
    long_description=open("README.MD").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/highofolly/shellui",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    license=__license__,
    install_requires=open("requirements.txt").read().splitlines(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
)