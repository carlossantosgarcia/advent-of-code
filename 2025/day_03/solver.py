import argparse

import numpy as np


def create_biggest_number(pattern: list[int], depth: int) -> str:
    if depth == 1:
        return str(pattern[np.argmax(pattern)])
    else:
        curr_idx = np.argmax(pattern[:-depth + 1])
        return (str(pattern[curr_idx]) +
                create_biggest_number(pattern[curr_idx + 1:], depth - 1))


def part_1(file: str) -> int:
    with open(file, 'r') as f:
        data = [[int(n) for n in line.strip()] for line in f]

    count = 0
    for row in data:
        count += int(create_biggest_number(row, 2))
    return count


def part_2(file: str) -> int:
    with open(file, 'r') as f:
        data = [[int(n) for n in line.strip()] for line in f]

    count = 0
    for row in data:
        count += int(create_biggest_number(row, 12))
    return count


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solves current day puzzles")
    parser.add_argument("--file", type=str, help="Path to puzzle file")
    args = parser.parse_args()

    sol1 = part_1(file=args.file)
    sol2 = part_2(file=args.file)

    print(f"Part 1 solution: {sol1}")
    print(f"Part 2 solution: {sol2}")
