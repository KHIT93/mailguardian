import inspect
from collections.abc import Callable
from functools import wraps
from typing import (
    Annotated,
    Any,
    TypeVar,
    get_args,
    get_origin,
    get_type_hints,
)

from injector import Injector

from mailguardian.app.service_providers.service_container import services

# Type variable for decorated functions
F = TypeVar('F', bound=Callable[..., Any])


class Depends:  # noqa: B903
    """Marker class to indicate a dependency, similar to FastAPI's Depends"""
    def __init__(self, dependency: Callable[..., Any] = None):
        self.dependency = dependency


def _extract_depends_from_annotation(annotation):
    """
    Extract Depends instance from type annotation.
    Handles Annotated[Type, Depends(...)] syntax.
    """
    # Check if it's an Annotated type
    if get_origin(annotation) is Annotated:
        args = get_args(annotation)
        if len(args) >= 2:
            # First arg is the actual type, rest are metadata
            actual_type = args[0]
            metadata = args[1:]

            # Look for Depends in metadata
            for meta in metadata:
                if isinstance(meta, Depends):
                    return actual_type, meta

            # If no Depends found in metadata, return type for auto-injection
            return actual_type, None

    # For non-Annotated types, return as-is for potential auto-injection
    return annotation, None


def inject_dependencies(injector: Injector = None):
    """
    Decorator to inject dependencies into standalone functions.
    Supports both Annotated[Type, Depends(...)] and regular type hints.

    Args:
        injector: Optional injector instance. If None, a default one will be created.
    """
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get the injector instance
            active_injector = injector or services

            # Get function signature and type hints
            sig = inspect.signature(func)
            type_hints = get_type_hints(func, include_extras=True)

            # Process parameters and inject dependencies
            bound_args = sig.bind_partial(*args, **kwargs)
            bound_args.apply_defaults()

            for param_name, param in sig.parameters.items():
                # Skip if already provided
                if param_name in bound_args.arguments:
                    continue

                # Get type annotation if available
                if param_name in type_hints:
                    annotation = type_hints[param_name]
                    actual_type, depends_info = _extract_depends_from_annotation(annotation)

                    if depends_info is not None:
                        # Has explicit Depends annotation
                        dependency = depends_info.dependency or actual_type
                        bound_args.arguments[param_name] = active_injector.get(dependency)
                    elif param.default == param.empty:
                        # Auto-inject based on type hint if no default value
                        try:
                            bound_args.arguments[param_name] = active_injector.get(actual_type)
                        except Exception:
                            # If injection fails and no default, let the function handle it
                            pass

                # Fallback: check if parameter has Depends as default value (old style)
                elif param.default and isinstance(param.default, Depends):
                    dependency = param.default.dependency
                    if dependency is None:
                        raise ValueError(f"Cannot resolve dependency for parameter '{param_name}'")
                    bound_args.arguments[param_name] = active_injector.get(dependency)

            return func(**bound_args.arguments)

        return wrapper
    return decorator
