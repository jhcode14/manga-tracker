import logging.config
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(name)s %(levelname)s %(message)s",
        },
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": (
                "standard"
                if os.getenv("LOG_FORMAT", "standard") == "standard"
                else "json"
            ),
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "": {  # Root logger
            "handlers": ["console"],
            "level": LOG_LEVEL,
        },
        "werkzeug": {  # Flask's logger
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "sqlalchemy": {  # SQLAlchemy's logger
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}
