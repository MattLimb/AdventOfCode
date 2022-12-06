"""Advent of Code - Day 5."""
from pathlib import Path


INPUT_FILENAME: Path = Path("./input.txt")


def read_input(filename: Path) -> str:
    """Read the input to the days challenge.

    :arg filename: The filename of the input.
    :type filename: pathlib.Path

    :returns: A list strings. One item per line.
    :rtype: list[str]
    """
    with filename.open("r", encoding="utf-8") as _file_handler:
        return _file_handler.read().strip()


def find_packet(datastream: str, unique_items: int) -> int:
    """Find the index in the datastream where the last unique_items is unique.

    :arg datastream: The datastream as a string.
    :type datastream: str

    :arg unique_items: The number of unique items in a row are required for packet detection.
    :type unique_items: int

    :returns: The index where the start of datastream packet ends.
    :rtype: int
    """

    last_index: int = 0

    for idx, character in enumerate(datastream):
        # Ignore the first 4 index items.
        if idx >= (unique_items - 1):
            # Create a set with the last 4 characters from the datastream.
            char_set: set[str] = {
                datastream[step] for step in range(idx, idx - unique_items, -1)
            }

            # If the set has length of unique_items - all items are unique.
            if len(char_set) == unique_items:
                # Set the last_index as a if counting from 1 not 0.
                last_index = idx + 1
                break

    return last_index


def main():
    """The main program function."""
    datastream = read_input(INPUT_FILENAME)

    # Find packet start
    print("Part 1:", find_packet(datastream, 4))

    # Find message start
    print("Part 2:", find_packet(datastream, 14))


if __name__ == "__main__":
    main()
