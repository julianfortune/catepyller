from __future__ import annotations

from typing import Any, Callable, Protocol, TypeVar, runtime_checkable

A = TypeVar("A", covariant=True)
B = TypeVar("B", contravariant=True)

ValueT = TypeVar("ValueT")


@runtime_checkable
class Functor(Protocol[A]):
    def map(self, f: Callable[[A], B]) -> Functor[B]:
        ...


@runtime_checkable
class Semigroupal(Protocol[A]):
    def product(self, fb: Any[B]) -> Semigroupal[tuple[A, B]]:
        ...


@runtime_checkable
class Applicative(Functor[A], Protocol[A]):
    @classmethod
    def pure(cls, value: ValueT) -> Any[ValueT]:
        """
        Haskell -> 'pure'
        Scala -> 'pure'
        F# -> 'lift'
        """
        ...

    # There is no way to properly notate the type of `f`
    def apply(self, f: Any[Callable[[A], B]]) -> Applicative[B]:
        """
        Haskell -> '<*>'
        Scala -> 'ap'
        """
        ...


@runtime_checkable
class Monad(Applicative[A], Protocol[A]):
    """
    Must implement `pure` and `flat_map`.

    Must re-declare with correct types:
    - map
    - apply
    """

    def flat_map(self, f: Callable[[A], Any[B]]) -> Monad[B]:
        ...

    def map(self, f: Callable[[A], B]) -> Any[B]:
        return self.flat_map(self.pure(f))

    def apply(self, f: Any[Callable[[A], B]]) -> Any[B]:
        return f.flat_map(self.map)
