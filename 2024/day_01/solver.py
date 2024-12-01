import argparse
import collections

import numpy as np

def part_1(file: str) -> int:
    lists = np.loadtxt(file, dtype=str).astype(int)
    return np.abs(np.sort(lists[:, 0]) - np.sort(lists[:, 1])).sum()

def part_2(file: str) -> int:
    lists = np.loadtxt(file, dtype=str).astype(int)
    left, rigth = lists[:, 0], lists[:, 1]
    rigth_ocurrences = collections.Counter(rigth)
    compute_sim = np.vectorize(lambda x: rigth_ocurrences[x])
    return (compute_sim(left) * left).sum()





if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solves Day 1 puzzles")
    parser.add_argument("--file", type=str, help="Path to puzzle file")
    args = parser.parse_args()

    sol1 = part_1(file=args.file)
    sol2 = part_2(file=args.file)

    print(f"Part 1 solution: {sol1}")
    print(f"Part 2 solution: {sol2}")
