from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from typing import Any, Callable, Generic, TypeVar, Union

from typing_extensions import TypeGuard

from catepyller.protocols.context_2 import Monad2
from catepyller.util import Wrapper

A = TypeVar("A", covariant=True)
B = TypeVar("B", covariant=True)

C = TypeVar("C", contravariant=True)

T = TypeVar("T")


class Result(Monad2[A, B], Generic[A, B], ABC):
    @staticmethod
    def pure(a: T) -> Result[T, Any]:
        return Success(a)


@dataclass(frozen=True)
class Success(Result[A, B], Wrapper):
    value: A

    def flat_map(self, f: Callable[[A], Result[C, B]]) -> Result[C, B]:
        return f(self.value)


@dataclass(frozen=True)
class Failure(Result[A, B], Wrapper):
    value: B

    def flat_map(self, f: Callable[[A], Result[C, B]]) -> Result[C, B]:
        return Failure(self.value)


def is_success(r: Result[A, B]) -> TypeGuard[Success[A, B]]:
    """
    Using `TypeGuard` tells the static type checker that for a given function:

        1. The return value is a boolean.
        2. If the return value is True, the type of its argument is the type inside TypeGuard.

    Can also do `if type(r) is Success` directly and MyPy will narrow.
    """
    return type(r) is Success
