import argparse

import numpy as np


def add_next(x, y, data, curr_val):
    """Find neighbors for (x, y) where value == curr_val + 1."""
    next_coords = []
    deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for dx, dy in deltas:
        if data[x + dx, y + dy] == curr_val + 1:
            next_coords.append((x + dx, y + dy))
    return next_coords


def part_1(file: str) -> int:
    data = np.genfromtxt(file, delimiter=1)
    data = np.pad(data, 1, 'constant', constant_values=-1)

    starts = np.argwhere(data == 0)
    count = 0

    for x, y in starts:
        tops = set()
        curr_val = data[x, y]
        to_visit = []
        to_visit.extend(add_next(x, y, data, curr_val))
        while len(to_visit):
            x, y = to_visit.pop()
            curr_val = data[x, y]
            if curr_val < 9:
                to_visit.extend(add_next(x, y, data, curr_val))
            else:
                tops.add((x, y))
        count += len(tops)
    return count


def part_2(file: str) -> int:
    data = np.genfromtxt(file, delimiter=1)
    data = np.pad(data, 1, 'constant', constant_values=-1)

    starts = np.argwhere(data == 0)
    count = 0

    count = 0
    for x, y in starts:
        hikes = set()
        curr_val = data[x, y]
        curr_hike = [(x, y)]
        to_visit = []
        to_visit.extend(add_next(x, y, data, curr_val))
        while len(to_visit):
            x, y = to_visit.pop(0)
            curr_val = data[x, y]
            curr_hike = [tup for tup in curr_hike if data[tup]
                         < curr_val] + [(x, y)]
            if curr_val < 9:
                for x, y in add_next(x, y, data, curr_val):
                    to_visit.insert(0, (x, y))
            else:
                hikes.add(str(curr_hike))
        count += len(hikes)
    return count


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solves current day puzzles")
    parser.add_argument("--file", type=str, help="Path to puzzle file")
    args = parser.parse_args()

    sol1 = part_1(file=args.file)
    sol2 = part_2(file=args.file)

    print(f"Part 1 solution: {sol1}")
    print(f"Part 2 solution: {sol2}")
