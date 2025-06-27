#! /usr/bin/env python3

import typer

from mailguardian.app.bootstrap.cli import register_cli_routes

# from mailguardian.app import commands

app: typer.Typer = typer.Typer()

# Configure Console Commands
commands: list[typer.Typer] = register_cli_routes()

for command in commands:
    app.add_typer(typer_instance=command)


if __name__ == '__main__':
    # print(commands)
    # print(app.registered_commands)
    app()
