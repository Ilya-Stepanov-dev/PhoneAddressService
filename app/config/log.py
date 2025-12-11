import logging
import sys
from logging.config import dictConfig
from pathlib import Path

from .config import service_config

log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": service_config.APP_LOG_LEVEL,
            "formatter": "simple",
            "stream": sys.stdout,
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": service_config.APP_LOG_LEVEL,
            "formatter": "detailed",
            "filename": "logs/app.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "encoding": "utf8",
        },
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "formatter": "detailed",
            "filename": "logs/error.log",
            "maxBytes": 5242880,  # 5MB
            "backupCount": 3,
            "encoding": "utf8",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "file", "error_file"],
            "level": "INFO",
        },
        "uvicorn": {
            "handlers": ["console", "file"],
            "level": service_config.APP_LOG_LEVEL,
            "propagate": False,
        },
        "app": {
            "handlers": ["console", "file", "error_file"],
            "level": service_config.APP_LOG_LEVEL,
            "propagate": False,
        },
    },
}


def setup_logging():
    """Инициализация логирования"""
    dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger("app")
    logger.info("Logging initialized")
    return logger
