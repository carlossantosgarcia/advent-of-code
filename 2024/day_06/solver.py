import argparse

import numpy as np

UP, RIGHT, DOWN, LEFT = (-1, 0), (0, 1), (1, 0), (0, -1)
next_dir = {UP: RIGHT, RIGHT: DOWN, DOWN: LEFT, LEFT: UP}


def can_move(
        guard: tuple[int, int],
        dir: tuple[int, int],
        data: np.ndarray) -> bool:
    """Checks if the guard can move in the given direction."""
    x, y = guard
    dx, dy = dir
    return data[x + dx, y + dy] != "#"


def guard_is_out(
        guard: tuple[int, int],
        dir: tuple[int, int],
        data: np.ndarray) -> bool:
    """Returns True if the guard is out of the lab."""
    x, y = guard
    return data[x, y] == "o"


def move_guard(
        guard: tuple[int, int],
        dir: tuple[int, int],
        next_dir: dict,
        data: np.ndarray) -> tuple[tuple[int, int], tuple[int, int], list]:
    """Moves the guard in the given direction.

    Returns:
        - new_guard: the new position of the guard.
        - new_dir: the new direction of the guard.
        - visited_points: a list of visited points
    """
    x, y = guard
    x, y = int(x), int(y)
    dx, dy = dir
    n = 1
    while np.isin(data[x + n*dx, y + n*dy], [".", "^"]):
        n += 1
    if data[x + n*dx, y + n*dy] == "o":
        n = n + 1
    visited_points = [(x + i*dx, y + i*dy) for i in range(0, n)]
    return (x + (n-1)*dx, y + (n-1)*dy), next_dir[dir], visited_points


def part_1(file: str) -> int:
    data = []
    with open(file) as f:
        for line in f:
            data.append(list(line.strip()))
    data = np.array(data)
    data = np.pad(data, 1, constant_values="o")

    guard = np.where(data == "^")
    guard, dir, visited_points = move_guard(guard, UP, next_dir, data)
    while not guard_is_out(guard, dir, data):
        guard, dir, new_points = move_guard(guard, dir, next_dir, data)
        visited_points.extend(new_points)
    return len(set(visited_points)) - 1  # -1 to remove the last "o"


def has_loop(data: np.ndarray) -> bool:
    """Returns True if the guard falls in a loop with the given input data."""
    guard = np.where(data == "^")
    corners = set()
    guard, dir, _ = move_guard(guard, UP, next_dir, data)
    while not guard_is_out(guard, dir, data):
        guard, dir, _ = move_guard(guard, dir, next_dir, data)
        if (guard, dir) in corners:
            return True
        corners.add((guard, dir))
    return False


def compute_visited(data: np.ndarray) -> set[tuple[int, int]]:
    """Returns the set of visited points by the guard."""
    guard = np.where(data == "^")
    visited_points = []
    guard, dir, visited_points = move_guard(guard, UP, next_dir, data)
    while not guard_is_out(guard, dir, data):
        guard, dir, new_points = move_guard(guard, dir, next_dir, data)
        visited_points.extend(new_points)
    return set(visited_points)


def get_possible_obstructions(data: np.ndarray) -> list[tuple[int, int]]:
    """Returns a list of places to put an obstruction '#'."""
    visited = compute_visited(data)
    new_data = data.copy()
    for x, y in visited:
        if data[x, y] != "o":
            new_data[x, y] = "X"
    positions = []
    for x, y in zip(*np.where(new_data == "X")):
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if data[x + dx, y + dy] == ".":
                positions.append((x + dx, y + dy))
    return list(set(positions))


def part_2(file: str) -> int:
    data = []
    with open(file) as f:
        for line in f:
            data.append(list(line.strip()))
    data = np.array(data)
    data = np.pad(data, 1, constant_values="o")

    positions = get_possible_obstructions(data)
    count = 0
    for x, y in positions:
        new_data = data.copy()
        new_data[x, y] = "#"
        if has_loop(new_data):
            count += 1
            new_data[x, y] = "O"
    return count


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solves current day puzzles")
    parser.add_argument("--file", type=str, help="Path to puzzle file")
    args = parser.parse_args()

    sol1 = part_1(file=args.file)
    sol2 = part_2(file=args.file)

    print(f"Part 1 solution: {sol1}")
    print(f"Part 2 solution: {sol2}")
