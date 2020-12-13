"""
Ensure a class only has one instance, and provide a global point of
access to it.
"""
from weakref import WeakValueDictionary


class Singleton(type):
    """
    Define an Instance operation that lets clients access its unique
    instance.
    """

    _instances = WeakValueDictionary()

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls._instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            # This variable declaration is required to force a
            # strong reference on the instance.
            instance = super(Singleton, cls).__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
