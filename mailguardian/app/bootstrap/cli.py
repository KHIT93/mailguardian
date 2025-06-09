from importlib import import_module
from pathlib import Path

from mailguardian.config.app import settings

def register_cli_routes() -> list:
    routes: list = []
    for module in Path(settings.COMMANDS).iterdir():
        python_module = None
        try:
            module_name: str = module.name.replace('.py', '')
            python_module = import_module(f'mailguardian.app.console.{module_name}')
        except ImportError:
            continue
        if hasattr(python_module, 'app'):
            routes.append(python_module.app)
    return routes

