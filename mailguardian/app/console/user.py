import rich
from sqlmodel import Session
from typing import Optional, Annotated
import typer
from mailguardian.app.auth.utils import validate_new_password, hash_password
from mailguardian.app.models.user import User
from mailguardian.app.schemas.user import UserRole
from mailguardian.database.connect import engine

app: typer.Typer = typer.Typer()

@app.command(name='createuser')
def create_user(email: Annotated[Optional[str], typer.Argument()]):
    password: str = typer.prompt(text='Enter password', hide_input=True)
    confirm_password: str = typer.prompt(text='Enter password again', hide_input=True)
    if not password == confirm_password:
        rich.print('[bold red]Passwords do not match[/bold red]')
        raise typer.Exit(code=1)
    validate_new_password(plain_password=password)
    user: User = User(email=email, password=hash_password(password=password), role=UserRole.USER)
    # raise typer.Exit(code=0)
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
    
    rich.print(f'[bold green]User {user} has been created[/bold green]')

@app.command(name='createadmin')
def create_user(email: Annotated[Optional[str], typer.Argument()]):
    password: str = typer.prompt(text='Enter password', hide_input=True)
    confirm_password: str = typer.prompt(text='Enter password again', hide_input=True)
    if not password == confirm_password:
        rich.print('[bold red]Passwords do not match[/bold red]')
        raise typer.Exit(code=1)
    validate_new_password(plain_password=password)
    user: User = User(email=email, password=hash_password(password=password), role=UserRole.SUPERUSER)
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
    
    rich.print(f'[bold green]Admin {user} has been created[/bold green]')