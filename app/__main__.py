from sys import version_info, exit

import numpy as np
from rich.padding import Padding
from rich.panel import Panel

from app.big_brain import BigBrain
from app.config import RAISE_DEPRECATION_WARNINGS
from app.utils.console import *

VERSION_MAJOR = 3
VERSION_MINOR = 10


def main():
    print_banner() # presentation banner

    if not check_version(): # check if the Python version is supported
        return

    if RAISE_DEPRECATION_WARNINGS:
        np.warnings.filterwarnings(  # type: ignore
            "error", category=np.VisibleDeprecationWarning
        )

    try:
        init()

    except KeyboardInterrupt:
        warning("Interrupted by user")

    except Exception:
        critical("Program crashed")
        console.print_exception()

    finally:
        print("")
    

def print_banner():
    """Print the presentation banner."""
    console.print(
        Padding(
            Panel(
                "Semester Project - Thymio organic movement\n"
                + "École Polytechnique Fédérale de Lausanne\n"
                + "date: 2023-12-13\n"
                + "Author: Adrien Pannatier\n"
            ),
            (1, 2),
        ),
        justify="left",
    )


def check_version():
    """Check if the Python version is supported."""
    (major, minor, _, _, _) = version_info

    if major < VERSION_MAJOR or minor < VERSION_MINOR:
        console.print(
            "\n".join(
                [
                    "[bold red]Python version not supported![/]",
                    f"This project uses features from Python {VERSION_MAJOR}.{VERSION_MINOR}",
                    f"You have version {major}.{minor}\n",
                ]
            )
        )

        return False

    return True

def init():
    info("Initializing...")
    start()

def start():
    """Start the application, instantiating the BigBrain."""

    brain = BigBrain()
    brain.start_thinking()
    

if __name__ == "__main__":
    main()
    try:
        exit()
    except Exception as e:
        print(e)