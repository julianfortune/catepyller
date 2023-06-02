from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional, TypeGuard, TypeVar

from catepyller.protocols import Monad
from catepyller.protocols.has_empty import SupportsEmpty
from catepyller.util import Singleton, Wrapper

A = TypeVar("A", covariant=True)
B = TypeVar("B", contravariant=True)

ValueT = TypeVar("ValueT")


class UnexpectedNothingException(Exception):
    pass


def unexpectedNothing(function: str) -> UnexpectedNothingException:
    return UnexpectedNothingException(
        f"Unexpectedly found `Nothing` in a call to '{function}'"
    )


class Option(Monad[A], SupportsEmpty[A]):
    """..."""

    # === STATIC ===

    empty = lambda: Nothing

    @staticmethod
    def from_optional(maybeValue: Optional[ValueT]) -> Option[ValueT]:
        if maybeValue is None:
            return Nothing
        return Some(maybeValue)

    @staticmethod
    def pure(value: ValueT) -> Some[ValueT]:
        return Some(value)

    # === INSTANCE ===

    def __bool__(self) -> TypeGuard[Some]:
        return isinstance(self, Some)

    def __len__(self) -> int:
        """
        >>> len(Some("?"))
        1
        >>> len(Nothing)
        0
        """
        return int(bool(self))

    # --- Declare typing for `Monad` methods ---

    def flat_map(self, f: Callable[[A], Option[B]]) -> Option[B]:
        if isinstance(self, Some):
            return f(self.value)
        else:
            return Nothing

    def map(self, f: Callable[[A], B]) -> Option[B]:
        return super().map(f)

    def apply(self, f: Option[Callable[[A], B]]) -> Option[B]:
        return super().apply(f)

    # --- Unwrapping ---

    def unwrap_or_throw_unsafe(self, e: Exception) -> A:
        if isinstance(self, Some):
            return self.value
        else:
            raise e

    def unwrap_unsafe(self) -> A:
        return self.unwrap_or_throw_unsafe(unexpectedNothing("unwrap_unsafe"))


@dataclass(frozen=True, repr=False)
class Some(Option[A], Wrapper):
    value: A


@dataclass(frozen=True, init=False, repr=False)
class NothingType(Option[A], Singleton):
    """
    Represents the absence of a value.
    """

    def __repr__(self) -> str:
        return "Nothing"


Nothing: NothingType = NothingType()
