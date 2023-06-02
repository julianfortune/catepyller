from __future__ import annotations

import itertools
import typing
from abc import abstractmethod
from typing import Any, Callable, Iterable, TypeVar, overload

from catepyller.data.option import Option, Some

A = TypeVar("A")
B = TypeVar("B", contravariant=True)

# T = TypeVar("T")


# TODO: Maybe create ToIterable and FromIterable protocols?


class Sequence(typing.Sequence[A], typing.Collection[A], typing.Sized):
    """
    Similar to `typing.Sequence` but with more functionality.

    Must implement `get` and `__len__`.

    Note: Some of the mixin methods, such as __iter__(), __reversed__() and index(),
    make repeated calls to the underlying __getitem__() method. Consequently, if
    __getitem__() is implemented with constant access speed, the mixin methods will
    have linear performance; however, if the underlying method is linear (as it would
    be with a linked list), the mixins will have quadratic performance and will likely
    need to be overridden.
    """

    # ====== Abstract ======

    @classmethod
    @abstractmethod
    def from_iter(cls, iter: Iterable[A]) -> Sequence[A]:
        ...

    # TODO: Maybe rename this...?
    # - `at`
    # - `item` (F#)
    # - `nth` (F# ?)
    # - `index`
    # - `get` (Rust Vec)
    @abstractmethod
    def get(self, index: int) -> Option[A]:
        ...

    @property
    @abstractmethod
    def length(self) -> int:
        ...

    # ====== Concrete ======

    def get_slice(self, slice: slice) -> Option[Sequence[A]]:
        # TODO: Doesn't work correctly for `[::-1]`
        return Some(
            self.from_iter(
                self.get_unsafe(x)
                for x in range(
                    slice.start if slice.start is not None else 0,
                    slice.stop if slice.stop is not None else self.length,
                    slice.step if slice.step is not None else 1,
                )
            )
        )

    # --- Unsafe variants ---

    def get_unsafe(self, index: int) -> A:
        return self.get(index).unwrap_or_throw_unsafe(
            IndexError(f"Index ({index}) out of range")
        )

    def get_slice_unsafe(self, slice: slice) -> Sequence[A]:
        return self.get_slice(slice).unwrap_or_throw_unsafe(
            IndexError(f"Slice ({slice}) undefined")
        )

    # --- Interface to satisfy `Sequence` ---

    @overload
    def __getitem__(self, index: int) -> A:
        ...

    @overload
    def __getitem__(self, index: slice) -> Sequence[A]:
        ...

    def __getitem__(self, index: int | slice) -> A | Sequence[A]:
        if isinstance(index, slice):
            return self.get_slice_unsafe(index)

        assert isinstance(index, int)
        return self.get_unsafe(index)

    def __len__(self) -> int:
        return self.length
