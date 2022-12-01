"""Advent of Code - Day 1."""
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
        return _file_handler.readlines()


def group_input(input: list[str]) -> list[list[int]]:
    """Process the raw list into a list of lists representing the calories each elf is carrying.

    :arg input: The raw input read in from the input file.
    :type input: list[str]

    :returns: A list of lists. Each sublist contains the calorie values for a single elf as integers.
    :rtype: list[list[int]]
    """
    all_lists: list[list[int]] = []
    current_elf: list[int] = []

    for cal in input:
        if cal == "\n":
            # Append the current elf to all lists.
            all_lists.append(current_elf)
            # Make current elf empty again.
            current_elf = []

        else:
            # Strip of the newline.
            cal = cal.strip()
            # Convert to int and add to current_elf list.
            current_elf.append(int(cal))

    return all_lists


def find_most_cals(grouped_input: list[list[int]]) -> list[int]:
    """Find the elf carrying the most calories.

    :arg grouped_input: The list of lists representing the calorie values for each elf.
    :type grouped_input: list[list[int]]

    :returns: A list of integers. Each integer representing the total number of calories a single elf is carrying.
    :rtype: list[int]
    """
    sum_cals: list[int] = [sum(inp) for inp in grouped_input]

    return sorted(sum_cals, reverse=True)


def main():
    """The main program function."""
    raw_input: list[str] = read_input(INPUT_FILENAME)

    # Group raw input into what each elf is carrying.
    grouped_input: list[list[int]] = group_input(raw_input)

    # Sum up the calories of each elf and sort them from most to least.
    sorted_cals: list[int] = find_most_cals(grouped_input)

    # The highest amount of calories a single elf is carrying.
    part_1: int = sorted_cals[0]
    # The total number of calories the top 3 elves are carrying.
    part_2: int = sum(sorted_calcs[0:3])

    # Display the results to the user
    print("Part 1:", part_1)
    print("Part 2:", part_2)



if __name__ == "__main__":
    main()
