"""Advent of Code - Day 7."""
from dataclasses import dataclass, field
from pathlib import Path
from shlex import split as shlex_split
from typing import Optional, Union


INPUT_FILENAME: Path = Path("./input.txt")
UP_DIR: str = ".."
ROOT_DIR: str = "/"
COMMAND_START: str = "$"
DIR_START: str = "dir"

INDENT: str = "  "
MAX_SIZE: int = 100_000

DELETE_MIN: int
DELETE_MAX: int

TOTAL_DISK: int = 70_000_000
TARGET_UNUSED: int = 30_000_000


@dataclass
class Directory:
    """Class representing a directory."""

    name: str
    children: dict[str, Union["Directory", "File"]] = field(default_factory=dict)
    _is_dir: bool = True

    @property
    def size(self) -> int:
        """Get the size of the current folder."""
        size: int = 0

        for item in self.children.values():
            size += item.size

        return size

    def get_dirs(self) -> list["Directory"]:
        """Get the directories this folder contains, and all folders it contains.

        :returns: A list of all folders within this directory
        :rtype: list[Directory]
        """
        output: list["Directory"] = [self]

        for item in self.children.values():
            if isinstance(item, type(self)):
                output.extend(item.get_dirs())

        return output

    def append(self, sub: list[str], item: Union["Directory", "File"]) -> None:
        """Append an item to the sub directory.

        :arg sub: A list containing the subdirectories to check.
        :type sub: list[str]

        :arg item: The item to append to the subdirectory.
        :type item: Union[Directory, File]

        :returns: Nothing
        :rtype: None
        """
        direc: "Directory" = self

        for fol in sub:
            tmp: Union["Directory", "File"] = direc.children[fol]

            if isinstance(tmp, File):
                raise ValueError("Cannot append to a file.")
            else:
                direc = tmp

        direc.children[item.name] = item

    def exists(self, sub: list[str]) -> bool:
        """Check to see if a subdirectory exists at the chosen level.

        :arg sub: A list containing the subdirectories to check.
        :type sub: list[str]

        :returns: If the sub exists in the structure.
        :rtype: bool
        """
        traversal: Union[Directory, File] = self
        result: bool = True

        for idx, item in enumerate(sub, start=1):
            if isinstance(traversal, File):
                if idx != len(sub):
                    result = False

                break
            else:
                if item not in traversal.children:
                    result = False
                    break
                else:
                    traversal = traversal.children[item]

        return result

    def structure(self, indent: int = 0) -> str:
        """Get the folder structure in a easy to view mannar.

        :arg indent: The number of indents to add before printing the structure.
        :type indent: int

        :returns: The structure as a string.
        :rtype: str
        """
        structure = f"""{INDENT*indent} - {str(self)}"""

        for child in self.children.values():
            structure += f"\n{child.structure(indent+1)}"

        return structure

    def __str__(self):
        """Stringify the directory."""
        return f"{self.name} (dir)"


@dataclass
class File:
    """Class representing a file."""

    name: str
    size: int
    _is_dir: bool = False

    def structure(self, indent: int = 0) -> str:
        """Get the folder structure in a easy to view mannar.

        :arg indent: The number of indents to add before printing the structure.
        :type indent: int

        :returns: The structure as a string.
        :rtype: str
        """
        return f"{INDENT*indent} - {str(self)}"

    def __str__(self):
        """Stringify the directory."""
        return f"{self.name} (file, size={self.size})"


def read_input(filename: Path) -> list[str]:
    """Read the input to the days challenge.

    :arg filename: The filename of the input.
    :type filename: pathlib.Path

    :returns: A list strings. One item per line.
    :rtype: list[str]
    """
    with filename.open("r", encoding="utf-8") as _file_handler:
        return [line.strip() for line in _file_handler.readlines()]


def process_commands(command_list: list[str]) -> Directory:
    """Process the commands given as input into a directory structure.

    :arg command_list: The command and command output list.
    :type command_list: list[str]

    :returns: A Directory instance containing the directory structure.
    :rtype: Directory
    """
    root: Directory = Directory(name=ROOT_DIR)

    current_dir: list[str] = []

    for output in command_list:
        split_line = shlex_split(output)

        if split_line[0] == COMMAND_START:
            if split_line[1] == "cd":
                if split_line[2] == UP_DIR:
                    current_dir.pop()
                elif split_line[2] == ROOT_DIR:
                    current_dir = []
                else:
                    current_dir.append(split_line[2])
        else:
            if split_line[0] == DIR_START:
                root.append(current_dir, Directory(name=split_line[1]))
            else:
                root.append(
                    current_dir, File(name=split_line[1], size=int(split_line[0]))
                )

    return root


def get_folder_sizes(root: Directory) -> list[tuple[str, int]]:
    """Get the recursive folder size of each directory inside it.

    :arg root: The root directory
    :type: root: Directory

    :returns: A list of pairs - the directory name and its size.
    :rtype: list[tuple[str, int]]
    """
    output: list[tuple[str, int]] = []

    for direc in root.get_dirs():
        output.append((direc.name, direc.size))

    return output


def part_1(folder_sizes: list[tuple[str, int]]) -> int:
    """Calculate the folders with the biggest files in them.

    :arg folder_sizes: Each folder with their approved size.
    :type: folder_sizes: list[tuple[str, int]]

    :returns: The total of folders with a size of at least 100_000.
    :rtype: int
    """
    total: int = 0

    for (_, size) in folder_sizes:
        if size <= MAX_SIZE:
            total += size

    return total


def part_2(folder_sizes: list[tuple[str, int]]) -> int:
    """Calculate the folders with the biggest files in them.

    :arg folder_sizes: Each folder with their approved size.
    :type: folder_sizes: list[tuple[str, int]]

    :returns: The total of folders with a size of at least 100_000.
    :rtype: int
    """
    folder_sizes = sorted(folder_sizes, key=lambda tup: tup[1])
    total_consumed_space: int = folder_sizes[-1][-1]

    current_unused: int = TOTAL_DISK - total_consumed_space
    target_necessary: int = TARGET_UNUSED - current_unused

    for (_, size) in folder_sizes:
        if size >= target_necessary:
            return size

    return 0


def main() -> None:
    """The main program function."""
    raw_input = read_input(INPUT_FILENAME)

    root: Directory = process_commands(raw_input)
    folder_sizes: list[tuple[str, int]] = get_folder_sizes(root)

    print("Part 1:", part_1(folder_sizes))
    print("Part 2:", part_2(folder_sizes))


if __name__ == "__main__":
    main()
