import argparse

import numpy as np


def find_letters_in_neighborhood(data, x, y, letter):
    """Find all neighbors of a given letter at x, y"""
    steps = (-1, 0, 1)
    deltas = [(x, y) for x in steps for y in steps if (x, y) != (0, 0)]
    matches = []
    for dx, dy in deltas:
        if data[x+dx, y+dy] == letter:
            matches.append((dx, dy))
    return matches


def count_xmas(data, x, y):
    """Count the number of XMAS sequences starting at x, y"""
    count = 0
    deltas = find_letters_in_neighborhood(data, x, y, "M")
    for dx, dy in deltas:
        values = []
        for i in range(4):
            values.append(data[x+i*dx, y+i*dy])
        if "".join(values) == "XMAS":
            count += 1
    return count


def part_1(file: str) -> int:
    data = np.loadtxt(file, dtype=str)
    data = np.array([list(row) for row in data])
    data = np.pad(data, 3, constant_values=".")
    x_idx = np.where(data == "X")
    count = 0
    for x, y in zip(*x_idx):
        count += count_xmas(data, x, y)
    return count


def create_kernels():
    """Create all possible X-MAS 3x3 blocks."""
    def antidiag(a):
        return np.fliplr(np.diag(a))
    diag_fn, antidiag_fn = np.diag, antidiag
    diags = [list(range(2, 5)), list(range(4, 1, -1))]
    kernels = []
    for diag1 in diags:
        for diag2 in diags:
            arr1, arr2 = diag_fn(diag1), antidiag_fn(diag2)
            result = np.where(arr1 != 0, arr1, arr2)
            result = np.where(result == 0, np.nan, result)
            kernels.append(result)
    return kernels


def A_belongs_to_x_mas(data, x, y):
    """Returns 1 if 'A' belongs to X-MAS, 0 otherwise."""
    kernels = create_kernels()
    submatrix = data[x-1:x+2, y-1:y+2]
    for kernel in kernels:
        mask = ~np.isnan(kernel)
        if np.all(submatrix[mask] == kernel[mask]):
            return 1
    return 0


def part_2(file: str) -> int:
    data = np.loadtxt(file, dtype=str)
    data = np.array([list(row) for row in data])
    data = np.pad(data, 3, constant_values=".")
    str2float = dict(zip("XMAS", range(1, 5)))
    str2float |= {".": np.nan}
    data = np.vectorize(str2float.get)(data)
    a_idx = np.where(data == str2float["A"])
    count = 0
    for x, y in zip(*a_idx):
        count += A_belongs_to_x_mas(data, x, y)
    return count


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solves current day puzzles")
    parser.add_argument("--file", type=str, help="Path to puzzle file")
    args = parser.parse_args()

    sol1 = part_1(file=args.file)
    sol2 = part_2(file=args.file)

    print(f"Part 1 solution: {sol1}")
    print(f"Part 2 solution: {sol2}")
