import logging
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
LOG_BASE_DIR = os.path.join(BASE_DIR, "logs")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"format": "%(asctime)s - [%(levelname)s] - %(message)s"},
        "verbose": {
            "format": "%(asctime)s - [%(levelname)s] - %(pathname)s:%(lineno)d - %(module)s - %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple", # 项目下所有日志的标准输出会受此配置影响
        },
        "debug": {
            "level": "DEBUG",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "when": "midnight",
            "utc": False,
            "backupCount": 3,
            "filename": os.path.join(LOG_BASE_DIR, "debug.log"),
            "formatter": "verbose",
        },
        "info": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "when": "midnight",
            "utc": False,
            "backupCount": 90,
            "filename": os.path.join(LOG_BASE_DIR, "info.log"),
            "formatter": "simple",
        },
        "warning": {
            "level": "WARNING",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "when": "midnight",
            "utc": False,
            "backupCount": 90,
            "filename": os.path.join(LOG_BASE_DIR, "warning.log"),
            "formatter": "verbose",
        },
        "error": {
            "level": "ERROR",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "when": "midnight",
            "utc": False,
            "backupCount": 90,
            "filename": os.path.join(LOG_BASE_DIR, "error.log"),
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console", "debug", "info", "warning", "error"],
        "level": os.getenv("DJANGO_LOG_LEVEL", "DEBUG"),
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            # True to disable any other loggers than the root logger
            # True 会将 Console 日志写入日志文件, 不要与 DEBUG 等级同时开启，否则会写入大量无用日志
            "propagate": True,
        },
    },
}
