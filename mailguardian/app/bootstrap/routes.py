import traceback
from importlib import import_module
from pathlib import Path

from mailguardian.config.app import settings


def register_web_routes() -> list:
    routes: list = []
    for module in Path(settings.ROUTES, 'web').iterdir():
        pass
    return routes


def register_api_routes() -> list:
    routes: list = []
    for module in Path(settings.ROUTES, 'api').iterdir():
        python_module = None
        try:
            module_name: str = module.name.replace('.py', '')
            python_module = import_module(f'mailguardian.routes.api.{module_name}')
        except ImportError:
            continue
        if hasattr(python_module, 'router'):
            routes.append(python_module.router)
    return routes
