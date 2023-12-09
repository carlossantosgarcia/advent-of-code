import argparse

import numpy as np


def predict_forward_value(row: np.ndarray) -> int:
    """Predicts next value in a time series."""
    vals = [row[-1]]
    while np.sum(np.abs(row)):
        delta = row[1:] - row[:-1]
        row = delta
        vals.append(delta[-1])
    return sum(vals)


def predict_backwards_value(row: np.ndarray) -> int:
    """Predicts previous value in a time series."""
    vals = [row[0]]
    sign = -1
    while np.sum(np.abs(row)):
        delta = row[1:] - row[:-1]
        row = delta
        vals.append(sign * delta[0])
        sign *= -1
    return np.sum(vals)


def part_1(file: str) -> int:
    """Computes the sum of the forward predictions from time series.

    Args:
        file (str): Path to the puzzle input

    Returns:
        int: Sum of the predicted values.
    """
    history = []
    with open(file) as f:
        for line in f.readlines():
            history.append(np.array([int(n) for n in line.rstrip().split()]))

    preds = []
    for row in history:
        pred = predict_forward_value(row)
        preds.append(pred)
    return sum(preds)


def part_2(file: str) -> int:
    """Computes the sum of the backward-predicted values from time series.

    Args:
        file (str): Path to the puzzle input

    Returns:
        int: Sum of the predicted values.
    """
    history = []
    with open(file) as f:
        for line in f.readlines():
            history.append(np.array([int(n) for n in line.rstrip().split()]))

    preds = []
    for row in history:
        pred = predict_backwards_value(row)
        preds.append(pred)
    return sum(preds)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solves Day 9 puzzles")
    parser.add_argument("--file", type=str, help="Path to puzzle file")
    args = parser.parse_args()

    sol1 = part_1(file=args.file)
    sol2 = part_2(file=args.file)

    print(f"Part 1 solution: {sol1}")
    print(f"Part 2 solution: {sol2}")
