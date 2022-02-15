import logging
from typing import NoReturn


class LogMixin:
    """
    Эксперимент с миксином для логгирования
    """
    def __init__(self, name: str = ""):
        self._name = name if name else self.__class__.__name__
        self._log = logging.getLogger(self._name)

    def info(self, *args, **kwargs) -> NoReturn:
        self._log.info(*args, **kwargs)

    def debug(self, *args, **kwargs) -> NoReturn:
        self._log.debug(*args, **kwargs)
