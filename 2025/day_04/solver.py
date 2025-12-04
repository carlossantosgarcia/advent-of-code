import argparse

import numpy as np


def check_less_than_4_neighbors(i: int, j: int, grid: np.ndarray) -> bool:
    """Check if less than 4 neighboring cells are '@'."""
    c = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            if grid[i + dx, j + dy] == '@':
                c += 1
    return c < 4


def part_1(file: str) -> int:
    with open(file, 'r') as f:
        data = f.readlines()
    grid = np.array([list(row.strip()) for row in data])
    grid = np.pad(grid, pad_width=1, mode='constant', constant_values='.')

    forklifts = np.where(grid == '@')
    count = 0
    for i, j in zip(*forklifts):
        if check_less_than_4_neighbors(i, j, grid):
            count += 1
    return count


def remove_forklifts(grid: np.ndarray) -> tuple[np.ndarray, int]:
    forklifts = np.where(grid == '@')
    to_remove = []
    new_grid = grid.copy()
    for i, j in zip(*forklifts):
        if check_less_than_4_neighbors(i, j, grid):
            to_remove.append((i, j))
    if to_remove:
        indices = tuple(zip(*to_remove))
        new_grid[indices] = '.'
    return new_grid, len(to_remove)


def part_2(file: str) -> int:
    with open(file, 'r') as f:
        data = f.readlines()
    grid = np.array([list(row.strip()) for row in data])
    grid = np.pad(grid, pad_width=1, mode='constant', constant_values='.')

    new_grid, removed = remove_forklifts(grid)
    while (new_grid != grid).any():
        grid = new_grid.copy()
        new_grid, newly_removed = remove_forklifts(grid)
        removed += newly_removed
    return removed


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solves current day puzzles")
    parser.add_argument("--file", type=str, help="Path to puzzle file")
    args = parser.parse_args()

    sol1 = part_1(file=args.file)
    sol2 = part_2(file=args.file)

    print(f"Part 1 solution: {sol1}")
    print(f"Part 2 solution: {sol2}")
