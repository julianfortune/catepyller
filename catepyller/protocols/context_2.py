from __future__ import annotations

from typing import Any, Callable, Protocol, TypeVar, runtime_checkable

A = TypeVar("A", covariant=True)
B = TypeVar("B", covariant=True)

C = TypeVar("C", contravariant=True)
D = TypeVar("D", contravariant=True)

ValueT = TypeVar("ValueT")


@runtime_checkable
class Functor2(Protocol[A, B]):
    def map(self, f: Callable[[A], C]) -> Functor2[C, B]:
        ...


@runtime_checkable
class Semigroupal2(Protocol[A, B]):
    def product(
        self, fb: Any[C, D]
    ) -> Semigroupal2[tuple[A, C], B | D]:  # Is this right ???
        ...


@runtime_checkable
class Applicative2(Functor2[A, B], Protocol[A, B]):
    @classmethod
    def pure(cls, value: ValueT) -> Any[ValueT]:
        """
        Haskell -> 'pure'
        Scala -> 'pure'
        F# -> 'lift'
        """
        ...

    # There is no way to properly notate the type of `f`
    def apply(self, f: Any[Callable[[A], C]]) -> Applicative2[C, B]:
        """
        Haskell -> '<*>'
        Scala -> 'ap'
        """
        ...


@runtime_checkable
class Monad2(Applicative2[A, B], Protocol[A, B]):
    """
    Must implement `pure` and `flat_map`.

    Suggested to re-declare with correct types:
    - map
    - apply
    """

    def flat_map(self, f: Callable[[A], Any[C, B]]) -> Monad2[C, B]:
        ...

    def map(self, f: Callable[[A], C]) -> Functor2[C, B]:
        return self.flat_map(self.pure(f))

    def apply(self, f: Any[Callable[[A, B], C]]) -> Applicative2[C, B]:
        return f.flat_map(self.map)
