from __future__ import annotations

from operator import add
from typing import Any, Callable, TypeVar, overload

from catepyller.data.list import List
from catepyller.data.option import NothingType, Option, Some
from catepyller.protocols.semigroup import SupportsAdd

A = TypeVar("A", covariant=True, bound=SupportsAdd)


# fmt: off
@overload
def combine(this: Option[A], other: Option[A]) -> Option[A]:...
@overload
def combine(
    this: Option[A], other: Option[A], combineF: Callable[[A, A], A]
) -> Option[A]:...

@overload
def combine(this: List[A], other: List[A]) -> List[A]: ...
@overload
def combine(
    this: List[A], other: List[A], combineF: Callable[[A, A], A]
) -> List[A]: ...

@overload
def combine(this: list[A], other: list[A]) -> list[A]: ...
@overload
def combine(
    this: list[A], other: list[A], combineF: Callable[[A, A], A]
) -> list[A]: ...

@overload
def combine(this: tuple[A, ...], other: tuple[A, ...]) -> tuple[A, ...]: ...
@overload
def combine(
    this: tuple[A, ...], other: tuple[A, ...], combineF: Callable[[A, A], A]
) -> tuple[A, ...]: ...

@overload
def combine(this: set[A], other: set[A]) -> set[A]: ...
@overload
def combine(this: set[A], other: set[A], combineF: Callable[[A, A], A]) -> set[A]: ...
# fmt: on


def combine(
    this: Any[A],
    other: Any[A],
    combineF: Callable[[A, A], A] = add,
) -> Any[A]:
    if isinstance(this, Option) and isinstance(other, Option):
        return _combineOption(this, other, combineF)
    elif isinstance(this, List) and isinstance(other, List):
        # TODO: ...
        raise NotImplementedError()
    elif isinstance(this, set) and isinstance(other, set):
        return this.union(other)
    else:  # `set` and `list`
        return this + other


def _combineOption(
    this: Option[A],
    other: Option[A],
    combineF: Callable[[A, A], A] = add,
) -> Option[A]:
    if isinstance(this, Some) and isinstance(other, Some):
        return Some(combineF(this.value, other.value))
    else:
        if isinstance(this, NothingType):
            return other
        else:  # `other` is `Nothing``
            return this
