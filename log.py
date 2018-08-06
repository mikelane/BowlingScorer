import logging.config
import os


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(__name__)

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '{levelname} {asctime} | {message}',
                'datefmt': '%Y-%m-%d %H:%M:%S',
                'style': '{'
            }
        },
        'handlers': {
            'default': {
                'level': os.environ.get('LOG_LEVEL', 'INFO'),
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            '': {
                'handlers': ['default'],
                'level': os.environ.get('LOG_LEVEL', 'INFO'),
                'propagate': True
            },
        }
    }

    logging.config.dictConfig(LOGGING)
    return logger