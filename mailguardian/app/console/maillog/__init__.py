import typer
from . import milter
from . import postfix
from . import mailscanner

app: typer.Typer = typer.Typer()

app.add_typer(typer_instance=milter.app, name='milter')
app.add_typer(typer_instance=postfix.app, name='postfix')
app.add_typer(typer_instance=mailscanner.app, name='mailscanner')