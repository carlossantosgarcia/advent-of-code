import argparse

import numpy as np
import pandas as pd


def are_same_sign(row):
    # Ignore NaN values
    row = row.dropna()
    return np.all(row > 0) or np.all(row < 0)


def range_is_ok(row):
    # Ignore NaN values
    row = row.dropna()
    return np.abs(row).max() <= 3 and np.abs(row).min() >= 1


def remove_one_and_check(row):
    row = row.dropna().tolist()
    for i in range(len(row)):
        new_row = pd.Series(row[:i] + row[i+1:])
        new_row = new_row.diff()
        if are_same_sign(new_row) and range_is_ok(new_row):
            return True
    return False


def part_1(file: str) -> int:
    data = pd.read_csv(file, sep=" ", names=[str(i) for i in range(8)])
    diff = data.diff(axis=1)
    data["same_sign"] = diff.apply(are_same_sign, axis=1)
    data['range_is_ok'] = diff.apply(range_is_ok, axis=1)
    return len(data[data['same_sign'] & data['range_is_ok']])


def part_2(file: str) -> int:
    data = pd.read_csv(file, sep=" ", names=[str(i) for i in range(8)])
    data['tolerated'] = data.apply(remove_one_and_check, axis=1)
    return len(data[data['tolerated']])


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solves Day 1 puzzles")
    parser.add_argument("--file", type=str, help="Path to puzzle file")
    args = parser.parse_args()

    sol1 = part_1(file=args.file)
    sol2 = part_2(file=args.file)

    print(f"Part 1 solution: {sol1}")
    print(f"Part 2 solution: {sol2}")
