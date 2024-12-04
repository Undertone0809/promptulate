"""The singleton metaclass for ensuring only one instance of a class."""

import abc
import logging

logger = logging.getLogger(__name__)


class Singleton(abc.ABCMeta, type):
    """
    Singleton metaclass for ensuring only one instance of a class.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Call method for the singleton metaclass."""
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class AbstractSingleton(abc.ABC, metaclass=Singleton):
    """
    Abstract singleton class for ensuring only one instance of a class.
    """

    pass


class SingletonPool(metaclass=Singleton):
    """Storing classes which cannot use metaclass=Singleton due to implement
    BaseModel."""

    def __init__(self):
        self.instances = {}


def singleton():
    """singleton decorator"""

    def decorator(cls):
        singleton_pool = SingletonPool()

        def get_instance():
            if cls not in singleton_pool.instances:
                singleton_pool.instances[cls] = cls()
                logger.debug(f"[pne config] class <{cls.__name__}> initialization")
            return singleton_pool.instances[cls]

        return get_instance

    return decorator
