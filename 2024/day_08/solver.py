import argparse
import itertools

import numpy as np


def get_antinodes(p1: np.ndarray, p2: np.ndarray) -> list[np.ndarray]:
    diff = p2 - p1
    return [p2 + diff, p1 - diff]


def is_in_bounds(coords: np.ndarray, data: np.ndarray) -> bool:
    W, H = data.shape
    return 0 <= coords[0] < W and 0 <= coords[1] < H


def get_harmonic_antinodes(data, p1, p2) -> list[np.ndarray]:
    diff = p2 - p1
    n2, n1 = 1, 1
    anti_coords = []
    while is_in_bounds(p2 + n2 * diff, data):
        n2 += 1
    while is_in_bounds(p1 - n1 * diff, data):
        n1 += 1
    anti_coords.extend([p2 + i * diff for i in range(0, n2)])
    anti_coords.extend([p1 - i * diff for i in range(0, n1)])
    return anti_coords


def add_antinodes(antinodes: np.ndarray, coords: list[np.ndarray]) -> np.ndarray:
    W, H = antinodes.shape
    for x, y in coords:
        if 0 <= x < W and 0 <= y < H:
            antinodes[x, y] += 1
    return antinodes


def part_1(file: str) -> int:
    rows = []
    with open(file) as f:
        for line in f.readlines():
            rows.append(list(line.strip()))
    data = np.array(rows)
    antinodes = np.zeros(data.shape)
    for antenna in np.unique(data):
        if antenna == ".":
            continue
        coords = np.argwhere(data == antenna)  # N, 2
        for i1, i2 in itertools.combinations(range(coords.shape[0]), 2):
            anti_coords = get_antinodes(coords[i1, :], coords[i2, :])
            antinodes = add_antinodes(antinodes, anti_coords)
    return np.sum(antinodes > 0)


def part_2(file: str) -> int:
    rows = []
    with open(file) as f:
        for line in f.readlines():
            rows.append(list(line.strip()))
    data = np.array(rows)
    antinodes = np.zeros(data.shape)
    for antenna in np.unique(data):
        if antenna == ".":
            continue
        coords = np.argwhere(data == antenna)  # N, 2
        for i1, i2 in itertools.combinations(range(coords.shape[0]), 2):
            anti_coords = get_harmonic_antinodes(
                data, coords[i1, :], coords[i2, :])
            antinodes = add_antinodes(antinodes, anti_coords)
    return np.sum(antinodes > 0)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solves current day puzzles")
    parser.add_argument("--file", type=str, help="Path to puzzle file")
    args = parser.parse_args()

    sol1 = part_1(file=args.file)
    sol2 = part_2(file=args.file)

    print(f"Part 1 solution: {sol1}")
    print(f"Part 2 solution: {sol2}")
