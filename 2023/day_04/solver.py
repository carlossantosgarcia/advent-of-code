import argparse
from typing import Sequence


def parse_input(line: str) -> tuple[set[int], Sequence[int]]:
    """Parses each line corresponding to a card."""
    winning_nums, my_nums = line.split(" | ")
    winning_nums = winning_nums.split(": ")[-1]
    winning_nums = {int(n) for n in winning_nums.split() if n}
    my_nums = [int(n) for n in my_nums.split() if n]
    return winning_nums, my_nums


def compute_score(winning_nums: set[int], my_nums: Sequence[int]) -> int:
    """Computes the score from a card."""
    power = -1
    for num in my_nums:
        if num in winning_nums:
            power += 1
    return 2**power if power != -1 else 0


def count_matches(winning_nums: set[int], my_nums: Sequence[int]) -> int:
    """Counts the number of matches in a card."""
    return len([n for n in my_nums if n in winning_nums])


def part_1(file: str) -> int:
    """Computes the sum of the number of points obtained per card.

    Args:
        file (str): Path to the puzzle input

    Returns:
        int: Total sum of points.
    """
    total_points = []
    with open(file) as f:
        for line in f.readlines():
            points = compute_score(*parse_input(line.rstrip()))
            total_points.append(points)
    return sum(total_points)


def part_2(file: str) -> int:
    """Computes the final number of scratchcards.

    Args:
        file (str): Path to the puzzle input

    Returns:
        int: The final number of scratchcards.
    """
    with open(file) as f:
        lines = f.readlines()
        games = range(1, (N := len(lines)) + 1)
        values = [1] * N
        occurrences = dict(zip(games, values))

    for idx, line in enumerate(lines):
        game_id = idx + 1
        count = count_matches(*parse_input(line.rstrip()))
        if count:
            for k in range(1, count + 1):
                occurrences[game_id + k] += occurrences[game_id]

    return sum([val for _, val in occurrences.items()])


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solves Day 4 puzzles")
    parser.add_argument("--file", type=str, help="Path to puzzle file")
    args = parser.parse_args()

    sol1 = part_1(file=args.file)
    sol2 = part_2(file=args.file)

    print(f"Part 1 solution: {sol1}")
    print(f"Part 2 solution: {sol2}")
