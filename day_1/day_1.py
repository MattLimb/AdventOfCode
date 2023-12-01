"""Advent of Code - Day 1."""
import re
from pathlib import Path


INPUT_FILENAME: Path = Path("./input.txt")

NUMBERS_AS_TEXT: dict[str, str] = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

def read_input(filename: Path) -> list[str]:
    """Read the input to the days challenge.

    :arg filename: The filename of the input.
    :type filename: pathlib.Path

    :returns: A list strings. One item per line.
    :rtype: list[str]
    """
    with filename.open("r", encoding="utf-8") as _file_handler:
        return [ line.strip() for line in _file_handler.readlines() if len(line) != 0]


def part_1(puzzle_input_list: list[str]) -> list[int]:
    """For each line in the puzzle input, discover the first and last digit.

    :arg puzzle_input_list: The input provided by AdventOfCode as a list of stings.
    :type puzzle_input_list: list[str]

    :returns: A list of integers containing the first and last digit on each line.
    :rtype: list[int]
    """
    output: list[int] = []

    for line in puzzle_input_list:
        numbers_in_string = [ character for character in line if character.isdigit() ]

        first_number = numbers_in_string[0]
        last_number = numbers_in_string[-1]

        output.append(int(f"{first_number}{last_number}"))

    return output


def part_2(puzzle_input_list: list[str]) -> list[int]:
    """For each line in the puzzle input, discover the first and last digit.

    :arg puzzle_input_list: The input provided by AdventOfCode as a list of stings.
    :type puzzle_input_list: list[str]

    :returns: A list of integers containing the first and last digit on each line.
    :rtype: list[int]
    """
    output: list[int] = []
    regex = re.compile(rf"(?=([1-9]|{'|'.join(NUMBERS_AS_TEXT.keys())}))")

    for line in puzzle_input_list:
        numbers_in_string: list[str] = regex.findall(line)

        first_number: str = NUMBERS_AS_TEXT.get(numbers_in_string[0], numbers_in_string[0])
        last_number: str = NUMBERS_AS_TEXT.get(numbers_in_string[-1], numbers_in_string[-1])

        number: int = int(f"{first_number}{last_number}")

        output.append(number)

    return output



if __name__ == "__main__":
    puzzle_input: list[str] = read_input(INPUT_FILENAME)

    print("Part 1:", sum(part_1(puzzle_input)))
    print("Part 2:", sum(part_2(puzzle_input)))
