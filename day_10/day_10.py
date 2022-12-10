"""Advent of Code - Day 10."""
from dataclasses import dataclass, field
from pathlib import Path

INPUT_FILENAME: Path = Path("./input.txt")
INSTRUC_LIST_TYPE = list[str]
INSTRUC_SEP: str = " "
DRAW_POSITIVE_CHAR: str = "#"
DRAW_NEGATIVE_CHAR: str = " "


@dataclass
class CPU:
    reg_x: int = 1
    ready: bool = True
    current_instruction: str = ""
    clock_since_instr: int = 0

    def set_instruction(self, instruction: str) -> None:
        """Set the CPU to run an instruction.

        :arg instruction: Set the CPU instruction.
        :type instruction: str
        """
        self.current_instruction = instruction
        self.ready = False
        self.clock_since_instr = 0

    def clear_instruction(self) -> None:
        """Clear the instruction and ready the CPU."""
        self.current_instruction = ""
        self.clock_since_instr = 0
        self.ready = True

    def tick(self) -> None:
        """Tick the CPU clock."""
        if "addx" in self.current_instruction:
            if self.clock_since_instr == 1:
                _, num = self.current_instruction.split(INSTRUC_SEP)
                self.reg_x += int(num)
                self.clear_instruction()
            else:
                self.clock_since_instr += 1
        else:
            self.clear_instruction()


def read_input(filename: Path) -> list[str]:
    """Read the input to the days challenge.

    :arg filename: The filename of the input.
    :type filename: pathlib.Path

    :returns: A list strings. One item per line.
    :rtype: list[str]
    """
    with filename.open("r", encoding="utf-8") as _file_handler:
        return [line.strip() for line in _file_handler.readlines()]


def simulate_cpu(instructions: list[str]) -> tuple[int, str]:
    """Simulate the CPU and calculate the signal strength.

    :arg instructions: The list of instructions to process each CPU instruction.
    :type tree_rows: list[list[int]]

    :returns: An integer representing the combined signal strength.
    :rtype: int
    """
    monitor_cycle: int = 20
    new_crt_row: int = 40

    cpu = CPU()
    clock_cycle: int = 0

    crt: list[str] = [""]

    signal_strengths: list[int] = []

    for instruction in instructions:
        cpu.set_instruction(instruction)

        while not cpu.ready:
            clock_cycle += 1

            if clock_cycle == monitor_cycle:
                signal_strengths.append(clock_cycle * cpu.reg_x)
                monitor_cycle += 40

            sprite_pos: list[int] = [
                cpu.reg_x - 1,
                cpu.reg_x,
                cpu.reg_x + 1,
            ]

            if len(crt[-1]) in sprite_pos:
                crt[-1] += DRAW_POSITIVE_CHAR
            else:
                crt[-1] += DRAW_NEGATIVE_CHAR

            if clock_cycle == new_crt_row:
                crt.append("")
                new_crt_row += 40

            cpu.tick()

    return sum(signal_strengths), "\n".join(crt)


def main() -> None:
    """The main program function."""
    raw_input: list[str] = read_input(INPUT_FILENAME)
    part_1, part_2 = simulate_cpu(raw_input)

    print("Part 1:", part_1)
    print(f"Part 2:\n{part_2}")


if __name__ == "__main__":
    main()
