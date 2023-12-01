import argparse
import re

import numpy as np


def part_1(file: str) -> tuple[list, int]:
    """Computes calibration values from document.

    Args:
        file (str): Path to the puzzle input

    Returns:
        int: Total sum of calibration values
    """
    pattern = r"\d+"
    document = np.loadtxt(file, dtype=str)
    calibration_vals = []
    for line in document:
        nums = re.findall(pattern, line)
        start, end = nums[0], nums[-1]
        start = start[0] if len(start) > 1 else start
        end = end[-1] if len(end) > 1 else end
        calibration_vals.append(int("".join([start, end])))
    return sum(calibration_vals)


def part_2(file: str) -> int:
    """Computes calibration values now also taking into account numbers written
    in natural language.

    Args:
        file (str): Path to the puzzle input

    Returns:
        int: Total sum of calibration values
    """
    pattern = r"\d+"
    document = np.loadtxt(file, dtype=str)
    replacements = dict(zip(
        ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"],
        range(1, 10),
    ))
    for num, target in replacements.items():
        replacements[num] = f"{num[0]}{target}{num[-1]}"
    calibration_vals = []
    for line in document:
        for num, target in replacements.items():
            line = line.replace(num, str(target))
        nums = re.findall(pattern, line)
        start, end = nums[0], nums[-1]
        start = start[0] if len(start) > 1 else start
        end = end[-1] if len(end) > 1 else end
        calibration_vals.append(int("".join([start, end])))
    return sum(calibration_vals)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solves Day 1 puzzles")
    parser.add_argument("--file", type=str, help="Path to puzzle file")
    args = parser.parse_args()

    sol1 = part_1(file=args.file)
    sol2 = part_2(file=args.file)

    print(f"Part 1 solution: {sol1}")
    print(f"Part 2 solution: {sol2}")
