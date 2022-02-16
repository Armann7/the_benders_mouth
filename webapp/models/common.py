"""
Модели, которые не стоит выделять отдельно
"""
from enum import Enum


class Version(str, Enum):
    """
    Версия API
    """
    V1 = "v1"
