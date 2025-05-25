from typing import Annotated

import invoke
import rich
from rich.progress import Progress, SpinnerColumn, TextColumn
import typer

from mailguardian.config.app import settings, FRONTEND_DIR

app: typer.Typer = typer.Typer()

@app.command(name='rebuild')
def rebuild(debug: Annotated[bool, typer.Option('--debug', help='Used to render detailed command output')] = False):
    if not settings.NUXT_BIN.is_file():
        rich.print('[bold][red]Nuxt is not installed in the frontend application. Please ensure that it is installed and try again![/red][/bold]')
        typer.Exit(1)
    if debug:
        result: invoke.Result = invoke.run(f'cd {FRONTEND_DIR} && {settings.NUXT_BIN} build', hide=False)
    else:
        with Progress(SpinnerColumn(), TextColumn('[progress.description]{task.description}'), transient=True) as progress:
            progress.add_task(description='Rebuilding client application...', total=None)
            result: invoke.Result = invoke.run(f'cd {FRONTEND_DIR} && {settings.NUXT_BIN} build', hide=True)
        rich.print('[bold][green]Client application has been successfully rebuilt[/green][/bold]')