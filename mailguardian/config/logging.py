import logging
import logging.config
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Literal, Optional, Union

LogLevelType = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
LogOutputFormat = Literal["default", "json"]

def setup_logging(log_level: Union[LogLevelType, str] = 'INFO', log_output: Union[LogOutputFormat, str] = 'default', log_dir: Union[str, Path] = None) -> logging.Logger:
    """
    Set up logging configuration for the application
    
    Args:
        log_level: The logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_level: The logging outoput format (default, json)
        log_dir: Directory to store log files
        
    Returns:
        The configured logger for the application
    """
    handlers_to_apply: list[str] = []
    handlers: dict = {}
    if log_dir is not None:
        today: str = datetime.now().strftime("%Y-%m-%d")
        Path(log_dir).mkdir(exist_ok=True)
        # Generate log filename with current date
        log_file: str = f"{log_dir}/{today}.log"

        handlers_to_apply.append('file')
        handlers['file'] = {
            "class": "logging.handlers.RotatingFileHandler",
            "level": log_level,
            "formatter": log_output,
            "filename": log_file,
            "maxBytes": 10485760,  # 10 MB
            "backupCount": 10,
            "encoding": "utf8",
        }
    else:
        handlers_to_apply.append('console')
        handlers['console'] = {
            "class": "logging.StreamHandler",
            "level": log_level,
            "formatter": log_output,
            "stream": sys.stdout,
        }

    # Logging configuration dictionary
    config: dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s %(process)d %(levelname)s %(name)s %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "simple": {
                "format": "%(asctime)s %(process)d %(levelname)s %(name)s %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "json": {
                "format": '{ "timestamp": "%(asctime)s", "process": "%(process)d", "severity": "%(levelname)s", "module": "%(name)s", "message": "%(message)s" }',
                "datefmt": "%Y-%m-%d %H:%M:%S",
            }
        },
        "handlers": handlers,
        "loggers": {
            "mailguardian": {  # Application logger
                "level": log_level,
                "handlers": handlers_to_apply,
                "propagate": False,
            },
            "fastapi": {  # FastAPI logger
                "level": log_level,
                "handlers": handlers_to_apply,
                "propagate": False,
            },
            "uvicorn": {  # Uvicorn logger
                "level": log_level,
                "handlers": handlers_to_apply,
                "propagate": False,
            },
            "uvicorn.access": {  # Uvicorn access logger
                "level": log_level,
                "handlers": handlers_to_apply,
                "propagate": False,
            },
            "uvicorn.error": {  # Uvicorn error logger
                "level": log_level,
                "handlers": handlers_to_apply,
                "propagate": False,
            },
            "sqlalchemy.engine": {  # SQLAlchemy engine logger (SQL queries)
                "level": "WARNING",  # Set to DEBUG to log all SQL queries
                "handlers": handlers_to_apply,
                "propagate": False,
            },
        },
        "root": {  # Root logger
            "level": log_level,
            "handlers": handlers_to_apply,
        },
    }

    # Apply the configuration
    logging.config.dictConfig(config)
    
    # Return a logger for the application
    return logging.getLogger("mailguardian")