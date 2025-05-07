from .tools import LoggingTools, CaptureLogs
from .loggers import LoggerOverseer, LoggerFactory
from .timber import Timber


import logging
class LogLevel:
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL