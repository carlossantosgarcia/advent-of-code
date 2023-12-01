import argparse

import numpy as np


def load_graph(file: str) -> np.ndarray:
    """Loads puzzle file and creates a grid with each position's height.

    Starting position is -1, and target is 26 (= ord("z") - 96)

    Args:
        file (str): Path to puzzle file

    Returns:
        np.ndarray: Array with each position's height
    """
    raw = np.genfromtxt(file, dtype=None, encoding=None)
    N, M = len(raw), len(raw[0])
    graph = [[] for _ in range(N)]
    for i in range(N):
        for j in range(M):
            val = raw[i][j]
            if val not in ("S", "E"):
                graph[i].append(ord(val) - 97)
            elif val == "S":
                graph[i].append(-1)
            elif val == "E":
                graph[i].append(ord("z") - 96)
    return np.array(graph)


def is_valid(
    graph: np.ndarray, parent: tuple[int, int], child: tuple[int, int]
) -> bool:
    """Checks if the tuple child is a child node from parent in the given grid.

    Args:
        graph (np.ndarray): Array with each position's height
        parent (tuple[int,int]): Coordinates of parent's node
        child (tuple[int,int]): Coordinates of child's node

    Returns:
        bool: True if one can go from parent to child
    """

    N, M = graph.shape
    if child[1] < M and child[0] < N and min(child) > -1:
        return graph[child] - graph[parent] <= 1
    else:
        return False


def find_unvisited_neighbours(
    graph: np.ndarray, coord: tuple[int, int], already_visited: set
) -> list:
    """Creates a list of unvisited neighbours for coord.

    Args:
        graph (np.ndarray): Array with each position's height
        coord (tuple[int, int]): Coordinates of current position
        already_visited (set): Set of already visited nodes with BFS

    Returns:
        list: List of unvisited coord's neighbours coordinates
    """
    i, j = coord
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    return [
        ((i + k, j + l), coord)
        for k, l in dirs
        if (i + k, j + l) not in already_visited
        and is_valid(graph, coord, (i + k, j + l))
    ]


def bfs(graph: np.ndarray, start: tuple, end: int = 26) -> int:
    """Performs Breadth First Search from a start position until it finds the end node.

    Args:
        graph (np.ndarray): Array with each position's height
        start (tuple, optional): Coordinates of starting position
        end (int, optional): Value of target node. Defaults to 26.

    Returns:
        int: Returns the length of the shortest path from start until the end.
    """
    N, M = graph.shape

    # Initialization
    depth = np.zeros((N, M), dtype=np.uint32)
    depth[start] = 0
    already_visited = set()
    already_visited.add(start)
    queue = find_unvisited_neighbours(graph, start, already_visited)
    end_found = False

    # Loops over the queued nodes
    while not end_found and len(queue) > 0:
        coord, parent = queue.pop(0)
        if coord not in already_visited:
            depth[coord] = depth[parent] + 1
            already_visited.add(coord)
            if graph[coord] == end:
                end_found = True
            else:
                queue += find_unvisited_neighbours(graph, coord, already_visited)
    if end_found:
        return depth[coord]
    else:
        # If not found, returns infinity
        return np.inf


def part_1(file: str) -> int:
    """Computes the shortest path from starting position to final position.

    Args:
        file (str): Path to puzzle file

    Returns:
        int: Lenght of the shortest path between start and end
    """
    graph = load_graph(file)
    start = np.unravel_index(np.argmin(graph), graph.shape)
    return bfs(graph=graph, start=start)


def part_2(file: str) -> int:
    """Computes the shortest possible path from "a" to "E" in the graph.

    Args:
        file (str): Path to puzzle file

    Returns:
        int: Lenght of the shortest possible path between any "a" and E nodes
    """
    graph = load_graph(file)

    initials = np.argwhere(graph <= 0)

    min_val = np.inf
    for coord in initials:
        coord = tuple(coord)
        path_length = bfs(graph=graph, start=coord)
        if min_val > path_length:
            min_val = path_length
    return min_val


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solves Day 12 puzzles")
    parser.add_argument("--file", type=str, help="Path to puzzle file")
    args = parser.parse_args()

    sol1 = part_1(file=args.file)
    sol2 = part_2(file=args.file)

    print(f"Part 1 solution: {sol1}")
    print(f"Part 2 solution: {sol2}")
