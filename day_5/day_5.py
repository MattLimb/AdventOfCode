"""Advent of Code - Day 5."""
import re
import shlex
from collections import namedtuple
from dataclasses import dataclass, field
from pathlib import Path
from queue import LifoQueue
from typing import Callable
from typing import NamedTuple


INPUT_FILENAME: Path = Path("./input.txt")

STACK_TYPE = dict[int, LifoQueue]
CRATE_REGEX = re.compile(r"(\[[A-Z]\])|(    )")
Instruction: NamedTuple = namedtuple("Instruction", ["amount", "start", "end"])


def parse_stacks(stacks: list[str]) -> STACK_TYPE:
    """Parse the stack lines in the input into a LifoQueue dictionary.

    :arg stacks: The lines from the input describing the stacks.
    :type stacks: list[str]

    :returns: A dictionary of LiFo Queues representing the stacks.
    :rtype: dict[int, LifoQueue]
    """
    stacks.reverse()
    stack_dict: STACK_TYPE = {
        int(num.strip()): LifoQueue() for num in stacks[0].strip().split("   ")
    }

    for index_item in stacks[1:]:
        crates = index_item.strip()

        findall = re.findall(CRATE_REGEX, crates)

        for idx, (crate, _) in enumerate(findall, start=1):
            if crate != "":
                # Only put the letter in the stack
                stack_dict[idx].put(crate[1])

    return stack_dict


def read_input(filename: Path) -> tuple[STACK_TYPE, list[str]]:
    """Read the input to the days challenge.

    :arg filename: The filename of the input.
    :type filename: pathlib.Path

    :returns: A list strings. One item per line.
    :rtype: list[str]
    """
    with filename.open("r", encoding="utf-8") as _file_handler:
        lines = _file_handler.readlines()

    seperator_index = lines.index("\n")

    # Remove newline characters
    instructions = [inst.strip() for inst in lines[seperator_index:]]

    stacks = parse_stacks(lines[:seperator_index])

    return (stacks, instructions)


def process_instrution(instruction: str) -> Instruction:
    """Process the instruction so that its usable by the code.

    :arg instruction: The string instruction presented in the input.
    :type instruction: str

    :returns: A tuple containing the amount of crates to move, the start and end stacks.
    :rtype: Instruction
    """
    split_instr = shlex.split(instruction)

    return Instruction(
        amount=int(split_instr[1]), start=int(split_instr[3]), end=int(split_instr[5])
    )


def get_top_stacks(stacks: STACK_TYPE) -> str:
    """Get the top item from each stack as a string.

    :arg stacks: The stacks to process.
    :type stacks: dict[int, LifoQueue]

    :returns: The string representing the top of each stack.
    :rtype: str
    """
    items: str = ""

    for stack in stacks.values():
        items += stack.get_nowait()

    return items


def part_1(stacks: STACK_TYPE, instructions: list[str]) -> str:
    """Process through the instructions - taking each move one at a time.

    :arg stacks: The lifo queues representing the container stacks.
    :type stacks: dict[int, LifoQueue]

    :arg instructions: The list of instructions to complete.
    :type instructions: list[str]

    :returns: The containers at the top of each stack.
    :rtype: str
    """
    for instr in instructions[1:]:
        instruction: Instruction = process_instrution(instr)

        for _ in range(instruction.amount):
            item: str = stacks[instruction.start].get()
            stacks[instruction.end].put(item)

    return get_top_stacks(stacks)


def part_2(stacks: STACK_TYPE, instructions: list[str]) -> str:
    """Process through the instructions - taking each move one at a time.

    :arg stacks: The lifo queues representing the container stacks.
    :type stacks: dict[int, LifoQueue]

    :arg instructions: The list of instructions to complete.
    :type instructions: list[str]

    :returns: The containers at the top of each stack.
    :rtype: str
    """
    for instr in instructions[1:]:
        instruction: Instruction = process_instrution(instr)

        move_items: list[str] = []

        for _ in range(instruction.amount):
            item: str = stacks[instruction.start].get_nowait()
            move_items.append(item)

        move_items.reverse()
        for item in move_items:
            stacks[instruction.end].put_nowait(item)

        move_items = []

    return get_top_stacks(stacks)


def main():
    """The main program function."""
    stacks, instructions = read_input(INPUT_FILENAME)

    print("Part 1:", part_1(stacks, instructions))

    # Ensure stacks are refilled to their prior state
    stacks, instructions = read_input(INPUT_FILENAME)
    print("Part 2:", part_2(stacks, instructions))


if __name__ == "__main__":
    main()
