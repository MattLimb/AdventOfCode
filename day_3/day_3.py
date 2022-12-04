"""Advent of Code - Day 3."""
from pathlib import Path


INPUT_FILENAME: Path = Path("./input.txt")
PRIORITY_ORDER: str = "abcdefghijklmnopqrstuvwxyz" "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def read_input(filename: Path) -> list[str]:
    """Read the input to the days challenge.

    :arg filename: The filename of the input.
    :type filename: pathlib.Path

    :returns: A list strings. One item per line.
    :rtype: list[str]
    """
    with filename.open("r", encoding="utf-8") as _file_handler:
        return _file_handler.readlines()


def part_1(rucksacks: list[str]) -> int:
    """Split a rucksack into the two compartments.

    :arg rucksacks: The raw input of all the rucksacks.
    :type rucksacks: list[str]

    :returns: The total score of each backpacks duplicates.
    :rtype: int
    """
    rucksacks_dupe: list[str] = []

    for rucksack in rucksacks:
        rucksack = rucksack.strip()
        rucksack_size: int = len(rucksack)
        compartment_size: int = rucksack_size // 2

        comp_1 = set(rucksack[:compartment_size])
        comp_2 = set(rucksack[compartment_size:])

        duplicate_item = comp_1.intersection(comp_2).pop()
        rucksacks_dupe.append(duplicate_item)

    rucksack_score: list[int] = [
        PRIORITY_ORDER.index(item) + 1 for item in rucksacks_dupe
    ]

    return sum(rucksack_score)


def part_2(rucksacks: list[str]) -> int:
    """Split all rucksacks into a group of three, and calculate the common item.

    :arg rucksacks: The raw input of all the rucksacks.
    :type rucksacks: list[str]

    :returns: The total score of each backpack group's common item.
    :rtype: int
    """
    common_items: list[str] = []

    for idx_start in range(0, len(rucksacks), 3):
        group: list[set[str]] = [
            set(rucksacks[idx_start + i].strip()) for i in range(3)
        ]

        common: set[str] = group[0] & group[1] & group[2]

        common_items.append(common.pop())

    rucksack_score: list[int] = [
        PRIORITY_ORDER.index(item) + 1 for item in common_items
    ]

    return sum(rucksack_score)


def main():
    """The main program function."""
    raw_input: list[str] = read_input(INPUT_FILENAME)

    print("Part 1:", part_1(raw_input))
    print("Part 2:", part_2(raw_input))


if __name__ == "__main__":
    main()
