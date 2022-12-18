import argparse

import numpy as np


def check_fully_contains(pair: np.ndarray) -> int:
    """Checks if for a given pair (e.g. "2-3,3-5") one assignment contains the other.

    Args:
        pair (np.ndarray): Array of strings

    Returns:
        int: Returns 1 if one assignment contains the other, 0 otherwise
    """
    section_1, section_2 = pair[0].split(",")
    beg_1, end_1 = section_1.split("-")
    beg_2, end_2 = section_2.split("-")
    if (int(beg_2) <= int(beg_1) and int(end_1) <= int(end_2)) or (
        int(beg_1) <= int(beg_2) and int(end_2) <= int(end_1)
    ):
        return 1
    else:
        return 0


def check_overlaps(pair: np.ndarray) -> int:
    """Checks if for a given pair the assignments overlap.

    Args:
        pair (np.ndarray): Array of strings

    Returns:
        int: Returns 1 if there is some overlap, 0 otherwise
    """
    section_1, section_2 = pair[0].split(",")
    beg_1, end_1 = section_1.split("-")
    beg_2, end_2 = section_2.split("-")
    for i in range(int(beg_1), int(end_1) + 1):
        if i in range(int(beg_2), int(end_2) + 1):
            return 1
    return 0


def part_1(file: str) -> int:
    """Computes the number of pairs where one assignment fully contains the other.

    Args:
        file (str): Path to puzzle file

    Returns:
        int: Number of pairs where one assignment contains the other
    """
    puzzle = np.genfromtxt(file, dtype=str)

    scores = np.apply_along_axis(check_fully_contains, 1, puzzle.reshape(-1, 1))

    return np.sum(scores)


def part_2(file: str) -> int:
    """Computes the number of pairs where there is some overlap.

    Args:
        file (str): Path to puzzle file

    Returns:
        int: Number of pairs with overlap
    """
    puzzle = np.genfromtxt(file, dtype=str)

    scores = np.apply_along_axis(check_overlaps, 1, puzzle.reshape(-1, 1))

    return np.sum(scores)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solves Day 4 puzzles")
    parser.add_argument("--file", type=str, help="Path to puzzle file")
    args = parser.parse_args()

    sol1 = part_1(file=args.file)
    sol2 = part_2(file=args.file)

    print(f"Part 1 solution: {sol1}")
    print(f"Part 2 solution: {sol2}")
