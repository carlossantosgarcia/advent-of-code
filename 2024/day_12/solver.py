import argparse
import collections

import numpy as np


def find_connected_indices(data, i, j) -> list[tuple[int, int]]:
    """Finds all coordinates belonging to the same group as (i, j)."""
    val = data[i, j]
    to_visit = [(i, j)]
    visited = set()
    indices = []
    deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    while len(to_visit):
        x, y = to_visit.pop()
        if (x, y) in visited:
            continue
        indices.append((x, y))
        visited.add((x, y))
        for dx, dy in deltas:
            if data[x + dx, y + dy] == val:
                to_visit.append((x + dx, y + dy))
    return indices


def find_perimeter(data, indices: list[tuple[int, int]]) -> int:
    """Computes the perimeter of a given group of coordinates."""
    perimeter = 0
    deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    val = data[indices[0]]
    for x, y in indices:
        perimeter += 4 - sum(data[x + dx, y + dy] == val for dx, dy in deltas)
    return perimeter


def is_alone(
        block: tuple[int, int],
        coords: list[tuple[int, int]],
        axis: int) -> bool:
    """Checks if a given fence all by itself."""
    axis2coord = {'x': 1, 'y': 0}
    ax = axis2coord[axis]
    for coord in coords:
        if abs(coord[ax]-block[ax]) == 1:
            return False
    return True


def find_same_fence_group(
        block: tuple[int, int],
        coords: list[tuple[int, int]],
        axis: int,
        fence: tuple[int, int]):
    """For a given fence, finds all elements from a list of coordinates that
    belong to the same geometrical 'side'."""
    axis2coord = {'x': 1, 'y': 0}
    ax = axis2coord[axis]
    to_visit = [block]
    group = set()
    while len(to_visit):
        curr = to_visit.pop()
        # Check neighbors of curr along axis ax
        for coord in coords:
            uid = tuple(list(fence) + list(coord))
            if (
                abs(coord[ax]-curr[ax]) == 1
                and uid not in group
                and coord[1-ax] == curr[1-ax]
            ):
                group.add(uid)
                to_visit.append(coord)
    return group


def keep_only_one_fence_per_side(level, axis):
    """Keep only one representative of each geometrical side."""
    clean = []
    to_ignore = set()
    for fence, coords in level.items():
        for idx, (x, y) in enumerate(coords):
            uid = tuple(list(fence) + [x, y])
            if is_alone((x, y), coords[:idx] + coords[idx+1:], axis):
                clean.append(uid)
            elif uid in to_ignore:
                continue
            else:
                group = find_same_fence_group((x, y), coords, axis, fence)
                to_ignore.update(group)
                clean.append(tuple(list(fence) + [x, y]))
    return clean


def find_nb_sides(data, indices) -> int:
    """Computes the number of geometrical sides of a group of blocks."""
    deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    val = data[indices[0]]
    x_level, y_level = collections.defaultdict(
        list), collections.defaultdict(list)
    for x, y in indices:
        for dx, dy in deltas:
            if data[x + dx, y + dy] != val:
                if dx:
                    x_level[(min(x, x + dx), max(x, x + dx))].append((x, y))
                elif dy:
                    y_level[(min(y, y + dy), max(y, y + dy))].append((x, y))

    x_clean = keep_only_one_fence_per_side(x_level, 'x')
    y_clean = keep_only_one_fence_per_side(y_level, 'y')

    return len(x_clean) + len(y_clean)


def part_1(file: str) -> int:
    data = np.genfromtxt(file, delimiter=1, dtype=str)
    visited = np.zeros(data.shape)
    data = np.pad(data, 1, mode='constant', constant_values='.')
    visited = np.pad(visited, 1, mode='constant', constant_values=1)

    count = 0
    while not np.all(visited):
        for i in range(1, data.shape[0]-1):
            for j in range(1, data.shape[1]-1):
                if visited[i, j]:
                    continue
                indices = find_connected_indices(data, i, j)
                area = len(indices)
                sides = find_perimeter(data, indices)
                for x, y in indices:
                    visited[x, y] = 1
                count += area * sides
    return count


def part_2(file: str) -> int:
    data = np.genfromtxt(file, delimiter=1, dtype=str)
    visited = np.zeros(data.shape)
    data = np.pad(data, 1, mode='constant', constant_values='.')
    visited = np.pad(visited, 1, mode='constant', constant_values=1)

    count = 0
    while not np.all(visited):
        for i in range(1, data.shape[0]-1):
            for j in range(1, data.shape[1]-1):
                if visited[i, j]:
                    continue
                indices = find_connected_indices(data, i, j)
                area = len(indices)
                sides = find_nb_sides(data, indices)
                for x, y in indices:
                    visited[x, y] = 1
                count += area * sides
    return count


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solves current day puzzles")
    parser.add_argument("--file", type=str, help="Path to puzzle file")
    args = parser.parse_args()

    sol1 = part_1(file=args.file)
    sol2 = part_2(file=args.file)

    print(f"Part 1 solution: {sol1}")
    print(f"Part 2 solution: {sol2}")
