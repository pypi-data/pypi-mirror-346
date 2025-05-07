import logging

from holytools.logging import LoggerFactory


class Timber:
    def __init__(self):
        self.logger = LoggerFactory.get_logger(name=self.__class__.__name__)

    def log(self, msg : str, level : int = logging.INFO):
        self.logger.log(level=level, msg=msg)

    def warning(self, msg : str, *args, **kwargs):
        kwargs['level'] = logging.WARNING
        self.logger.log(msg=msg, *args, **kwargs)

    def error(self, msg : str, *args, **kwargs):
        kwargs['level'] = logging.ERROR
        self.logger.log(msg=msg, *args, **kwargs)

    def critical(self, msg : str, *args, **kwargs):
        kwargs['level'] = logging.CRITICAL
        self.logger.log(msg=msg, *args, **kwargs)

    def info(self, msg : str, *args, **kwargs):
        kwargs['level'] = logging.INFO
        self.logger.log(msg=msg, *args, **kwargs)



