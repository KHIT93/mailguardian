import typer

from . import mailscanner, milter, postfix

app: typer.Typer = typer.Typer(name='maillog')

app.add_typer(typer_instance=milter.app, name='milter')
app.add_typer(typer_instance=postfix.app, name='postfix')
app.add_typer(typer_instance=mailscanner.app, name='mailscanner')
