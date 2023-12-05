"""Advent of Code - Day 5."""
from pathlib import Path
from typing import TypedDict

INPUT_FILENAME: Path = Path("./input.txt")


class SeedMaps(TypedDict):
    """Dictionary representing the various maps necessary for seeds."""
    seeds: list[int]
    seed_to_soil: list[tuple[tuple[int, int], int]]
    soil_to_fertilizer: list[tuple[tuple[int, int], int]]
    fertilizer_to_water: list[tuple[tuple[int, int], int]]
    water_to_light: list[tuple[tuple[int, int], int]]
    light_to_temperature: list[tuple[tuple[int, int], int]]
    temperature_to_humidity: list[tuple[tuple[int, int], int]]
    humidity_to_location: list[tuple[tuple[int, int], int]]

def read_input(filename: Path) -> list[str]:
    """Read the input to the days challenge.

    :arg filename: The filename of the input.
    :type filename: pathlib.Path

    :returns: A list strings. One item per line.
    :rtype: list[str]
    """
    with filename.open("r", encoding="utf-8") as _file_handler:
        return [ line.strip() for line in _file_handler.readlines() if len(line) != 0]


def process_input(raw_input: list[str]) -> SeedMaps:
    """Take the raw input of the file, and convert the maps to useful dicts.

    :arg raw_input: The raw file input.
    :type raw_input: list[str]

    :returns: The seed maps filled out with the maps.
    :rtype: SeedMaps
    """
    seed_maps: SeedMaps = {
        "seeds": [],
        "seed_to_soil": [],
        "soil_to_fertilizer": [],
        "fertilizer_to_water": [],
        "water_to_light": [],
        "light_to_temperature": [],
        "temperature_to_humidity": [],
        "humidity_to_location": [],
    }

    idx = 0

    while idx < len(raw_input):
        line = raw_input[idx]

        if "seeds" in line:
            nums = line.split(":")[-1].strip()
            seed_maps["seeds"] = [int(num.strip()) for num in nums.split(" ") if len(num) > 0]

        if "map:" in line:
            name = line.split("map:")[0].strip().replace("-", "_")
            idx += 1

            while idx < len(raw_input) and (line := raw_input[idx]) != "":
                nums = [int(num.strip()) for num in line.split(" ") if len(num) > 0]

                seed_maps[name].append((
                    (nums[1], nums[1]+nums[-1]),
                    nums[0]
                ))

                idx += 1

        idx += 1

    return seed_maps


def process_number(map: list[tuple[tuple[int, int], int]], input_number: int) -> int:
    """Convert an input number according to a map.

    :arg map: The input mappings.
    :type: map: list[tuple[tuple[int, int], int]]

    :arg input_number: The number to process.
    :type input_number: int

    :returns: The mapped value.
    :rtype: int
    """
    for ((in_st, in_end), out_start) in map:
        if input_number >= in_st and input_number <= in_end:
            in_diff = input_number - in_st

            return out_start + in_diff

    return input_number


def part_1(maps: SeedMaps) -> int:
    """Process the seeds through the seed maps.
    
    :arg maps: The seed maps to use in the mapping.
    :type maps: SeedMaps

    :returns: The lowest location possible.
    :rtype: int
    """
    final_locations: list[int] = []
    process_key_order: list[str] = [
        "seed_to_soil",
        "soil_to_fertilizer",
        "fertilizer_to_water",
        "water_to_light",
        "light_to_temperature",
        "temperature_to_humidity",
        "humidity_to_location",
    ]

    for seed in maps["seeds"]:
        tmp_value = seed
        for key in process_key_order:
            tmp_value = process_number(maps[key], tmp_value)

        final_locations.append(tmp_value)

    return min(final_locations)


def part_2(maps: SeedMaps) -> int:
    """Process the seeds through the seed maps.

    :arg maps: The seed maps to use in the mapping.
    :type maps: SeedMaps

    :returns: The lowest location possible.
    :rtype: int
    """
    final_locations: list[int] = []
    process_key_order: list[str] = [
        "seed_to_soil",
        "soil_to_fertilizer",
        "fertilizer_to_water",
        "water_to_light",
        "light_to_temperature",
        "temperature_to_humidity",
        "humidity_to_location",
    ]


    batched_seeds: list[list[int]] = [
        maps["seeds"][idx:idx+2] for idx in range(0, len(maps["seeds"]), 2)
    ]

    all_seeds = []

    for (start, length) in batched_seeds:
        all_seeds.extend(list(range(start, start+length)))

    # for seed in all_seeds:
    tmp_value = 82
    for key in process_key_order:
        tmp_value = process_number(maps[key], tmp_value)

    final_locations.append(tmp_value)

    return min(final_locations)


if __name__ == "__main__":
    puzzle_input: list[str] = read_input(INPUT_FILENAME)

    proc_seed_maps: SeedMaps = process_input(puzzle_input)

    # print("Part 1:", part_1(proc_seed_maps))
    print("Part 2:", part_2(proc_seed_maps))

