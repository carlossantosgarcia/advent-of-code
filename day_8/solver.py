import argparse

import numpy as np


def file_to_array(file: str) -> np.ndarray:
    """Loads input file and creates array with tree heights.

    Args:
        file (str): Path to puzzle file

    Returns:
        np.ndarray: Array with puzzle input
    """
    lines = []
    with open(file) as f:
        for line in f:
            line = line.strip("\n")
            lines.append(np.array([int(n) for n in line]))
    return np.array(lines)


def is_visible(data: np.ndarray, i: int, j: int) -> bool:
    """Checks if a given tree is visible from outside the grid.

    Args:
        data (np.ndarray): Map of tree heights
        i (int): x coordinate of the tree
        j (int): y coordinate of the tree

    Returns:
        bool: True if tree is visible, else False
    """
    directions = [data[:i, j], data[i + 1 :, j], data[i, :j], data[i, j + 1 :]]
    return data[i, j] > min([max(a) for a in directions])


def viewing_distance(direction: np.ndarray, value: int) -> int:
    """Computes the viewing distance for a given direction.

    Args:
        direction (np.ndarray): The heights of trees in the given direction
        value (int): Height of the tree from which the distance is computed

    Returns:
        int: Viewing distance from the tree
    """
    new = np.where((direction - value) < 0, 1, 0)
    if 0 not in new:
        return len(direction)
    else:
        return np.argwhere(new == 0)[0][0] + 1


def scenic_score(data: np.ndarray, i: int, j: int) -> int:
    """Computes the scenic score from tree in (i,j).

    Args:
        data (np.ndarray): Map of tree heights
        i (int): x coordinate of the tree
        j (int): y coordinate of the tree

    Returns:
        int: Scenic score from the tree at (i,j)
    """
    directions = [
        np.flip(data[:i, j]),
        data[i + 1 :, j],
        np.flip(data[i, :j]),
        data[i, j + 1 :],
    ]
    score = 1
    for direction in directions:
        lscore = viewing_distance(direction, data[i, j])
        score *= lscore
    return score


def scenic_map(data: np.ndarray) -> np.ndarray:
    """Creates a grid with scenic scores for each tree.

    Args:
        data (np.ndarray): Map of tree heights

    Returns:
        np.ndarray: Scenic scores grid
    """
    N, M = data.shape
    scenic_map = np.zeros((N, M))
    for i in range(1, N - 1):
        for j in range(1, M - 1):
            scenic_map[i, j] = scenic_score(data, i, j)
    return scenic_map


def part_1(file: str) -> int:
    """Computes the number of trees visible from the outside of the grid.

    Args:
        file (str): Path to puzzle file

    Returns:
        int: The number of visible trees in the grid.
    """

    data = file_to_array(file=file)

    N, M = data.shape
    counter = 2 * (N + M) - 4
    for i in range(1, N - 1):
        for j in range(1, M - 1):
            if is_visible(data, i, j):
                counter += 1
    return counter


def part_2(file: str) -> int:
    """Computes the maximum scenic score in the grid

    Args:
        file (str): Path to puzzle file

    Returns:
        int: The highest scenic score in the grid
    """

    data = file_to_array(file=file)

    map = scenic_map(data)

    return int(np.max(map))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solves Day 8 puzzles")
    parser.add_argument("--file", type=str, help="Path to puzzle file")
    args = parser.parse_args()

    sol1 = part_1(file=args.file)
    sol2 = part_2(file=args.file)

    print(f"Part 1 solution: {sol1}")
    print(f"Part 2 solution: {sol2}")
