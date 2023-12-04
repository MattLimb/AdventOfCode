"""Advent of Code - Day 3."""
from collections import namedtuple
from pathlib import Path
from string import digits
from string import punctuation

INPUT_FILENAME: Path = Path("./input.txt")
CoOrdinate = namedtuple("CoOrdinate", ["y", "x"])

def read_input(filename: Path) -> list[str]:
    """Read the input to the days challenge.

    :arg filename: The filename of the input.
    :type filename: pathlib.Path

    :returns: A list strings. One item per line.
    :rtype: list[str]
    """
    with filename.open("r", encoding="utf-8") as _file_handler:
        return [ line.strip() for line in _file_handler.readlines() if len(line) != 0]


def discover_number(input_grid: list[str], coord: CoOrdinate) -> int:
    """Discover a valid number when given a coordinate.

    :arg input_grid: The grid to search.
    :type: input_grid: list[str]

    :arg coord: The coorinate to start searching from.
    :type coord: CoOrdinate

    :returns: The discovered number
    :rtype: int
    """
    if input_grid[coord.y][coord.x] not in digits:
        raise ValueError(f"Starting Position ({coord.y}, {coord.x}) is not a valid number.")

    output_string: str = input_grid[coord.y][coord.x]

    # Move Left
    new_x = coord.x - 1
    while new_x != -1:
        val = input_grid[coord.y][new_x]

        if val not in digits:
            break

        output_string = f"{val}{output_string}"
        new_x -= 1

    # Move Right
    new_x = coord.x + 1
    while new_x != (len(input_grid[coord.y])):
        val = input_grid[coord.y][new_x]

        if val not in digits:
            break

        output_string = f"{output_string}{val}"
        new_x += 1

    return int(output_string)


def coord_around(coord: CoOrdinate, max_coord: CoOrdinate) -> list[CoOrdinate]:
    """Get the coordinates surrounding a given coordinate.

    :arg coord: The starting coordinate.
    :type coord: CoOrdinate

    :arg max_coord: The coordinate representing the maximum values for x and y.
    :type: CoOrdinte

    :returns: A list of all surrounding coordinates.
    :rtype: list[CoOrdinate]
    """
    output: list[CoOrdinate] = []

    # Row Above
    if coord.y != 0:
        if coord.x != 0:
            output.append(CoOrdinate(y=coord.y-1, x=coord.x-1))

        output.append(CoOrdinate(y=coord.y-1, x=coord.x))

        if coord.x != max_coord.x:
            output.append(CoOrdinate(y=coord.y-1, x=coord.x+1))

    # Current Row
    if coord.x != 0:
        output.append(CoOrdinate(y=coord.y, x=coord.x-1))

    output.append(CoOrdinate(y=coord.y, x=coord.x))

    if coord.x != max_coord.x:
        output.append(CoOrdinate(y=coord.y, x=coord.x+1))

    # Row Below
    if coord.y != max_coord.y:
        if coord.x != 0:
            output.append(CoOrdinate(y=coord.y+1, x=coord.x-1))

        output.append(CoOrdinate(y=coord.y+1, x=coord.x))

        if coord.x != max_coord.x:
            output.append(CoOrdinate(y=coord.y+1, x=coord.x+1))

    return output

def part_1(input_grid: list[str]) -> list[int]:
    """Parse through the grid to find part numbers.

    :arg input_grid: The grid to use as input.
    :type input_grid: list[str]

    :returns: All part numbers in the grid.
    :rtype: list[int]
    """
    max_coord = CoOrdinate(y=len(input_grid)-1, x=len(input_grid[0])-1)
    part_numbers: list[int] = []

    for y, row in enumerate(input_grid):
        for x, col in enumerate(row):
            if col in punctuation and col != ".":
                coord = CoOrdinate(y=y, x=x)
                all_around = coord_around(coord, max_coord=max_coord)


                filter_out = set(map(
                    lambda o: discover_number(input_grid, o),
                    filter(
                        lambda o: input_grid[o.y][o.x] in digits,
                        all_around
                    )
                ))
                part_numbers.extend(list(filter_out))
            

    return part_numbers

def part_2(input_grid: list[str]) -> list[int]:
    """Parse through the grid to find gear ratios.

    :arg input_grid: The grid to use as input.
    :type input_grid: list[str]

    :returns: All gear ratios in the grid.
    :rtype: list[int]
    """
    max_coord = CoOrdinate(y=len(input_grid)-1, x=len(input_grid[0])-1)
    ratios: list[int] = []

    for y, row in enumerate(input_grid):
        for x, col in enumerate(row):
            if col == "*":
                coord = CoOrdinate(y=y, x=x)
                all_around = coord_around(coord, max_coord=max_coord)

                filter_out = list(set(map(
                    lambda o: discover_number(input_grid, o),
                    filter(
                        lambda o: input_grid[o.y][o.x] in digits,
                        all_around
                    )
                )))

                if len(filter_out) == 2:
                    ratios.append(filter_out[0] * filter_out[-1])

    return ratios


if __name__ == "__main__":
    puzzle_input: list[str] = read_input(INPUT_FILENAME)

    print("Part 1:", sum(part_1(puzzle_input)))
    print("Part 2:", sum(part_2(puzzle_input)))
