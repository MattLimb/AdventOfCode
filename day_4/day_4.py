"""Advent of Code - Day 4."""
from pathlib import Path


INPUT_FILENAME: Path = Path("./input.txt")
LEVEL_1_SPLIT_CHAR: str = ","
LEVEL_2_SPLIT_CHAR: str = "-"


def read_input(filename: Path) -> list[str]:
    """Read the input to the days challenge.

    :arg filename: The filename of the input.
    :type filename: pathlib.Path

    :returns: A list strings. One item per line.
    :rtype: list[str]
    """
    with filename.open("r", encoding="utf-8") as _file_handler:
        return _file_handler.readlines()


def process_pairings(pair: str) -> tuple[set[int], set[int]]:
    """Process the pairings into two sets.

    :arg pair: The raw input of pairings. Newline delimited `3-3,9-56`
    :type pair: str

    :returns: The pairings as range sets.
    :rtype: list[tuple[set[int], set[int]]]
    """
    pair_a, pair_b = pair.strip().split(LEVEL_1_SPLIT_CHAR)

    a: list[int] = [int(item) for item in pair_a.split(LEVEL_2_SPLIT_CHAR)]
    b: list[int] = [int(item) for item in pair_b.split(LEVEL_2_SPLIT_CHAR)]

    a_set = set(range(int(a[0]), int(a[1]) + 1))
    b_set = set(range(int(b[0]), int(b[1]) + 1))

    return a_set, b_set


def part_1(pairings: list[str]) -> int:
    """Calculate the number of pairings whereby one pair exists entirely within the other.

    :arg pairings: The raw input of pairings. Newline delimited `3-3,9-56`
    :type pairings: list[str]

    :retturns: Number of pairings where one range exists within the other.
    :rtype: int
    """
    overlapping_pairs: int = 0

    for pair in pairings:
        a_set, b_set = process_pairings(pair)

        if a_set.issubset(b_set) or b_set.issubset(a_set):
            overlapping_pairs += 1

    return overlapping_pairs


def part_2(pairings: list[str]) -> int:
    """Calculate the number of pairings whereby one pair overlaps even partially with another.

    :arg pairings: The raw input of pairings. Newline delimited `3-3,9-56`
    :type pairings: list[str]

    :retturns: Number of pairings where the ranges overlap.
    :rtype: int
    """
    overlapping_pairs: int = 0

    for pair in pairings:
        a_set, b_set = process_pairings(pair)

        if len(a_set & b_set) > 0:
            overlapping_pairs += 1

    return overlapping_pairs


def main():
    """The main program function."""
    raw_input: list[str] = read_input(INPUT_FILENAME)

    print("Part 1:", part_1(raw_input))
    print("Part 2:", part_2(raw_input))


if __name__ == "__main__":
    main()
