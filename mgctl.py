#! /usr/bin/env python3

import typer

from mailguardian.app import commands

app: typer.Typer = typer.Typer()

for command in commands:
    app.add_typer(typer_instance=command)


if __name__ == '__main__':
    # print(commands)
    # print(app.registered_commands)
    app()
