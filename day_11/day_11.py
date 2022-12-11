"""Advent of Code - Day 11."""
from dataclasses import dataclass, field
from pathlib import Path
from queue import SimpleQueue


INPUT_FILENAME: Path = Path("./input.txt")
PART_1_ROUNDS: int = 20
PART_2_ROUNDS: int = 10_000


@dataclass
class Monkey:
    """A class representing a monkey."""

    operation: str = field(default="", init=False)
    test: str = field(default="", init=False)
    results: dict[bool, int] = field(default_factory=dict, init=False)
    items: SimpleQueue = field(default_factory=SimpleQueue, init=False)
    processed: int = field(default=0, init=False)
    prod_divisors: int = 0

    def process(self, part: int = 1) -> tuple[int, int]:
        """Process the first item in the Monkey's posetion.

        :arg part: Which part of the challenge this is.
        type: part: int

        :returns: The new worry level for the item and the monkey to throw too.
        :rtype: tuple[int, int]
        """
        old: int = self.items.get_nowait()  # type: ignore

        test_num = int(self.test.split(" ")[-1])

        worry = eval(self.operation)

        if part == 1:
            worry = worry // 3
        else:
            worry = worry % self.prod_divisors

        throw_to = self.results[worry % test_num == 0]

        self.processed += 1
        return worry, throw_to


def read_input(filename: Path) -> list[str]:
    """Read the input to the days challenge.

    :arg filename: The filename of the input.
    :type filename: pathlib.Path

    :returns: A list strings. One item per line.
    :rtype: list[str]
    """
    with filename.open("r", encoding="utf-8") as _file_handler:
        return _file_handler.readlines()


def process_input(monkey_list: list[str]) -> dict[int, Monkey]:
    """Process the input into a dictionary of monkeys.

    :arg monkey_list: The raw input read in from the text file.
    :type monkey_list: list[str]

    :returns: A dictionary representing each monkey.
    :rtype: dict[int, Monkey]
    """
    monkeys: dict[int, Monkey] = {}
    curr_monkey: int = 0
    prod_divisors: int = 1

    for line in monkey_list:
        if "Monkey" in line:
            _, number_str = line.split(" ")
            number: int = int(number_str[:-2])
            monkeys[number] = Monkey()
            curr_monkey = number
        elif "Starting items" in line:
            _, items = line.split(":")

            for item in items.split(","):
                monkeys[curr_monkey].items.put_nowait(int(item.strip()))
        elif "Operation" in line:
            _, operation = line.split(":")
            monkeys[curr_monkey].operation = operation.strip().split("=")[1]

        elif "Test" in line:
            _, test = line.split(":")
            monkeys[curr_monkey].test = test.strip()
            prod_divisors *= int(test.split(" ")[-1])
        elif "If true" in line:
            _, throw = line.split(":")
            monkeys[curr_monkey].results[True] = int(throw.strip().split(" ")[-1])
        elif "If false" in line:
            _, throw = line.split(":")
            monkeys[curr_monkey].results[False] = int(throw.strip().split(" ")[-1])

    for monkey in monkeys.values():
        monkey.prod_divisors = prod_divisors

    return monkeys


def run_rounds(monkeys: dict[int, Monkey], rounds: int, part: int = 1) -> int:
    """Calculate the level of Monkey Business there has been.

    :arg monkeys: The dictionary of monkeys.
    :type monkeys: dict[int, Monkey]

    :arg rounds: The number of rounds to run.
    :type rounds: int

    :arg part: The part of the challenge beign run.
    :type part: int

    :returns: The Monkey Business Score
    :rtype: int
    """
    for r in range(0, rounds):
        for monkey in monkeys.values():
            while monkey.items.qsize() != 0:
                item, new_monkey = monkey.process(part=part)

                monkeys[new_monkey].items.put_nowait(item)

    monkey_business = sorted([m.processed for m in monkeys.values()], reverse=True)

    return monkey_business[0] * monkey_business[1]


def main() -> None:
    """The main program function."""
    raw_input: list[str] = read_input(INPUT_FILENAME)
    monkeys = process_input(raw_input)
    monkeys_2 = process_input(raw_input)

    print("Part 1:", run_rounds(monkeys, PART_1_ROUNDS, 1))
    print("Part 2:", run_rounds(monkeys_2, PART_2_ROUNDS, 2))


if __name__ == "__main__":
    main()
