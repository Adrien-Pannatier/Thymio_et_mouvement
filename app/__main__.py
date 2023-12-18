import sys, os

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

    # build paths
    if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app 
    # path into variable _MEIPASS'.
        application_path = os.path.dirname(sys.executable)
        # remove the "dist" folder and the executable name
        application_path = os.path.dirname(application_path)
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    debug(f"Application path: {application_path}")
    if not check_version(): # check if the Python version is supported
        return

    if RAISE_DEPRECATION_WARNINGS:
        np.warnings.filterwarnings(  # type: ignore
            "error", category=np.VisibleDeprecationWarning
        )

    try:
        init(application_path)

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
    (major, minor, _, _, _) = sys.version_info

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

def init(application_path):
    info("Initializing...")
    start(application_path)

def start(application_path):
    """Start the application, instantiating the BigBrain."""

    brain = BigBrain(application_path)
    brain.start_thinking()
    

if __name__ == "__main__":
    main()
    try:
        sys.exit()
    except Exception as e:
        print(e)