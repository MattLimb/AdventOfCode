"""Advent of Code - Day 2."""
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Union


INPUT_FILENAME: Path = Path("./input.txt")


class Game(Enum):
    """Integer Enum for Rock Paper Scissors Game."""

    ROCK = 1
    PAPER = 2
    SCISSORS = 3


PART_1_GUESS_KEY: dict[str, Game] = {
    "A": Game.ROCK,
    "B": Game.PAPER,
    "C": Game.SCISSORS,
    "X": Game.ROCK,
    "Y": Game.PAPER,
    "Z": Game.SCISSORS,
}


PART_2_GUESS_KEY: dict[str, Game] = {
    "A": Game.ROCK,
    "B": Game.PAPER,
    "C": Game.SCISSORS,
}
PART_2_OUTCOME_KEY: dict[str, str] = {
    "X": "lose",
    "Y": "draw",
    "Z": "win",
}


def read_input(filename: Path) -> list[str]:
    """Read the input to the days challenge.

    :arg filename: The filename of the input.
    :type filename: pathlib.Path

    :returns: A list strings. One item per line.
    :rtype: list[str]
    """
    with filename.open("r", encoding="utf-8") as _file_handler:
        return _file_handler.readlines()


@lru_cache(maxsize=None)
def determine_player_score_1(elf: Game, player: Game) -> int:
    """Function to determine if the player wins, loses or draws."""
    # Draw Condition
    if elf == player:
        return 3 + player.value

    game_state: tuple[Game, Game] = (elf, player)

    # Winning combinations for player
    player_win_combos: list[tuple[Game, Game]] = [
        (Game.ROCK, Game.PAPER),
        (Game.PAPER, Game.SCISSORS),
        (Game.SCISSORS, Game.ROCK),
    ]

    # Check to see if the player won
    if game_state in player_win_combos:
        return 6 + player.value

    # If not a draw or win, must be a loss
    return 0 + player.value


@lru_cache(maxsize=None)
def determine_player_score_2(elf: Game, outcome: str) -> int:
    """Function to determine if the player wins, loses or draws."""
    # Draw Condition
    if outcome == "draw":
        return 3 + elf.value

    # Winning combinations for player
    win_combos: dict[Game, Game] = {
        Game.ROCK: Game.PAPER,
        Game.PAPER: Game.SCISSORS,
        Game.SCISSORS: Game.ROCK,
    }

    # Check to see if the player won
    if outcome == "win":
        return 6 + win_combos[elf].value

    lose_combos: dict[Game, Game] = {
        Game.ROCK: Game.SCISSORS,
        Game.PAPER: Game.ROCK,
        Game.SCISSORS: Game.PAPER,
    }

    # If not a draw or win, must be a loss
    return 0 + lose_combos[elf].value


def part_1(guide: list[str]) -> list[int]:
    """Process the stratergy guide into their score per game.

    :arg guide: The stratergy guide presented as a list of strings.
    :type guide: list[str]

    :returns: A list of the score result for each game, for me.
    :rtype: list[int]
    """
    outcomes: list[int] = []

    for game in guide:
        guesses: list[str] = game.strip().split(" ")

        elf_guess: Game = PART_1_GUESS_KEY[guesses[0]]
        player_guess: Game = PART_1_GUESS_KEY[guesses[-1]]

        # Determine Player Score
        outcomes.append(determine_player_score_1(elf_guess, player_guess))

    return outcomes


def part_2(guide: list[str]) -> list[int]:
    """Process the stratergy guide so the games equal the projected output.

    :arg guide: The stratergy guide presented as a list of strings.
    :type guide: list[str]

    :returns: A list of the score result for each game, for me.
    :rtype: list[int]
    """
    outcomes: list[int] = []

    for game in guide:
        guesses: list[str] = game.strip().split(" ")

        elf_guess: Game = PART_2_GUESS_KEY[guesses[0]]
        game_outcome: str = PART_2_OUTCOME_KEY[guesses[-1]]

        # Determine Player Score
        outcomes.append(determine_player_score_2(elf_guess, game_outcome))

    return outcomes


def main():
    """The main program function."""
    raw_input: list[str] = read_input(INPUT_FILENAME)

    print("Part 1:", sum(part_1(raw_input)))
    print("Part 2:", sum(part_2(raw_input)))


if __name__ == "__main__":
    main()
