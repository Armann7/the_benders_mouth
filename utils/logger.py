"""
Встраиваемое логгирование
"""
import logging


class LogMixin:
    """
    Эксперимент с миксином
    """
    def __init__(self, name: str = ""):
        """
        :param name: наименование журнала
        """
        self._name = name if name else self.__class__.__name__
        self._log = logging.getLogger(self._name)

    def info(self, *args, **kwargs):
        """
        Прокси
        """
        self._log.info(*args, **kwargs)

    def debug(self, *args, **kwargs):
        """
        Прокси
        """
        self._log.debug(*args, **kwargs)
