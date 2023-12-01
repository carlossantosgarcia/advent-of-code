import argparse

import numpy as np


def create_X_register(file: str) -> list:
    """Creates the register of X values at each clock cycle.

    Args:
        file (str): Path to puzzle file

    Returns:
        list: X value at each clock cycle
    """
    X_hist = []
    with open(file) as f:
        X = 1
        for line in f:
            line = line.strip()
            if line == "noop":
                X_hist.append(X)
            else:
                val = int(line.split(" ")[1])
                X_hist += [X, X]
                X += val
    return X_hist


def sum_signal_strengths(indices: list, X_hist: list) -> int:
    """Computes the total signal strengths with the given the history of X.

    Args:
        indices (list): Cycles at which to compute signal strengths
        X_hist (list): History of X values

    Returns:
        int: Sum of signal strengths
    """
    return sum([n * X_hist[n - 1] for n in indices])


def part_1(file: str) -> int:
    """Computes the sum of the signal strengths taken at given clock cycles.

    Args:
        file (str): Path to puzzle file

    Returns:
        int: Sum of signal strengths
    """
    X_hist = create_X_register(file=file)
    return sum_signal_strengths(indices=[20, 60, 100, 140, 180, 220], X_hist=X_hist)


def part_2(file: str) -> np.ndarray:
    """Plots the Cathode-ray tube obtained by drawing pixels.

    Args:
        file (str): Path to puzzle file
    """
    X_hist = create_X_register(file=file)

    CRT = []
    for i in range(6):
        row = ""
        for k in range(40):
            X_pos = X_hist[k + 40 * i]
            char = "#" if abs(X_pos - k) <= 1 else "."
            row += char
        CRT.append(row)
    return np.array(CRT)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solves Day 10 puzzles")
    parser.add_argument("--file", type=str, help="Path to puzzle file")
    args = parser.parse_args()

    sol1 = part_1(file=args.file)
    sol2 = part_2(file=args.file)

    print(f"Part 1 solution: {sol1}")
    print("Part 2 solution: ")
    for row in sol2:
        print(row)
