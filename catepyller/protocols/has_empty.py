from __future__ import annotations

from typing import Any, Protocol, Type, TypeVar

A = TypeVar("A", covariant=True)

S = TypeVar("S", bound="SupportsDefault")


class SupportsDefault(Protocol):
    """
    Weaker version of `Monoid`
    """

    @classmethod
    def default(cls: Type[S]) -> S:
        ...


class SupportsEmpty(Protocol[A]):
    """
    Weaker version of `MonoidK`

    NOTE: `NonEmptyList` cannot satisfy `SupportsEmpty`
    """

    # NOTE: Assumes we don't need `A` to be a `Monoid`
    @staticmethod
    def empty() -> SupportsEmpty[Any]:
        ...
