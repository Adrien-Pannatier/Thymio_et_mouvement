from asyncio import create_task, run, sleep
from pathlib import Path
from sys import version_info

import numpy as np
from pkg_resources import DistributionNotFound, parse_requirements, require
from rich.padding import Padding
from rich.panel import Panel
from tdmclient import ClientAsync

from app.big_brain import BigBrain
from app.config import DEBUG, PROCESS_MSG_INTERVAL, RAISE_DEPRECATION_WARNINGS
from app.context import Context
# from app.server import Server
from app.state import State
from app.utils.console import *
from app.utils.pool import Pool
from app.utils.types import Channel, Vec2

VERSION_MAJOR = 3
VERSION_MINOR = 10


def main():
    print_banner() # presentation banner

    if not check_version() or not check_requirements():
        return

    if RAISE_DEPRECATION_WARNINGS:
        np.warnings.filterwarnings(  # type: ignore
            "error", category=np.VisibleDeprecationWarning
        )

    try:
        run(init(), debug=DEBUG)

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
                "[bold white]Big Brain - Thymio Controller\n"
                + "Semester Project - Thymio organic movement\n"
                + "École Polytechnique Fédérale de Lausanne"
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


def check_requirements():
    """Check if the required packages are installed."""
    requirements = parse_requirements(Path("requirements.txt").open())

    not_met = []

    for requirement in requirements:
        try:
            require(str(requirement))
        except DistributionNotFound:
            not_met.append(str(requirement))

    if not_met != []:
        console.print(
            "\n".join(
                [
                    "[bold red]Requirements not met![/]",
                    "The following requirements are not met:\n",
                    *not_met,
                ]
            )
        )

        return False

    return True


async def init():
    info("Initializing...")
    await start()

async def start():
    """Start the application, instantiating the BigBrain."""

    brain = BigBrain()
    await brain.start_thinking()

if __name__ == "__main__":
    main()
