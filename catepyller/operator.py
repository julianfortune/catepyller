from typing import TypeVar

A = TypeVar("A")


def identity(a: A) -> A:
    return a
