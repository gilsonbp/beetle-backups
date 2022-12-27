import sys
from logging.config import dictConfig

from newrelic import agent

from src.config import settings

agent.initialize()


def configure_logging() -> None:
    dictConfig(  # NOSONAR
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "correlation_id": {
                    "()": "asgi_correlation_id.CorrelationIdFilter",
                    "uuid_length": 36,
                },
                "celery_tracing": {
                    "()": "asgi_correlation_id.CeleryTracingIdsFilter",
                    "uuid_length": 36,
                },
            },
            "formatters": {
                "console": {
                    "class": "logging.Formatter",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                    "format": "%(levelname)s:\t\b%(asctime)s "
                    "%(name)s:%(lineno)d "
                    "[%(correlation_id)s] %(message)s",
                },
                "celery": {
                    "class": "logging.Formatter",
                    "datefmt": "%H:%M:%S",
                    "format": "%(levelname)s:\t\b[%(correlation_id)s] "
                    "[%(celery_parent_id)s-%(celery_current_id)s] "
                    "%(name)s %(message)s",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "filters": ["correlation_id"],
                    "formatter": "console",
                },
                "celery": {
                    "class": "logging.StreamHandler",
                    "filters": ["correlation_id", "celery_tracing"],
                    "formatter": "celery",
                },
            },
            "loggers": {
                "root": {
                    "handlers": [
                        "celery"
                        if any("celery" in i for i in sys.argv)
                        else "console"
                    ],
                    "level": settings.LOG_LEVEL,
                    "propagate": True,
                },
                "app": {
                    "handlers": ["console"],
                    "level": settings.LOG_LEVEL,
                    "propagate": True,
                },
                "databases": {
                    "handlers": ["console"],
                    "level": settings.LOG_LEVEL,
                },
                "httpx": {
                    "handlers": ["console"],
                    "level": settings.LOG_LEVEL,
                },
                "asgi_correlation_id": {
                    "handlers": ["console"],
                    "level": settings.LOG_LEVEL,
                },
            },
        }
    )
