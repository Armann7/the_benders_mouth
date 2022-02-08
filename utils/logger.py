import logging


class LogMixin:
    def __init__(self, name: str = ""):
        self._name = name if name else self.__class__.__name__
        self._log = logging.getLogger(self._name)

    def info(self, *args, **kwargs):
        self._log.info(*args, **kwargs)

    def debug(self, *args, **kwargs):
        self._log.debug(*args, **kwargs)
