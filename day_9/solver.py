import argparse

import numpy as np


def move_tail(h_coord: tuple[int, int], t_coord: tuple[int, int]) -> tuple[int, int]:
    """Moves tail towards head using the rules of motion.

    Args:
        h_coord (tuple[int, int]): Coordinates of the head
        t_coord (tuple[int, int]): Coordinates of the tail

    Returns:
        tuple[int, int]: New position for the tail
    """
    hx, hy = h_coord
    tx, ty = t_coord
    if abs(hx - tx) <= 1 and abs(hy - ty) <= 1:
        # Both knots are touching each other
        return t_coord
    else:
        # Moves tail towards head
        return (tx + np.sign(hx - tx), ty + np.sign(hy - ty))


def solver(file: str, nb_knots: int) -> int:
    """Computes the number of different positions visited by the tail of the rope.

    Args:
        file (str): Path to puzzle file
        nb_knots (int): Number of knots on the rope.

    Returns:
        int: Number of different positions visited by the tail
    """
    actions = np.genfromtxt(file, dtype=None, encoding=None)
    delta_coords = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}
    rope = [(0, 0)] * nb_knots

    tail_visits = set()
    for direction, length in actions:
        for _ in range(length):
            hx, hy = rope[0]
            dx, dy = delta_coords[direction]
            rope[0] = (hx + dx, hy + dy)
            for i in range(1, len(rope)):
                rope[i] = move_tail(rope[i - 1], rope[i])
            tail_visits.add(rope[len(rope) - 1])
    return len(tail_visits)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solves Day 9 puzzles")
    parser.add_argument("--file", type=str, help="Path to puzzle file")
    args = parser.parse_args()

    sol1 = solver(file=args.file, nb_knots=2)
    sol2 = solver(file=args.file, nb_knots=10)

    print(f"Part 1 solution: {sol1}")
    print(f"Part 2 solution: {sol2}")
