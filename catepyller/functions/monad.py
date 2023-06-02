from __future__ import annotations

from typing import TypeVar, overload

from catepyller.data.list import List
from catepyller.data.option import Option
from catepyller.operator import identity
from catepyller.protocols import Monad

A = TypeVar("A", covariant=True)
B = TypeVar("B", contravariant=True)

ValueT = TypeVar("ValueT")

# fmt: off
@overload
def flatten(nested_monad: List[List[ValueT]]) -> List[ValueT]: ...

@overload
def flatten(nested_monad: Option[Option[ValueT]]) -> Option[ValueT]: ...
# fmt: on


def flatten(nested_monad: Monad[Monad[ValueT]]) -> Monad[ValueT]:
    return nested_monad.flat_map(identity)
