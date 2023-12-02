import argparse
from collections import defaultdict
import re

import numpy as np


def part_1(file: str) -> tuple[list, int]:
    """Computes the sum of the IDs of game that would have been possible if the
    the bag contained only 12 red cubes, 13 green cubes, and 14 blue cubes.

    Args:
        file (str): Path to the puzzle input

    Returns:
        int: Total sum of IDs of games compatible.
    """
    max_per_color = {'red': 12, 'green': 13, 'blue': 14}

    def game_is_compatible(line: str) -> bool:
        """Check if game is compatible with constraints."""
        compatibilities = []
        for subset in line.split(";"):
            for color, max_val in max_per_color.items():
                res = re.findall(f"(\d+) {color}", subset)
                if len(res):
                    val = int(res[0])
                else:
                    val = 0
                compatibilities.append(val <= max_val)
        return all(compatibilities)

    compatible_ids = []
    with open(file) as f:
        for idx, line in enumerate(f.readlines()):
            game_id = idx + 1
            line = line.rstrip()
            if game_is_compatible(line):
                compatible_ids.append(game_id)

    return sum(compatible_ids)


def part_2(file: str) -> int:
    """Computes the power of a set of cubes after computing the mininal number
    of cubes per color needed to make each game possible.

    Args:
        file (str): Path to the puzzle input

    Returns:
        int: The sum of the powers computed on all games.
    """
    max_per_color = {'red': 12, 'green': 13, 'blue': 14}

    def minimum_number_of_cubes(line: str) -> list[int]:
        history = defaultdict(list)
        for subset in line.split(";"):
            for color, _ in max_per_color.items():
                res = re.findall(f"(\d+) {color}", subset)
                if len(res):
                    history[color].append(int(res[0]))
                else:
                    history[color].append(0)
        minimums = [max(values) for _, values in history.items()]
        return minimums

    powers = []
    with open(file) as f:
        for line in f.readlines():
            line = line.rstrip()
            powers.append(np.prod(minimum_number_of_cubes(line)))

    return sum(powers)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solves Day 2 puzzles")
    parser.add_argument("--file", type=str, help="Path to puzzle file")
    args = parser.parse_args()

    sol1 = part_1(file=args.file)
    sol2 = part_2(file=args.file)

    print(f"Part 1 solution: {sol1}")
    print(f"Part 2 solution: {sol2}")
