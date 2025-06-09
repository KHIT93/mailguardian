from fastapi import APIRouter
from injector import Injector
from typer import Typer

from mailguardian.config.app import settings
from mailguardian.config.logging import setup_logging
from mailguardian.framework import setup_service_container
from mailguardian.app.bootstrap.routes import register_web_routes, register_api_routes
from mailguardian.app.bootstrap.cli import register_cli_routes
from . import models
from . import exceptions

# Configure logging
logger = setup_logging(log_level=settings.APP_LOGLEVEL, log_output='default', log_dir=settings.APP_LOGDIR if settings.APP_LOG_TO_FILE else None)

# Configure Dependency Injection
services: Injector = setup_service_container()

# Configure Web Routes
web_routes: list = register_web_routes()

# Configure API Routes
api_routes: list[APIRouter] = register_api_routes()

# Configure Console Commands
commands: list[Typer] = register_cli_routes()