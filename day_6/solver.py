import argparse


def find_marker_idx(seq: str, length: int = 4) -> int:
    """Finds the index of the start-of-packet marker in the input sequence

    Args:
        seq (str): Input string of characters
        length (int, optional): Length of the marker. Defaults to 4.

    Returns:
        int: Index of the start of the
    """
    for i in range(len(seq) - length):
        if len(set(seq[i : i + length])) == length:
            return i


def solver(file: str, length: int) -> int:
    """Finds the index of the end of the start-of-packet marker in a sequence.

    Args:
        file (str): Path to puzzle file
        length (int): Length of the marker

    Returns:
        int: The length from the begginning of the sequence to the end of the marker
    """

    input_sequence = open(file).read().strip()

    marker_idx = find_marker_idx(seq=input_sequence, length=length)

    return marker_idx + length


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solves Day 6 puzzles")
    parser.add_argument("--file", type=str, help="Path to puzzle file")
    args = parser.parse_args()

    sol1 = solver(file=args.file, length=4)
    sol2 = solver(file=args.file, length=14)

    print(f"Part 1 solution: {sol1}")
    print(f"Part 2 solution: {sol2}")
