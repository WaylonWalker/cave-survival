# SPDX-FileCopyrightText: 2023-present Waylon S. Walker <waylon@waylonwalker.com>
#
# SPDX-License-Identifier: MIT
import debugpy
import typer

from cave_survival.console import console
from cave_survival.run import run

from ..__about__ import __version__, name


def version_callback(value: bool) -> None:
    if value:
        console.print(f"{__version__}")
        raise typer.Exit()


app = typer.Typer(
    name=name,
    help="A cave survival game",
)


@app.callback(invoke_without_command=True)
def main(
    version: bool = typer.Option(
        False,
        "--version",
        callback=version_callback,  # is_eager=True
    ),
    debug: bool = typer.Option(None, "--debug", help="start with debug mode running"),
) -> None:
    if debug:
        print("debugging")
        debugpy.listen(("localhost", 5678))
        print("waiting...")
        debugpy.wait_for_client()

    run()
    # Do other global stuff, handle other global options here
    return
