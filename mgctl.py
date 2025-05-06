#! /usr/bin/env python3

from contextlib import asynccontextmanager

import typer
from fastapi import FastAPI

from mailguardian.app.console import commands
from mailguardian.app.http.middleware import middleware as http_middleware
from mailguardian.config.app import API_VERSION, settings
from mailguardian.config.logging import (
    enable_logfile,
    enable_stdout_logging,
    init_logger,
)

# Application bootstrapping
# TODO: See if we can move this to separate python module and then simply import it here


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
    # On Startup
    # init_logger(level=settings.APP_LOGLEVEL)
    # if settings.APP_LOGFILE and settings.APP_LOG_TO_FILE:
    #     enable_logfile(filename=settings.APP_LOGFILE)
    # else:
    #     enable_stdout_logging()

    yield


api = FastAPI(
    title='MailGuardian',
    lifespan=lifespan,
    version=API_VERSION,
    root_path=settings.API_ROOT,
    responses={
        401: {"description": "Unauthorized"},
        404: {"description": "Not found"},
    },
    middleware=http_middleware
)

app: typer.Typer = typer.Typer()

for command in commands.keys():
    app.add_typer(typer_instance=commands[command], name=command)


if __name__ == '__main__':
    # init_logger(level=settings.APP_LOGLEVEL)
    # if settings.APP_LOGFILE and settings.APP_LOG_TO_FILE:
    #     enable_logfile(filename=settings.APP_LOGFILE)
    # else:
    #     enable_stdout_logging()
    app()
