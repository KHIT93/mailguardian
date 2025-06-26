from typing import Annotated

import rich
import typer

from mailguardian.app import services
from mailguardian.app.auth.utils import hash_password, validate_new_password
from mailguardian.app.models.user import User
from mailguardian.app.schemas.user import UserRole
from mailguardian.database.connect import Database

app: typer.Typer = typer.Typer(name='user')


@app.command(name='createuser')
def create_user(email: Annotated[str | None, typer.Argument()]):
    password: str = typer.prompt(text='Enter password', hide_input=True)
    confirm_password: str = typer.prompt(text='Enter password again', hide_input=True)
    if not password == confirm_password:
        rich.print('[bold red]Passwords do not match[/bold red]')
        raise typer.Exit(code=1)
    validate_new_password(plain_password=password)
    user: User = User(email=email, password=hash_password(password=password), role=UserRole.USER)
    # raise typer.Exit(code=0)
    with services.get(Database).session_scope() as session:
        session.add(user)
        session.commit()
        session.refresh(user)

    rich.print(f'[bold green]User {user} has been created[/bold green]')


@app.command(name='createadmin')
def create_superuser(email: Annotated[str | None, typer.Argument()]):
    password: str = typer.prompt(text='Enter password', hide_input=True)
    confirm_password: str = typer.prompt(text='Enter password again', hide_input=True)
    if not password == confirm_password:
        rich.print('[bold red]Passwords do not match[/bold red]')
        raise typer.Exit(code=1)
    validate_new_password(plain_password=password)
    user: User = User(email=email, password=hash_password(password=password), role=UserRole.SUPERUSER)
    with services.get(Database).session_scope() as session:
        session.add(user)
        session.commit()
        session.refresh(user)

    rich.print(f'[bold green]Admin {user} has been created[/bold green]')
