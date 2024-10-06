import typer
from typing import List

# TODO: Find a way to automatically create the imports and build the dict below by using the filename as the key and the `app` variable within as the value

from .user import app as user_app
from .v2tov3 import app as v2tov3_app
from .maillog import app as maillog_app
from .scheduler import app as scheduler_app

commands: dict[str, typer.Typer] = {
    "user": user_app,
    'v2tov3': v2tov3_app,
    "maillog": maillog_app,
    'scheduler': scheduler_app,
}
