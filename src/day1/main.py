"""
### Part 1:

--- Day 1: Calorie Counting ---

Santa's reindeer typically eat regular reindeer food, but they need a lot of
magical energy to deliver presents on Christmas. For that, their favorite snack
is a special type of **star** fruit that only grows deep in the jungle. The
Elves have brought you on their annual expedition to the grove where the fruit
grows.

To supply enough magical energy, the expedition needs to retrieve a minimum of
**fifty stars** by December 25th. Although the Elves assure you that the grove
has plenty of fruit, you decide to grab any fruit you see along the way, just in
case.

Collect stars by solving puzzles. Two puzzles will be made available on each day
in the Advent calendar; the second puzzle is unlocked when you complete the
first. Each puzzle grants **one star**. Good luck!

The jungle must be too overgrown and difficult to navigate in vehicles or access
from the air; the Elves' expedition traditionally goes on foot. As your boats
approach land, the Elves begin taking inventory of their supplies. One important
consideration is food - in particular, the number of **Calories** each Elf is
carrying (your puzzle input).

The Elves take turns writing down the number of Calories contained by the
various meals, snacks, rations, etc. that they've brought with them, one item
per line. Each Elf separates their own inventory from the previous Elf's
inventory (if any) by a blank line.
"""


import io
from typing import Generic, Iterable, Iterator, TextIO, TypeVar


def test_part1() -> None:
    """
    For example, suppose the Elves finish writing their items' Calories and end up
    with the following list:
    """

    input = io.StringIO(
        """\
        1000
        2000
        3000

        4000

        5000
        6000

        7000
        8000
        9000

        10000"""  # pycco needs this comment
    )

    elf_notes = iter(parse_calorie_notes(input))

    # This list represents the Calories of the food carried by five Elves:

    # > The first Elf is carrying food with `1000`, `2000`, and `3000` Calories,
    #   a total of `6000` Calories.
    assert sum(next(elf_notes)) == 6000

    # > The second Elf is carrying one food item with `4000` Calories.
    assert sum(next(elf_notes)) == 4000

    # > The third Elf is carrying food with `5000` and `6000` Calories, a total
    #   of `11000` Calories.
    assert sum(next(elf_notes)) == 11000

    # > The fourth Elf is carrying food with `7000`, `8000`, and `9000`
    #   Calories, a total of `24000` Calories.
    assert sum(next(elf_notes)) == 24000

    # > The fifth Elf is carrying one food item with `10000` Calories.
    assert sum(next(elf_notes)) == 10000


"""
In case the Elves get hungry and need extra snacks, they need to know which Elf
to ask: they'd like to know how many Calories are being carried by the Elf
carrying the most Calories. In the example above, this is `24000` (carried by
the fourth Elf).

Find the Elf carrying the most Calories. How many total Calories is that Elf
carrying?
"""

# === Part 1 Solution: ===

"""
Solution seems straightforward. Parse the input into a list of list of `int`s,
then find the `max()` with `sum()` as the key.
"""


T = TypeVar("T")


class InspectableIter(Generic[T]):
    """
    Provides an iterable for `it` with a `.has_stopped` member that becomes
    `True` once empty.
    """

    def __init__(self, it: Iterable) -> None:
        self.has_stopped = False
        self.it = iter(it)

    def __iter__(self) -> Iterator[T]:
        return self

    def __next__(self) -> T:
        try:
            return next(self.it)
        except StopIteration:
            self.has_stopped = True
            raise


def parse_calorie_notes(input: TextIO) -> Iterable[Iterable[int]]:
    """
    Parse the noted Calorie amounts from the multiline string input and return
    the total as a list of list of Calorie counts.
    """

    def yield_group(it: Iterator) -> Iterable[int]:
        """
        Yields lines as ints until a blank line is found.

        Equivalent to `map(int, iter(it.__next__, ""))`.
        """
        for val in it:
            if val == "":
                break
            yield int(val)

    lines: InspectableIter[str] = InspectableIter(map(str.strip, input))
    while not lines.has_stopped:
        yield yield_group(lines)


def part1(input: TextIO) -> int:
    """
    Find the elf that holds the most amount of Calories, and return the amount
    of Calories they hold.
    """
    elf_notes = parse_calorie_notes(input)
    totals: Iterable[int] = map(sum, elf_notes)
    return max(totals)


"""
### Part 2:

<paste in problem description here>
"""


def test_part2() -> None:
    """For example:"""
    # > `""` results in  `...`.
    assert part2(io.StringIO("")) == ...


"""
<end of problem description>
"""

# === Part 2 Solution: ===


def part2(input: TextIO) -> ...:
    """ """
    return ...


if __name__ == "__main__":
    # Print out part 1 solution
    with open("input.txt") as puzzle_input:
        print("Part 1:", part1(puzzle_input))

    # Print out part 2 solution
    with open("input.txt") as puzzle_input:
        print("Part 2:", part2(puzzle_input))
