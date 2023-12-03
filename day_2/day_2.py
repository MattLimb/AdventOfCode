"""Advent of Code - Day 2."""
from collections import namedtuple
from pathlib import Path


INPUT_FILENAME: Path = Path("./input.txt")
CubeAmounts = namedtuple("CubeAmounts", ["red", "green", "blue"])

TOTAL_CUBES = CubeAmounts(red=12, green=13, blue=14)

def read_input(filename: Path) -> list[str]:
    """Read the input to the days challenge.

    :arg filename: The filename of the input.
    :type filename: pathlib.Path

    :returns: A list strings. One item per line.
    :rtype: list[str]
    """
    with filename.open("r", encoding="utf-8") as _file_handler:
        return [ line.strip() for line in _file_handler.readlines() if len(line) != 0]

def process_input(input_list: list[str]) -> dict[int, list[CubeAmounts]]:
    """For each line in the puzzle input - parse through it so that it is easier to use.
    
    :arg input_list: The raw puzzle input as read from the file.
    :type input_list: list[str]

    :returns: A dictionary containing all the games and their scores.
    :rtype: dict[int, list[CubeAmounts]]
    """
    output: dict[int, list[CubeAmounts]] = {}

    for game in input_list:
        gname, guesses = game.split(":", 1)
        gid = int(gname.split(" ", 1)[-1].strip())

        output[gid] = []

        for guess in guesses.split(";"):
            red = green = blue = 0
            for g in guess.strip().split(","):
                num, colour = g.strip().split(" ")

                match (num, colour):
                    case (num, "blue"):
                        blue += int(num)
                    case (num, "red"):
                        red += int(num)
                    case (num, "green"):
                        green += int(num)
                    case _:
                        print(f"UNKNOWN {num=}, {colour=}")

            output[gid].append(
                CubeAmounts(red=red, green=green, blue=blue)
            )

    return output

def part_1(puzzle_input_dict: dict[int, list[CubeAmounts]]) -> list[int]:
    """For each line in the puzzle input, discover the first and last digit.

    :arg puzzle_input_list: The input provided by AdventOfCode processed to be useful.
    :type puzzle_input_list: dict[str, list[CubeAmounts]]

    :returns: A list of integer ids of the games possible to play.
    :rtype: list[int]
    """
    output: list[int] = []

    for game_id, games in puzzle_input_dict.items():
        is_valid: bool = True

        for game in games:
            if game.blue > TOTAL_CUBES.blue:
                is_valid = False

            if game.green > TOTAL_CUBES.green:
                is_valid = False

            if game.red > TOTAL_CUBES.red:
                is_valid = False

        if is_valid:
            output.append(game_id)

    return output


def part_2(puzzle_input_dict: dict[int, list[CubeAmounts]]) -> list[int]:
    """For each line in the puzzle input, discover the first and last digit.

    :arg puzzle_input_list: The input provided by AdventOfCode processed to be useful.
    :type puzzle_input_list: dict[str, list[CubeAmounts]]

    :returns: A power of the minimum number of cubes required to play.
    :rtype: list[int]
    """
    output: list[int] = []

    for _, games in puzzle_input_dict.items():
        red = green = blue = 0

        for game in games:
            if game.blue > blue:
                blue = game.blue

            if game.green > green:
                green = game.green

            if game.red > red:
                red = game.red

        output.append(red*green*blue)

    return output


if __name__ == "__main__":
    puzzle_input: list[str] = read_input(INPUT_FILENAME)
    processed_input = process_input(puzzle_input)

    print("Part 1:", sum(part_1(processed_input)))
    print("Part 2:", sum(part_2(processed_input)))
