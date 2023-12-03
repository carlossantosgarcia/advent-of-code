import argparse
from collections import defaultdict
import re

import numpy as np


def create_array_from_schematic(doc: list[str]):
    """Create array from the engine schematic with one character per entry."""
    map = np.zeros((len(doc), len(doc[0])), dtype=str)
    N, M = map.shape
    for i in range(N):
        for j in range(M):
            map[i][j] = doc[i][j]
    return map


def map_and_group_values(doc: list[str], map: np.ndarray):
    """Stores in two dictionaries the total number a tuple of indices belong to
    and, for each number, the list of tuples containing its different digits."""
    pattern = r'\d+'
    idx_to_number = {}
    number_to_coords = defaultdict(list)
    for idx, line in enumerate(doc):
        res = [(match.group(), match.start())
               for match in re.finditer(pattern, line)]
        if res:
            for num, start in res:
                for k in range(len(num)):
                    idx_to_number[(idx, start + k)] = int(num)
                number_to_coords[int(num)].append(
                    [(idx, start + k) for k in range(len(num))])
    return idx_to_number, number_to_coords


def is_symbol(value):
    """Return true if value is a symbol different from a digit or a dot."""
    pattern = "[^0-9.]"
    return bool(len(re.findall(pattern, value)))


def get_neighborhood(map: np.ndarray, i: int, j: int):
    """Retrieves neighbor indices from the entry (i, j) of map if they contain
    digits."""
    neighbors = []
    N, M = map.shape
    for x in range(max(0, i - 1), min(N, i + 2)):
        for y in range(max(0, j - 1), min(M, j + 2)):
            if (x, y) != (i, j):
                if re.findall("\d+", map[x][y]):
                    neighbors.append((x, y))
    return neighbors


def part_1(file: str) -> tuple[list, int]:
    """Computes the sum of 'part numbers' from the engine schematic.

    Args:
        file (str): Path to the puzzle input

    Returns:
        int: Total sum of part numbers.
    """
    doc = np.loadtxt(file, dtype=str, comments=None)
    map = create_array_from_schematic(doc)
    idx_to_number, number_to_coords = map_and_group_values(doc, map)

    N, M = map.shape
    num_parts, seen_coords = [], []
    for i in range(N):
        for j in range(M):
            if is_symbol(map[i][j]):
                neighbours = get_neighborhood(map, i, j)
                if neighbours:
                    for x, y in neighbours:
                        val = idx_to_number[(x, y)]
                        for curr_coords in number_to_coords[val]:
                            if (x, y) in curr_coords:
                                break
                        if any([c in seen_coords for c in curr_coords]):
                            continue
                        else:
                            num_parts.append(val)
                            seen_coords.append((x, y))

    return sum(num_parts)


def part_2(file: str) -> int:
    """Computes the sum of gear ratios from a engine schematic.

    Args:
        file (str): Path to the puzzle input

    Returns:
        int: The sum of the gear ratios.
    """
    doc = np.loadtxt(file, dtype=str, comments=None)
    map = create_array_from_schematic(doc)
    idx_to_number, number_to_coords = map_and_group_values(doc, map)

    N, M = map.shape
    gear_ratios = []
    for i in range(N):
        for j in range(M):
            if map[i][j] == "*":
                neighbours = get_neighborhood(map, i, j)
                if neighbours:
                    value_groups = []
                    for x, y in neighbours:
                        val = idx_to_number[(x, y)]
                        for curr_coords in number_to_coords[val]:
                            if (x, y) in curr_coords:
                                break
                        if curr_coords not in value_groups:
                            value_groups.append(curr_coords)
                    if len(value_groups) == 2:
                        gear_ratios.append(
                            int(idx_to_number[value_groups[0][0]]) *
                            int(idx_to_number[value_groups[1][0]]))

    return sum(gear_ratios)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solves Day 3 puzzles")
    parser.add_argument("--file", type=str, help="Path to puzzle file")
    args = parser.parse_args()

    sol1 = part_1(file=args.file)
    sol2 = part_2(file=args.file)

    print(f"Part 1 solution: {sol1}")
    print(f"Part 2 solution: {sol2}")
