import argparse
import collections
from typing import NamedTuple


class Interval(NamedTuple):
    start: int
    end: int


def parse_seeds_and_mappings(file: str) -> tuple[list[int], dict]:
    """Parse input file and creates mappings for each component."""

    KEYS = [
        "seed-to-soil",
        "soil-to-fertilizer",
        "fertilizer-to-water",
        "water-to-light",
        "light-to-temperature",
        "temperature-to-humidity",
        "humidity-to-location",
    ]
    mappings = collections.defaultdict(list)
    to_add = False
    with open(file) as f:
        while (line := f.readline()):
            if 'seeds' in line:
                line = line.rstrip()
                line = line.replace("seeds: ", "")
                seeds = [int(n) for n in line.split()]
                continue
            if 'map' in line:
                name = [map for map in KEYS if map in line][0]
                to_add = True

            if to_add and 'map' not in line and line != "\n":
                mappings[name].append([int(n) for n in line.rstrip().split()])
            if to_add and line == "\n":
                to_add = False
    return seeds, mappings


def converts_value(value: int, instructions: list[list[int]]) -> int:
    """Given a value and a list of instructions from a mapping, computes the
    transformed value."""
    new_val = None
    for target, source, offset in instructions:
        if value >= source and value <= source + offset:
            new_val = target + (value-source)
            break
    if new_val is None:
        return value
    else:
        return new_val


def pairwise(seeds):
    "Iterates over a list taking two-elements at a time with no overlap."
    a = iter(seeds)
    return zip(a, a)


def split_interval(
        input_interval: Interval,
        instructions: list[list[int]]) -> list[Interval]:
    """Transforms an interval of integers into a list of intervals that have
    been mapped according to the instructions given."""
    to_visit = [input_interval]
    transformed = []
    already_treated = collections.defaultdict(set)

    while to_visit:
        curr_interval = to_visit.pop(0)
        seed_max, seed_min = curr_interval.end, curr_interval.start

        for idx, (target, source, size) in enumerate(instructions):
            start, end = source, source + size - 1

            if seed_max < start or end < seed_min:
                if curr_interval not in already_treated[idx]:
                    to_visit.append(curr_interval)
                    already_treated[idx].add(curr_interval)
                continue

            elif seed_min < start and seed_max < end:
                out_interval, in_interval = (
                    Interval(seed_min, start-1),
                    Interval(target, target + seed_max - start),
                )
                if curr_interval not in already_treated[idx]:
                    to_visit.append(out_interval)
                    already_treated[idx].add(out_interval)
                transformed.append(in_interval)
                continue

            elif seed_min < start and end < seed_max:
                out1, in_interval, out2 = (
                    Interval(seed_min, start-1),
                    Interval(target, target + end-start),
                    Interval(end + 1, seed_max),
                )
                for out in [out1, out2]:
                    if out not in already_treated[idx]:
                        to_visit.append(out)
                        already_treated[idx].add(out)
                transformed.append(in_interval)
                continue

            elif start <= seed_min and seed_max <= end:
                transformed.append(
                    Interval(target + seed_min-start, target + seed_max-start))
                continue

            elif start <= seed_min and end < seed_max:
                in_interval, out_interval = (
                    Interval(target + seed_min - start, target + end-start),
                    Interval(end + 1, seed_max),
                )
                if out_interval not in already_treated[idx]:
                    to_visit.append(out_interval)
                    already_treated[idx].add(out_interval)
                continue

        if all([curr_interval in already_treated[idx]
                for idx in range(len(instructions))]):
            transformed.append(curr_interval)

    return list(set(transformed))


def part_1(file: str) -> int:
    """Computes the lowest location number obtained with the input seeds.

    Args:
        file (str): Path to the puzzle input

    Returns:
        int: Lowest location number obtained.
    """
    seeds, mappings = parse_seeds_and_mappings(file)

    locations = []
    for seed in seeds:
        val = seed
        for mapping in mappings:
            val = converts_value(val, mappings[mapping])
        locations.append(val)
    return min(locations)


def part_2(file: str) -> int:
    """Computes the lowest location number obtained with the input seed ranges.

    Args:
        file (str): Path to the puzzle input

    Returns:
        int: Lowest location number obtained.
    """
    seeds, mappings = parse_seeds_and_mappings(file)

    per_range_minimums = []
    for seed, nb_seeds in pairwise(seeds):
        input_interval = Interval(seed, seed + nb_seeds - 1)
        intervals = [input_interval]
        for _, instructions in mappings.items():
            tmp_intervals = []
            for interval in intervals:
                tmp_intervals.extend(split_interval(interval, instructions))
            intervals = tmp_intervals
        per_range_minimums.append(
            min(interval.start for interval in intervals))
    return min(per_range_minimums)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solves Day 5 puzzles")
    parser.add_argument("--file", type=str, help="Path to puzzle file")
    args = parser.parse_args()

    sol1 = part_1(file=args.file)
    sol2 = part_2(file=args.file)

    print(f"Part 1 solution: {sol1}")
    print(f"Part 2 solution: {sol2}")
