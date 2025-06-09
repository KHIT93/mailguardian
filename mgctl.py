#! /usr/bin/env python3

from injector import Injector
import typer

from mailguardian.app import commands
# from mailguardian.app.console import commands
from mailguardian.config.app import API_VERSION, settings

app: typer.Typer = typer.Typer()

for command in commands:
    app.add_typer(typer_instance=command)


if __name__ == '__main__':
    # print(commands)
    # print(app.registered_commands)
    app()
