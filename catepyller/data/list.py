from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable, TypeVar, final

from catepyller.data.option import Nothing, Option, Some
from catepyller.protocols import Monad
from catepyller.protocols.has_empty import SupportsEmpty
from catepyller.util import Singleton, SupportsComparison

A = TypeVar("A")
B = TypeVar("B", contravariant=True)

T = TypeVar("T")
C = TypeVar("C", bound=SupportsComparison)


class UnexpectedNilError(ValueError):
    pass


class List(Monad[A], SupportsEmpty[A]):
    # TODO: Should this conform to Sequence[A] ? or maybe just Iterable[A]

    # === STATIC ===

    @staticmethod
    def of(head: T, *args: T) -> Elem[T]:
        """
        >>> List.of(1, 2, 3)
        1 :: 2 :: 3 :: Nil
        """
        return Elem(head, List.from_iter(args))

    @staticmethod
    def from_iter(iterable: Iterable[T]) -> List[T]:
        """
        >>> List.from_iter([1, 2, 3])
        1 :: 2 :: 3 :: Nil
        """
        new_list: List = Nil
        for elem in reversed(list(iterable)):
            new_list = Elem(elem, new_list)

        return new_list

    @staticmethod
    def empty() -> List[Any]:
        """
        >>> List.empty()
        Nil
        """
        return Nil

    @staticmethod
    def pure(value: T) -> Any[T]:
        """
        >>> List.pure(1)
        1 :: Nil
        """
        return List.of(value)

    @staticmethod
    def sorted(lst: List[C]) -> List[C]:
        raise NotImplementedError

    # === INSTANCE ===

    # --- `Monad` methods ---

    def flat_map(self, f: Callable[[A], List[B]]) -> List[B]:
        if isinstance(self, Elem):
            return f(self.value).extend(self.following.flat_map(f))
        else:
            return Nil

    def map(self, f: Callable[[A], B]) -> List[B]:
        return super().map(f)

    def apply(self, f: List[Callable[[A], B]]) -> List[B]:
        return super().apply(f)

    # ---

    # >>> Not O(1) :(

    # @property
    # def length(self) -> int:
    #     if isinstance(self, Elem):
    #         return 1 + self.following.length
    #     else:
    #         return 0

    # def get(self, index: int) -> Option[A]:
    #     if isinstance(self, Elem):
    #         return Some(self.value) if index == 0 else self.following.get(index - 1)
    #     else:
    #         return Nothing

    # <<<

    # --- Construct new lists ---

    def prepend(self, value: A) -> List[A]:
        """
        >>> List.of(1,2,3).prepend(0)
        0 :: 1 :: 2 :: 3 :: Nil
        """
        if isinstance(self, Elem):
            return Elem(value, self)
        else:
            return Elem(value)

    def extend(self, l: List[A]) -> List[A]:
        """
        >>> List.of(1,2,3).extend(List.of(4,5))
        1 :: 2 :: 3 :: 4 :: 5 :: Nil
        """
        if isinstance(self, Elem):
            return Elem(self.value, self.following.extend(l))
        else:
            return l

    # --- Access ---

    def first(self) -> A:
        """
        >>> List.of(1,2,3).first()
        1
        """
        if isinstance(self, Elem):
            return self.value
        else:
            raise UnexpectedNilError("Cannot call `first()` on `Nil`")

    def take_first(self, n: int) -> List[A]:
        """
        >>> List.of(1,2,3).take_first(2)
        1 :: 2 :: Nil
        """
        assert n >= 1
        if isinstance(self, Elem):
            return (
                Elem(self.value)
                if n == 1
                else Elem(self.value, self.following.take_first(n - 1))
            )
        else:
            raise UnexpectedNilError("Cannot call `take_first()` on `Nil`")

    def drop_first(self, n: int = 1) -> List[A]:
        """
        >>> List.of(1,2,3).drop_first(2)
        3 :: Nil
        """
        assert n >= 1
        if isinstance(self, Elem):
            return self.following if n == 1 else self.following.drop_first(n - 1)
        else:
            raise UnexpectedNilError("Cannot call `drop_first()` on `Nil`")

    def split_first(self) -> tuple[A, List[A]]:
        """
        >>> List.of(1,2,3).split_first()
        (1, 2 :: 3 :: Nil)
        """
        if isinstance(self, Elem):
            return self.first(), self.drop_first()
        else:
            raise UnexpectedNilError("Cannot call `split_first()` on `Nil`")

    # >>> Not O(1) :(

    # def last(self) -> A:
    #     """
    #     >>> List.of(1,2,3).last()
    #     3
    #     """
    #     if isinstance(self, Elem):
    #         return self.value if self.following is Nil else self.following.last()
    #     else:
    #         raise UnexpectedNilError("Cannot call `last()` on `Nil`")

    # def take_last(self, n: int = 1) -> List[A]:
    #     """
    #     >>> List.of(1,2,3).take_last(2)
    #     2 :: 3 :: Nil
    #     """
    #     # TODO: Error handling
    #     assert n >= 1
    #     return self.take_first(self.length - n)

    # def drop_last(self, n: int = 1) -> List[A]:
    #     ...  # TODO

    # def split_last(self) -> Option[tuple[List[A], A]]:
    #     ...  # TODO

    # <<<

    # --- Modifiers ---

    def _reverse(self, accumulated: List[A]) -> List[A]:
        if isinstance(self, Elem):
            return self.following._reverse(Elem(self.value, accumulated))
        else:
            return accumulated

    def reverse(self) -> List[A]:
        # TODO: Should this be past tense...?
        return self._reverse(Nil)

    # def split_at(self, n: int) -> tuple[List[A], List[A]]:
    #     ...  # TODO

    def filter(self, f: Callable[[A], bool]) -> List[A]:
        if isinstance(self, Elem):
            if f(self.value):
                return Elem(self.value, self.following.filter(f))
            else:
                return self.following.filter(f)
        else:
            return Nil

    def filter_not(self, f: Callable[[A], bool]) -> List[A]:
        return self.filter(lambda x: not f(x))

    def intercalate(self, a: A) -> List[A]:
        if isinstance(self, Elem):
            if isinstance(self.following, Elem):
                return Elem(self.value, Elem(a, self.intercalate(self.following)))
            else:
                return self
        else:
            return Nil

    # def chunks_of(self, n: int, drop_remainder: bool = False) -> List[A]:
    #     """
    #     # >>> [1,2,3,4,5].chunk(2)
    #     # [[1,2], [3,4], [5]]
    #     """
    #     ...  # TODO

    # def split_into(self, n: int) -> List[List[A]]:
    #     """
    #     # >>> List.of(1,2,3,4).split_into(2)
    #     # [[1,2], [3,4]]

    #     Name based on List.splitInto from F#
    #     """
    #     ...  # TODO

    # def window(
    #     self, size: int, step: int = 1, drop_remainder: bool = False
    # ) -> List[List[A]]:
    #     ...  # TODO

    # def group_by(self, f: Callable[[A], Any]) -> List[List[A]]:
    #     ...  # TODO

    # def partition(self, f: Callable[[A], bool]) -> tuple[List[A], List[A]]:
    #     return (self.filter(f), self.filter_not(f))


@final
class NilType(List[A], Singleton):
    def __repr__(self) -> str:
        """
        >>> NilType()
        Nil
        """
        return "Nil"


Nil: NilType = NilType()


@final
@dataclass(frozen=True, repr=False)
class Elem(List[A]):
    value: A
    following: List[A] = Nil

    def __repr__(self) -> str:
        """
        >>> Elem(1, Nil)
        1 :: Nil
        """
        return f"{self.value} :: {self.following}"
