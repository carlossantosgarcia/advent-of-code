import argparse
import math
import numpy as np
import re


def count_nb_of_wins(time: int, distance: int):
    """Counts the number of wins beating the record in a particular race."""
    root1 = time / 2 - (math.sqrt(time**2 - 4 * distance)) / 2
    mid = time / 2
    root2 = root1 + 2 * (mid - root1)
    return math.ceil(root2) - math.floor(root1) - 1


def part_1(file: str) -> int:
    """Computes the product of the number of wins from a list of races.

    Args:
        file (str): Path to the puzzle input

    Returns:
        int: product of the number of ways to beat each race's record.
    """
    with open(file) as f:
        while (line := f.readline()):
            if "Time" in line:
                line = line.replace("Time: ", "")
                times = [int(n) for n in re.findall("(\d+)", line)]
            elif "Distance" in line:
                line = line.replace("Distance: ", "")
                distances = [int(n) for n in re.findall("(\d+)", line)]
    wins = []
    for time, distance in zip(times, distances):
        wins.append(count_nb_of_wins(time, distance))

    return np.prod(wins)


def part_2(file: str) -> int:
    """Computes the the total number of wins beating the record from a race.

    Args:
        file (str): Path to the puzzle input

    Returns:
        int: Number of ways to beat the record in the particular race.
    """
    with open(file) as f:
        while (line := f.readline()):
            if "Time" in line:
                line = line.replace("Time: ", "").replace(" ", "")
                time = [int(n) for n in re.findall("(\d+)", line)]
            elif "Distance" in line:
                line = line.replace("Distance: ", "").replace(" ", "")
                distance = [int(n) for n in re.findall("(\d+)", line)]
    return count_nb_of_wins(*time, *distance)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solves Day 6 puzzles")
    parser.add_argument("--file", type=str, help="Path to puzzle file")
    args = parser.parse_args()

    sol1 = part_1(file=args.file)
    sol2 = part_2(file=args.file)

    print(f"Part 1 solution: {sol1}")
    print(f"Part 2 solution: {sol2}")
