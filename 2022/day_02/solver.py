import argparse

import numpy as np


def game_score(opponent_move, own_move):
    """
    Computes the score of a given game.
    """
    if opponent_move == own_move:
        return 3
    elif (opponent_move, own_move) in (
        ("Scissors", "Rock"),
        ("Rock", "Paper"),
        ("Paper", "Scissors"),
    ):
        return 6
    else:
        return 0


def part_1(file: str) -> int:
    """Computes the total score of Rock Paper Scissors games.

    Args:
        file (str): Path to puzzle file

    Returns:
        int: Final score
    """
    puzzle = np.genfromtxt(file, dtype=str)

    opponent_moves = {"A": "Rock", "B": "Paper", "C": "Scissors"}
    own_moves = {"X": "Rock", "Y": "Paper", "Z": "Scissors"}
    moves_scores = {"Rock": 1, "Paper": 2, "Scissors": 3}

    def total_score(input_array):
        """
        Adds the game and moves scores
        """
        opponent_move = opponent_moves[input_array[0]]
        own_move = own_moves[input_array[1]]
        return moves_scores[own_move] + game_score(opponent_move, own_move)

    scores = np.apply_along_axis(total_score, 1, puzzle)
    return np.sum(scores)


def part_2(file: str) -> int:
    """Computes the total score of Rock Paper Scissors games.
    Now with different rules: I play the move that ensures a given result.

    Args:
        file (str): Path to puzzle file

    Returns:
        int: Final score
    """
    puzzle = np.genfromtxt(file, dtype=str)

    opponent_moves = {"A": "Rock", "B": "Paper", "C": "Scissors"}
    moves_scores = {"Rock": 1, "Paper": 2, "Scissors": 3}
    moves_to_play = ["Rock", "Paper", "Scissors"]
    action_to_move = {"X": -1, "Y": 0, "Z": 1}

    def total_score(input_array):
        """
        Adds the game and moves scores
        """
        opponent_move = opponent_moves[input_array[0]]
        own_move_idx = (
            moves_to_play.index(opponent_move) + action_to_move[input_array[1]]
        ) % 3
        own_move = moves_to_play[own_move_idx]
        return moves_scores[own_move] + game_score(opponent_move, own_move)

    scores = np.apply_along_axis(total_score, 1, puzzle)
    return np.sum(scores)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solves Day 2 puzzles")
    parser.add_argument("--file", type=str, help="Path to puzzle file")
    args = parser.parse_args()

    sol1 = part_1(file=args.file)
    sol2 = part_2(file=args.file)

    print(f"Part 1 solution: {sol1}")
    print(f"Part 2 solution: {sol2}")
