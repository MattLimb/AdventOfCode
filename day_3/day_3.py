"""Advent of Code - Day 2."""
from collections import namedtuple
from pathlib import Path
from string import digits
from string import punctuation

INPUT_FILENAME: Path = Path("./input.txt")
CoOrdinate = namedtuple("CoOrdinate", ["x", "y"])

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
    if input_grid[coord.x][coord.y] not in digits:
        raise ValueError(f"Starting Position ({coord.x}, {coord.y}) is not a valid number.")

    output_string: str = input_grid[coord.x][coord.y]

    # Move Left
    new_y = coord.y - 1
    while new_y != -1:
        val = input_grid[coord.x][new_y]

        if val not in digits:
            break

        output_string = f"{val}{output_string}"
        new_y -= 1

    # Move Right
    new_y = coord.y + 1
    while new_y != (len(input_grid[coord.x])):
        val = input_grid[coord.x][new_y]

        if val not in digits:
            break

        output_string = f"{output_string}{val}"
        new_y += 1

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
    if coord.x != 0:
        if coord.y != 0:
            output.append(CoOrdinate(coord.x-1, coord.y-1))

        output.append(CoOrdinate(coord.x-1, coord.y))

        if coord.y != max_coord.y:
            output.append(CoOrdinate(coord.x-1, coord.y+1))

    # Current Row
    if coord.y != 0:
        output.append(CoOrdinate(coord.x, coord.y-1))

    output.append(CoOrdinate(coord.x, coord.y))

    if coord.y != max_coord.y:
        output.append(CoOrdinate(coord.x, coord.y+1))

    # Row Below
    if coord.x != max_coord.x:
        if coord.y != 0:
            output.append(CoOrdinate(coord.x+1, coord.y-1))

        output.append(CoOrdinate(coord.x+1, coord.y))

        if coord.y != max_coord.y:
            output.append(CoOrdinate(coord.x+1, coord.y+1))

    return output

def part_1(input_grid: list[str]) -> list[int]:
    """Parse through the grid to find part numbers.

    :arg input_grid: The grid to use as input.
    :type input_grid: list[str]

    :returns: All part numbers in the grid.
    :rtype: list[int]
    """
    max_coord = CoOrdinate(len(input_grid)-1, len(input_grid[0])-1)
    part_numbers: list[int] = []

    for x, row in enumerate(input_grid):
        for y, col in enumerate(row):
            if col in punctuation and col != ".":
                coord = CoOrdinate(x, y)
                all_around = coord_around(coord, max_coord=max_coord)

                filter_out = set(map(
                    lambda o: discover_number(input_grid, o),
                    filter(
                        lambda o: input_grid[o.x][o.y] in digits,
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
    max_coord = CoOrdinate(len(input_grid)-1, len(input_grid[0])-1)
    ratios: list[int] = []

    for x, row in enumerate(input_grid):
        for y, col in enumerate(row):
            if col == "*":
                coord = CoOrdinate(x, y)
                all_around = coord_around(coord, max_coord=max_coord)

                filter_out = list(set(map(
                    lambda o: discover_number(input_grid, o),
                    filter(
                        lambda o: input_grid[o.x][o.y] in digits,
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
    # print("\n".join(puzzle_input))
