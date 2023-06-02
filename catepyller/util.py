from abc import ABC
from functools import cache
from typing import Any, Protocol, TypeVar

T_contra = TypeVar("T_contra", contravariant=True)


class Wrapper(ABC):
    """
    Helper class to simplifying dataclasses designed to wrap a single `value`.
    """

    value: Any

    def simpleRepr(self) -> str:
        return f"{type(self).__qualname__}({self.value})"

    def __repr__(self) -> str:
        """
        Example
        -------
        >>> from dataclasses import dataclass
        >>> @dataclass(repr=False)
        ... class Example(Wrapper[int]):
        ...   value: int
        >>> Example(12)
        Example(12)

        (Instead of `Example(value=12)`)
        """
        return self.simpleRepr()


class Singleton:
    """
    Re-uses a singleton object in order to reduce memory usage ([source](https://python-patterns.guide/gang-of-four/singleton/#a-more-pythonic-implementation)).

    >>> Singleton() is Singleton()
    True
    """

    @cache  # type:ignore
    def __new__(cls):
        return object.__new__(cls)


class SupportsDunderLT(Protocol[T_contra]):
    def __lt__(self, __other: T_contra) -> bool:
        ...


class SupportsDunderGT(Protocol[T_contra]):
    def __gt__(self, __other: T_contra) -> bool:
        ...


SupportsComparison = SupportsDunderLT[Any] | SupportsDunderGT[Any]
