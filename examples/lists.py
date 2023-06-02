from dataclasses import dataclass

from catepyller.data.list import List


@dataclass(frozen=True)
class Person:
    name: str
    age: int


def main():
    numbers = List.of(1, 2, 3)
    print(numbers)

    people = List.of(Person("Jerry", 46), Person("Donna", 52))
    print(people)

    ages = set(people.map(lambda p: p.age))
    print(ages)

    head, tail = people.decap
    print(head, tail)


if __name__ == "__main__":
    main()
