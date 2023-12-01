import argparse

import numpy as np


def find_repeated_item(row) -> str:
    """
    Finds repeated item in two strings.
    """
    N = len(row[0]) // 2
    left, right = row[0][:N], row[0][N:]
    inter = set(left).intersection(set(right))
    return str(list(inter)[0])


def compute_score(row) -> int:
    """
    Computes the score (priority) of a given item.
    """
    letter = row[0]
    abc = "abcdefghijklmnopqrstuvwxyz"
    if letter.isupper():
        return 27 + abc.index(letter.lower())
    else:
        return 1 + abc.index(letter)


def find_badge(array):
    """
    Finds common item in three substrings.
    """
    return list(set(array[0]).intersection(set(array[1])).intersection(set(array[2])))[
        0
    ]


def part_1(file: str) -> int:
    """Computes the sum of priorities of wrongly packed items.

    Args:
        file (str): Path to puzzle file

    Returns:
        int: Sum of priorities of items
    """
    data = np.genfromtxt(file, dtype=str)

    repeated_items = np.apply_along_axis(find_repeated_item, 1, data.reshape(-1, 1))

    scores = np.apply_along_axis(compute_score, 1, repeated_items.reshape(-1, 1))

    return np.sum(scores)


def part_2(file: str) -> int:
    """Computes the priorities of the badges.

    Args:
        file (str): Path to puzzle file

    Returns:
        int: Sum of priorities of the found badges
    """
    data = np.genfromtxt(file, dtype=str)

    K = len(data) // 3
    priorities = 0

    for i in range(K):
        priorities += compute_score(find_badge(data[i * 3 : (i + 1) * 3]))

    return priorities


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solves Day 3 puzzles")
    parser.add_argument("--file", type=str, help="Path to puzzle file")
    args = parser.parse_args()

    sol1 = part_1(file=args.file)
    sol2 = part_2(file=args.file)

    print(f"Part 1 solution: {sol1}")
    print(f"Part 2 solution: {sol2}")
