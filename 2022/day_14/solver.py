import argparse

import numpy as np


def read_input(file: str) -> list:
    """Creates a list with each rock path from the input file.

    Args:
        file (str): Path to puzzle file

    Returns:
        list: List of rock paths
    """
    rock_paths = []
    with open(file) as f:
        raw = [line.split(" -> ") for line in f.read().splitlines()]
    for line in raw:
        path = []
        for point in line:
            x, y = point.split(",")
            # We invert here y and x for simplicity
            path.append((int(y), int(x)))
        rock_paths.append(path)
    return rock_paths


def draw_rocks(
    grid: np.ndarray, start: tuple[int, int], end: tuple[int, int], offset: int
) -> None:
    """Draws the rocks from start to end coordinates.

    Args:
        grid (np.ndarray): Grid of the cave
        start (tuple[int, int]): Start coordinates
        end (tuple[int, int]): End coordinates
        offset (int): Pulls back y values to range(O,L).
    """
    assert start[0] == end[0] or start[1] == end[1]
    x0, y0 = start
    x1, y1 = end
    if x0 == x1:
        grid[x0, min(y0, y1) - offset : max(y0, y1) + 1 - offset] = 2
    else:
        grid[min(x0, x1) : max(x0, x1) + 1, y0 - offset] = 2


def create_rock_structure(rock_paths: list, part=1) -> np.ndarray:
    """Creates rock structures in the cave by drawing straight lines between points.

    Args:
        rock_paths (list): List of rock paths
        part (int, optional): Part of the problem to solve. Defaults to 1.

    Returns:
        np.ndarray: Returns the cave grid with the rock paths.
    """
    x_max = max([max([coord[0] for coord in path]) for path in rock_paths])
    y_min = min([min([coord[1] for coord in path]) for path in rock_paths])
    y_max = max([max([coord[1] for coord in path]) for path in rock_paths])
    H = x_max + 1 + 2 * (part == 2)
    W = y_max - y_min + 1
    grid = np.zeros((H, W))

    for path in rock_paths:
        pivot = path[0]
        for point in path[1:]:
            draw_rocks(grid, start=pivot, end=point, offset=y_min)
            pivot = point
    # Sand source
    grid[0, 500 - y_min] = -1

    if part == 2:
        grid = np.pad(
            grid, pad_width=((0, 0), (H, H)), mode="constant", constant_values=0
        )
        bot1, bot2 = (grid.shape[0] - 1, 0), (grid.shape[0] - 1, grid.shape[1] - 1)
        draw_rocks(grid, start=bot1, end=bot2, offset=0)
    return grid


def checks_rest(grid: np.ndarray, x: int, y: int) -> bool:
    """Checks if a sand unit is at rest at coordinates (x,y)

    Args:
        grid (np.ndarray): Grid of the cave
        x (int): x-axis coordinate
        y (int): y-axis coordinate

    Returns:
        bool: True if the sand unit is at rest
    """
    if x < grid.shape[0] - 1 and y < grid.shape[1] - 1:
        return (
            grid[x + 1, y] != 0 and grid[x + 1, y + 1] != 0 and grid[x + 1, y - 1] != 0
        )
    else:
        return False


def sand_step(grid: np.ndarray, x: int, y: int) -> tuple[int, int]:
    """Performs one falling step for a sand unit at (x,y)

    Args:
        grid (np.ndarray): Grid of the cave
        x (int): x-axis coordinate
        y (int): y-axis coordinate

    Returns:
        tuple[int, int]: The next position of the sand unit
    """
    if x < grid.shape[0] - 1:
        if grid[x + 1, y] == 0:
            return x + 1, y
        elif grid[x + 1, y - 1] == 0:
            return x + 1, y - 1
        elif grid[x + 1, y + 1] == 0:
            return x + 1, y + 1
        else:
            return x, y
    else:
        return x + 1, y


def checks_out(grid: np.ndarray, x: int, y: int) -> bool:
    """Checks whether a sand unit at (x,y) is in the grid or not.

    Args:
        grid (np.ndarray): Grid of the cave
        x (int): x-axis coordinate
        y (int): y-axis coordinate

    Returns:
        bool: True if the sand unit is out of the grid.
    """
    return not (0 <= x and x < grid.shape[0] and 0 <= y and y < grid.shape[1])


def simulate_sandfall(grid: np.ndarray, rest: np.ndarray) -> np.ndarray:
    """Simulates the fall of a sand unit until it reaches rest.

    Args:
        grid (np.ndarray): Grid of the cave
        rest (np.ndarray): Binary grid of fallen sand units in rest

    Returns:
        np.ndarray: The updated grid with sand and rock
    """
    x, y = np.argwhere(grid == -1)[0]
    is_rest = False
    while not is_rest:
        x, y = sand_step(grid, x, y)
        is_rest = checks_rest(grid, x, y)
        if checks_out(grid, x, y):
            break

    if not checks_out(grid, x, y):
        grid[x, y] = 1
        rest[x, y] = 1
    return grid, rest


def count_drops(grid: np.ndarray, part: int = 1) -> int:
    """Counts the drops of sand until no more can fall.

    Args:
        grid (np.ndarray): Grid of the cave
        part (int, optional): Part of the problem to solve. Defaults to 1.

    Returns:
        int: Number of dropped units of sand
    """
    rest = np.zeros(grid.shape)
    converged = False
    counter = -1
    while not converged:
        past_rest = np.copy(rest)
        counter += 1
        grid, rest = simulate_sandfall(grid, rest)
        if part == 1:
            converged = (rest == past_rest).all()
        else:
            converged = -1 not in grid
    return counter + 1 * (part == 2)


def solver(file: str, part: int) -> int:
    """Computes the drops of sand units that fall until equilibrium.

    Args:
        file (str): Path to puzzle file
        part (int): Part of the problem to solve.

    Returns:
        int: Number of sand units fallen until equilibrium.
    """
    paths = read_input(file)
    grid = create_rock_structure(rock_paths=paths, part=part)
    return count_drops(grid=grid, part=part)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solves Day 12 puzzles")
    parser.add_argument("--file", type=str, help="Path to puzzle file")
    args = parser.parse_args()

    sol1 = solver(file=args.file, part=1)
    sol2 = solver(file=args.file, part=2)

    print(f"Part 1 solution: {sol1}")
    print(f"Part 2 solution: {sol2}")
