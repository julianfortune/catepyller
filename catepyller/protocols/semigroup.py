from __future__ import annotations

from typing import Protocol, TypeVar

T = TypeVar("T", bound="SupportsAdd")


class SupportsAdd(Protocol):
    """
    Approximation for Semigroup based around the plus operator.

    numeric -> addition
    string/list/tuple -> concatenation
    bool -> int(a) + int(b) -- super weird ???
    """

    def __add__(self: T, other: T):
        ...


S = TypeVar("S", bound="Semigroup")


class Semigroup(SupportsAdd):
    """More ergonomic interface"""
    def combine(self: S, other: S):
        ...

    def __add__(self: S, other: S):
        self.combine(other)
