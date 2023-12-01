"""Advent of Code - Day 12."""
from collections import namedtuple
from pathlib import Path
from typing import Optional
from copy import deepcopy


INPUT_FILENAME: Path = Path("./input_test.txt")
Position = namedtuple("Position", ("x", "y"))

START_CHAR: str = "S"
START_HEIGHT: str = "a"
END_CHAR: str = "E"

HEIGHT_MAP = "SabcdefghijklmnopqrstuvwxyzE."


def read_input(filename: Path) -> list[list[str]]:
    """Read the input to the days challenge.

    :arg filename: The filename of the input.
    :type filename: pathlib.Path

    :returns: A list strings. One item per line.
    :rtype: list[list[str]]
    """
    with filename.open("r", encoding="utf-8") as _file_handler:
        return [list(line.strip()) for line in _file_handler.readlines()]


def find_positions(graph: list[list[str]]) -> tuple[list[list[str]], Position, Position]:
    """Find the start and end positions from the puzzel input.

    :arg graph: The heightmap of the surrounding area.
    :type graph: list[list[str]]

    :returns: The position of the start, and end.
    :rtype: tuple[Position, Position]
    """
    start: Optional[Position] = None
    end: Optional[Position] = None

    for y, line in enumerate(graph):
        if START_CHAR in line:
            start = Position(x=line.index(START_CHAR), y=y)

        if END_CHAR in line:
            end = Position(x=line.index(END_CHAR), y=y)

    graph[start.y][start.x] = "a"
    graph[end.y][end.x] = "z"

    return graph, start, end

#
# def find_path(graph: list[list[str]], start: Position, end: Position) -> int:
#     """Find a path through the graph to reach the end.
#
#     :arg graph: The heightmap of the surrounding region.
#     :type graph: list[list[str]]
#
#     :arg start: The starting position in the graph.
#     :type start: Position
#
#     :arg end: The ending position in the graph.
#     :type end: Position:
#
#     :returns: The number of steps taken to reach the goal.
#     :rtype: int
#     """
#     finish: bool = False
#     step_history: list[Position] = [start]
#     step_exclude: list[Position] = []
#
#     def filter_out(item: Position) -> bool:
#         """Closure to filter out potential positions when moving.
#
#         :arg item: The position to evaluate
#         :type item: Position
#
#         :returns: Whether to filter out or not
#         :rtype: bool
#         """
#         X_MIN_BOUND = Y_MIN_BOUND = 0
#         X_MAX_BOUND = len(graph[0]) - 1
#         Y_MAX_BOUND = len(graph) - 1
#
#         return (item.x >= X_MIN_BOUND and item.x <= X_MAX_BOUND) \
#             and (item.y >= Y_MIN_BOUND and item.y <= Y_MAX_BOUND) \
#             and (item not in step_history) and (item not in step_exclude)
#
#     print("Start:", start)
#     print("End:", end)
#     print()
#     while not finish:
#         current = step_history[-1]
#         current_letter = HEIGHT_MAP.index(graph[current.y][current.x])
#         next_letter = current_letter + 1
#
#         print("Step")
#         print("    Current:", current)
#         print("    Current Letter:", HEIGHT_MAP[current_letter])
#         print("    Next Letter:", HEIGHT_MAP[next_letter])
#
#
#         move_dir = [
#             # Move Up
#             Position(current.x, current.y-1),
#             # Go Down
#             Position(current.x, current.y+1),
#             # Go Right
#             Position(current.x+1, current.y),
#             # Go Left
#             Position(current.x-1, current.y),
#         ]
#
#         can_move = list(filter(
#             filter_out,
#             move_dir
#         ))
#
#         print("    Possible Positions:", can_move)
#
#         can_move_letters = [
#             HEIGHT_MAP.index(graph[move.y][move.x]) for move in can_move
#         ]
#
#         print("    Can Move Options:", [
#             HEIGHT_MAP[letter] for letter in can_move_letters
#         ])
#
#         try:
#             if next_letter in can_move_letters:
#                 next_position = can_move[can_move_letters.index(next_letter)]
#             else:
#                 next_position = can_move[can_move_letters.index(current_letter)]
#
#             print("    Move To:", graph[next_position.y][next_position.x])
#             print("    Next Position:", next_position)
#             step_history.append(next_position)
#         except ValueError:
#             # Step Back
#             step_history = [start]
#             print("Start Again:", step_history[0])
#             step_exclude.append(current)
#
#         if step_history[-1] == end:
#             finish = True
#
#     return len(step_history) - 1


def find_path(graph: list[list[str]], start: Position, end: Position) -> int:
    """Find a path through the graph to reach the end.

    :arg graph: The heightmap of the surrounding region.
    :type graph: list[list[str]]

    :arg start: The starting position in the graph.
    :type start: Position

    :arg end: The ending position in the graph.
    :type end: Position:

    :returns: The number of steps taken to reach the goal.
    :rtype: int
    """
    graph_2 = deepcopy(graph)

    for y, line in enumerate(graph_2):
        for x, item in enumerate(line):
            current = HEIGHT_MAP.index(item)
            surrounding = []

            # Find left:
            if x > 0:
                surrounding.append(
                    HEIGHT_MAP.index(graph_2[y][x-1])
                )

            # Find right:
            if x < len(line) - 1:
                surrounding.append(
                    HEIGHT_MAP.index(graph_2[y][x+1])
                )

            # Find Top
            if y > 0:
                surrounding.append(
                    HEIGHT_MAP.index(graph_2[y-1][x])
                )

            # Find Bottom
            if y < len(graph) - 1:
                surrounding.append(
                    HEIGHT_MAP.index(graph_2[y+1][x])
                )

            has_others = True

            print(y, x, surrounding)

            for other in surrounding:
                if other < current - 1 or other > current + 1:
                    has_others = False
                else:
                    has_others = True

            if has_others is False:
                graph_2[y][x] = "."

    with Path("./output.txt").open("w+") as _f:
        for line in graph_2:
            _f.write("".join(line) + "\n")

    return 0


def main() -> None:
    """The main program function."""
    raw_input: list[str] = read_input(INPUT_FILENAME)
    graph, start, end = find_positions(raw_input)

    print(find_path(raw_input, start, end))


if __name__ == "__main__":
    main()
