import argparse
import collections
import re

import scipy


def is_int(n: int) -> bool:
    return abs(n-round(n)) < 1e-3


def load_data(file, offset=0):
    data = collections.defaultdict(list)
    with open(file, 'r') as f:
        for line in f.readlines():
            if line.startswith("Button"):
                button, x, y = re.findall(
                    r"Button (.*): X\+(\d+), Y\+(\d+)", line)[0]
                data[button].append((int(x), int(y)))
            elif line.startswith("Prize"):
                x, y = re.findall(r"Prize: X=(\d+), Y=(\d+)", line)[0]
                data['R'].append(
                    (offset + int(x), offset + int(y)))
    return data


def part_1(file: str) -> int:
    data = load_data(file)
    count = 0
    for (a_x, a_y), (b_x, b_y), (r_x, r_y) in zip(
            data['A'], data['B'], data['R']):
        nb_A, nb_B = scipy.linalg.inv([[a_x, b_x], [a_y, b_y]]) @ [r_x, r_y]
        if is_int(nb_A) and is_int(nb_B):
            count += 3*round(nb_A) + round(nb_B)
    return count


def part_2(file: str) -> int:
    data = load_data(file, offset=10000000000000)
    count = 0
    for (a_x, a_y), (b_x, b_y), (r_x, r_y) in zip(
            data['A'], data['B'], data['R']):
        nb_A, nb_B = scipy.linalg.inv([[a_x, b_x], [a_y, b_y]]) @ [r_x, r_y]
        if is_int(nb_A) and is_int(nb_B):
            count += 3*round(nb_A) + round(nb_B)
    return count


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solves current day puzzles")
    parser.add_argument("--file", type=str, help="Path to puzzle file")
    args = parser.parse_args()

    sol1 = part_1(file=args.file)
    sol2 = part_2(file=args.file)

    print(f"Part 1 solution: {sol1}")
    print(f"Part 2 solution: {sol2}")
