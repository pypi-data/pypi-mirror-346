# mypy: disable-error-code="explicit-any"
"""This module implements a simple-to-use decorator to implement the singleton pattern.

Exports:

- r_singleton: resettable singleton wrapper
- singleton: ignores the arguments to the constructor on subsequent calls
- singleton_argenforce: raises a ValueError if the arguments on subsequent
    calls vary from the initial ones.
"""

import functools
import threading
from typing import Any, Dict, Generic, Tuple, Type, TypeVar

T = TypeVar("T")  # noqa: WPS111


class _ResettableWrapper(Generic[T]):
    def __init__(self, cls: Type[T]):  # noqa: WPS117
        self._cls = cls
        self._instance: T | None = None
        self._lock = threading.Lock()
        functools.update_wrapper(self, cls)

    def __call__(self, *args, **kwargs) -> T:
        # Double-checked locking pattern
        if self._instance is None:
            with self._lock:
                if self._instance is None:
                    self._instance = self._cls(*args, **kwargs)
        return self._instance

    def reset(self):
        with self._lock:
            self._instance = None


class _SingletonWrapper(Generic[T]):

    _instance: T | None
    _args: Tuple[Any, ...]
    _kwargs: Dict[str, Any]

    def __init__(self, cls: Type[T]) -> None:  # noqa: WPS117
        self.__wrapped__: Type[T]
        functools.update_wrapper(self, cls)

        self._instance = None
        self._args = ()
        self._kwargs = {}

    def __call__(self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> T:
        if self._instance is None:  # Create the instance
            self._args = args
            self._kwargs = kwargs
            self._instance = self.__wrapped__(*args, **kwargs)
        return self._instance


class _ArgEnforceSingletonWrapper(_SingletonWrapper[T]):
    def __init__(self, cls: Type[T]) -> None:  # noqa: WPS117
        super().__init__(cls)
        self._instances: Dict[Tuple[T], T] = {}

    def __call__(self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> T:
        if self._instance is not None and (
            args != self._args or kwargs != self._kwargs
        ):
            raise ValueError("Singleton called with different arguments.")
        return super().__call__(*args, **kwargs)


def r_singleton(cls: Type[T]) -> _ResettableWrapper[T]:
    """Use this decorator to wrap a class to make it a resettable singleton.

    The first time the wrapped class is instantiated, it will create an object
    with those arguments and store it. Every subsequent instantiation will return
    the stored object, regardless of the provided parameters. The stored object
    can be reset to None by calling the `reset` method.

    Args:
        cls (Type[T]): The class to make a singleton

    Returns:
        _ResettableWrapper[T]: The singleton-wrapped class
    """
    return _ResettableWrapper(cls)


def singleton(cls: Type[T]) -> _SingletonWrapper[T]:
    """Use this decorator to wrap a class to make it a singleton.

    The first time the wrapped class is instantiated, it will create an object
    with those arguments and store it. Every subsequent instantiation will return
    the stored object, regardless of the provided parameters.

    Args:
        cls (Type[T]): The class to make a singleton

    Returns:
        _SingletonWrapper[T]: The singleton-wrapped class
    """
    return _SingletonWrapper(cls)


def singleton_argenforce(cls: Type[T]) -> _ArgEnforceSingletonWrapper[T]:
    """Use this decorator to wrap a class to make it an arg-enforce singleton.

    The first time the wrapped class is instantiated, it will create an object
    with those arguments and store it. Every subsequent instantiation will return
    the stored object, unless the arguments are different than the first call,
    in which case a ValueError will be thrown.

    Args:
        cls (Type[T]): The class to make a singleton

    Returns:
        _ArgEnforceSingletonWrapper[T]: The singleton-wrapped class
    """
    return _ArgEnforceSingletonWrapper(cls)
