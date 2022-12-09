"""Advent of Code - Day 9."""
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

INPUT_FILENAME: Path = Path("./input.txt")
INSTRUC_LIST_TYPE = list[tuple["Instruction", int]]
INSTRUC_SEP = " "


@dataclass
class Position:
    """Position class to make reasoning about each item easier."""

    x: int
    y: int


class Instruction(str, Enum):
    """A string enum showing the possible instructions."""

    U = "U"
    D = "D"
    L = "L"
    R = "R"


def read_input(filename: Path) -> INSTRUC_LIST_TYPE:
    """Read the input to the days challenge.

    :arg filename: The filename of the input.
    :type filename: pathlib.Path

    :returns: A list strings. One item per line.
    :rtype: list[str]
    """
    with filename.open("r", encoding="utf-8") as _file_handler:
        lines = []

        for line in _file_handler.readlines():
            inst, num = line.strip().split(INSTRUC_SEP)
            lines.append((Instruction[inst], int(num)))

        return lines


def move_tail(head_pos: Position, tail_pos: Position) -> Position:
    """Move the tail according to the rules set out in the AoC challenge.

    :arg head_pos: The current position of the head.
    :type head_pos: Position

    :arg tail_pos: The current position of the tail.
    :type tail_pos: Position

    :returns: The new position of the tail.
    :rtype: tuple[int. int]
    """
    spaces_around_head = [
        # Middle Left
        Position(x=head_pos.x - 1, y=head_pos.y),
        # Middle
        head_pos,
        # Middle Right
        Position(x=head_pos.x + 1, y=head_pos.y),
    ]

    # Go Up
    spaces_around_head.extend(
        [
            # Top Left
            Position(x=head_pos.x - 1, y=head_pos.y + 1),
            # Top Middle
            Position(x=head_pos.x, y=head_pos.y + 1),
            # Top Right
            Position(x=head_pos.x + 1, y=head_pos.y + 1),
        ]
    )
    # Go Down
    spaces_around_head.extend(
        [
            # Bottom Left
            Position(x=head_pos.x - 1, y=head_pos.y - 1),
            # Bottom Middle
            Position(x=head_pos.x, y=head_pos.y - 1),
            # Bottom Right
            Position(x=head_pos.x + 1, y=head_pos.y - 1),
        ]
    )

    if tail_pos in spaces_around_head:
        # Tail is already within 1 - No movement.
        return tail_pos

    # Head is right of tail
    if tail_pos.x < head_pos.x:
        tail_pos.x += 1
    # Head is to the left of tail
    elif tail_pos.x > head_pos.x:
        tail_pos.x -= 1

    # Head is above tail
    if tail_pos.y < head_pos.y:
        tail_pos.y += 1
    # Head is below tail
    elif tail_pos.y > head_pos.y:
        tail_pos.y -= 1

    return tail_pos


def part_1(instructions: INSTRUC_LIST_TYPE) -> int:
    """Calculate how many unique co-ordinates the tail went to.

    :arg instructions: The list of instructions to process each step.
    :type tree_rows: list[list[int]]

    :returns: An integer representing the number of unique spaces the tail went to.
    :rtype: int
    """
    # Co-ordinate System - (x, y)
    head = Position(x=0, y=0)
    tail = Position(x=0, y=0)

    tail_spaces: set[tuple[int, int]] = set()

    for idx, (direction, amount) in enumerate(instructions):
        for _ in range(amount):
            if direction == Instruction.U:
                # Go Up
                head.y += 1
            elif direction == Instruction.D:
                # Go Down
                head.y -= 1
            elif direction == Instruction.L:
                # Go Left <-
                head.x -= 1
            else:
                # Go Right ->
                head.x += 1

            tail = move_tail(head, tail)
            tail_spaces.add((tail.x, tail.y))

    return len(tail_spaces)


def part_2(instructions: INSTRUC_LIST_TYPE) -> int:
    """Calculate how many unique co-ordinates the tail went to with 10 knots.

    :arg instructions: The list of instructions to process each step.
    :type tree_rows: list[list[int]]

    :returns: An integer representing the number of unique spaces the tail went to.
    :rtype: int
    """
    # Co-ordinate System - (x, y)
    rope = [Position(x=0, y=0) for _ in range(10)]

    tail_spaces: set[tuple[int, int]] = set()

    for idx, (direction, amount) in enumerate(instructions):
        for _ in range(amount):
            if direction == Instruction.U:
                # Go Up
                rope[0].y += 1
            elif direction == Instruction.D:
                # Go Down
                rope[0].y -= 1
            elif direction == Instruction.L:
                # Go Left <-
                rope[0].x -= 1
            else:
                # Go Right ->
                rope[0].x += 1

            for idx in range(1, 10):
                rope[idx] = move_tail(rope[idx - 1], rope[idx])

            tail_spaces.add((rope[-1].x, rope[-1].y))

    return len(tail_spaces)


def main() -> None:
    """The main program function."""
    raw_input: INSTRUC_LIST_TYPE = read_input(INPUT_FILENAME)
    print("Part 1:", part_1(raw_input))
    print("Part 2:", part_2(raw_input))


if __name__ == "__main__":
    main()
