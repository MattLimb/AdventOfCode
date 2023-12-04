"""Advent of Code - Day 4."""
from pathlib import Path

INPUT_FILENAME: Path = Path("./input.txt")

def read_input(filename: Path) -> list[str]:
    """Read the input to the days challenge.

    :arg filename: The filename of the input.
    :type filename: pathlib.Path

    :returns: A list strings. One item per line.
    :rtype: list[str]
    """
    with filename.open("r", encoding="utf-8") as _file_handler:
        return [ line.strip() for line in _file_handler.readlines() if len(line) != 0]


def process_scratch_cards(input_list: list[str]) -> list[tuple[int, list[int], list[int]]]:
    """Process the scratchcards into a more useful format.

    :arg input_list: The list of scratchcards as formatted in the text file.
    :type input_list: list[str]

    :returns: The scratchcards as a tuple featuring the game number, the card
        numbers and the comparision numbers.
    :rtype: list[tuple[int, list[int], list[int]]]
    """
    output: list[tuple[int, list[int], list[int]]] = []

    for card in input_list:
        game, parts = card.split(":")

        _, gn = game.strip().split(" ", 1)

        pt_1, pt_2 = parts.strip().split("|")

        pt_1 = [int(i.strip()) for i in pt_1.strip().split(" ") if i != ""]
        pt_2 = [int(i.strip()) for i in pt_2.strip().split(" ") if i != ""]

        output.append((
            int(gn.strip()),
            pt_1,
            pt_2
        ))

    return output

def incrament_score(old_score: int=0) -> int:
    """Incrament the score for a scratchcard.

    :arg old_score: The current score to update.
    :type old_score: int

    :returns: The new score as an integer.
    :rtype: int
    """
    if old_score == 0:
        return 1

    return old_score * 2


def part_1(input_cards: list[tuple[int, list[int], list[int]]]) -> list[int]:
    """Parse through the cards to calculate scores.

    :arg input_grid: The Cards to use as input.
    :type input_grid: list[tuple[int, list[int], list[int]]]

    :returns: All part numbers in the grid.
    :rtype: list[int]
    """
    output: list[int] = []

    for _, set_1, set_2 in input_cards:
        score = 0

        for num in set_1:
            if num in set_2:
                score = incrament_score(score)

        output.append(score)

    return output


def part_2(input_cards: list[tuple[int, list[int], list[int]]]) -> list[int]:
    """Parse through the cards to calculate scores.

    :arg input_grid: The Cards to use as input.
    :type input_grid: list[tuple[int, list[int], list[int]]]

    :returns: The GameIDs of the winning cards.
    :rtype: list[int]
    """
    output_cards: list[int] = [ c[0] for c in input_cards ]
    output_wins: dict[int, list[int]] = {}

    for cid, set_1, set_2 in input_cards:
        wins = 0

        for num in set_1:
            if num in set_2:
                wins += 1

        output_wins[cid] = []

        for idx in range(cid+1, (cid+wins)+1):
            output_wins[cid].append(idx)

    for i in output_cards:
        output_cards.extend(output_wins[i])

    return output_cards


if __name__ == "__main__":
    puzzle_input: list[str] = read_input(INPUT_FILENAME)
    processed_input: list[tuple[int, list[int], list[int]]] = process_scratch_cards(puzzle_input)

    print("Part 1:", sum(part_1(processed_input)))
    print("Part 2:", len(part_2(processed_input)))
