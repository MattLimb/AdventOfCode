"""Advent of Code - Day 8."""
from pathlib import Path


INPUT_FILENAME: Path = Path("./input.txt")
RC_TYPE = list[list[int]]


def read_input(filename: Path) -> list[list[int]]:
    """Read the input to the days challenge.

    :arg filename: The filename of the input.
    :type filename: pathlib.Path

    :returns: A list strings. One item per line.
    :rtype: list[str]
    """
    with filename.open("r", encoding="utf-8") as _file_handler:
        return [
            [int(tree) for tree in line.strip()] for line in _file_handler.readlines()
        ]


def process_input(tree_grid: RC_TYPE) -> tuple[RC_TYPE, RC_TYPE]:
    """Process the input as rows and columns.

    :arg tree_grid: The grid of trees
    :type tree_grid: list[list[int]]

    :returns: The rows and columns broken out as two lists.
    :rtype: tuple[list[list[int]], list[list[int]]]
    """
    col_grid: RC_TYPE = [[] for _ in range(len(tree_grid[0]))]

    for ridx, row in enumerate(tree_grid):
        for cidx, col in enumerate(row):
            col_grid[cidx].append(col)

    return tree_grid, col_grid


def part_1(tree_rows: RC_TYPE, tree_columns: RC_TYPE) -> int:
    """Calculate how many trees are visiable from outside the grid.

    :arg tree_rows: The grid of rows being assessed.
    :type tree_rows: list[list[int]]

    :arg tree_columns: The grid of columns  being assessed.
    :type tree_columns: list[list[int]]

    :returns: An integer representing the number of trees visiable.
    :rtype: int
    """
    num_rows: int = len(tree_rows)
    row_length: int = len(tree_rows)

    visible_trees: int = (row_length * 2) + ((num_rows - 2) * 2)

    # Iterate over each row from the second row
    for row in range(1, num_rows - 1):
        # Iterate over each item in the row from the second item to the second to last item.
        for col in range(1, row_length - 1):
            item = tree_rows[row][col]

            check_taller = lambda i: i >= item

            row_left = list(map(check_taller, tree_rows[row][:col]))
            row_right = list(map(check_taller, tree_rows[row][col + 1 :]))

            col_up = list(map(check_taller, tree_columns[col][:row]))
            col_down = list(map(check_taller, tree_columns[col][row + 1 :]))

            visible_angles = [
                not any(row_left),
                not any(row_right),
                not any(col_up),
                not any(col_down),
            ]

            if any(visible_angles):
                visible_trees += 1

    return visible_trees


def part_2(tree_rows: RC_TYPE, tree_columns: RC_TYPE) -> int:
    """Calculate the highest possible scenic score.

    :arg tree_rows: The grid of rows being assessed.
    :type tree_rows: list[list[int]]

    :arg tree_columns: The grid of columns  being assessed.
    :type tree_columns: list[list[int]]

    :returns: An integer representing the number of trees visiable.
    :rtype: int
    """
    num_rows: int = len(tree_rows)
    row_length: int = len(tree_rows)

    highest_score: int = 0

    # Iterate over each row from the second row
    for row in range(1, num_rows - 1):
        # Iterate over each item in the row from the second item to the second to last item.
        for col in range(1, row_length - 1):
            item = tree_rows[row][col]
            score = 1  # Stop times by 0 error

            row_col = [
                list(reversed(tree_columns[col][:row])),  # Col Up
                list(reversed(tree_rows[row][:col])),  # Row Left
                tree_rows[row][col + 1 :],  # Row Right
                tree_columns[col][row + 1 :],  # Col Down
            ]

            for direction in row_col:
                tmp_score = 0

                for tmp_item in direction:
                    tmp_score += 1

                    if tmp_item >= item:
                        break

                if tmp_score > 0:
                    score *= tmp_score

            if score > highest_score:
                highest_score = score

    return highest_score


def main() -> None:
    """The main program function."""
    raw_input: RC_TYPE = read_input(INPUT_FILENAME)

    rows, columns = process_input(raw_input)

    print("Part 1:", part_1(rows, columns))
    print("Part 2:", part_2(rows, columns))


if __name__ == "__main__":
    main()
