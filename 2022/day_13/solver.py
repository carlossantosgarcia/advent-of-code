import argparse
import ast


def read_input(file: str) -> list:
    """Loads input file to a list of couples to compare.

    Args:
        file (str): Path to puzzle file

    Returns:
        list: List of couples to compare
    """
    packets = []
    with open(file) as f:
        raw = f.read().splitlines()
    for i in range(len(raw) // 3 + 1):
        u, v = raw[3 * i : 3 * i + 2]
        packets.append([ast.literal_eval(u), ast.literal_eval(v)])
    return packets


def compare(left, right) -> bool:
    """Compares two values recursively.

    Args:
        left (int or list): _description_
        right (int or list): _description_

    Returns:
        bool: Returns True if the inputs are in the right order
    """
    if type(left) == type(right) and type(left) == int:
        if left != right:
            return left < right
    elif type(left) == type(right) and type(left) == list:
        if len(left) == 0:
            return True
        elif len(right) == 0:
            return False
        else:
            for i, val in enumerate(zip(left, right)):
                l, r = val
                out = compare(l, r)
                if out is not None:
                    return out
            if i == len(left) - 1:
                return True
            else:
                return False
    elif type(left) == int:
        out = compare([left], right)
        if out is not None:
            return out
    elif type(right) == int:
        out = compare(left, [right])
        if out is not None:
            return out


def bubble_sort(idx_list: list, compare: callable, packets_list: list) -> None:
    """Sorts input_list in place using a bubble_sort technique.

    Works on the indices of the packets instead of on the packets themselves.

    Args:
        idx_list (list): List of indices of the packets
        compare (callable): Function to call on two elements to check wether they are properly ordered
        packets_list (list): The actual packets to compare
    """
    N = len(idx_list)

    for i in range(N):
        for j in range(0, N - i - 1):
            if not compare(packets_list[idx_list[j]], packets_list[idx_list[j + 1]]):
                idx_list[j], idx_list[j + 1] = idx_list[j + 1], idx_list[j]


def part_1(file: str) -> int:
    """Computes the sum of the indices of the packets in the right order.

    Args:
        file (str): Path to puzzle file

    Returns:
        int: Sum of the indices of the pairs of packets in the right order
    """
    packets = read_input(file)
    comparisons = [compare(left, right) for left, right in packets]
    return sum([i + 1 for i, val in enumerate(comparisons) if val])


def part_2(file: str) -> int:
    """Sorts the packets in the appropriate order and computes the final score.

    Args:
        file (str): Path to puzzle file

    Returns:
        int: Returns the product of the indices of the divider packets after sorting them.
    """
    packets = read_input(file)

    # Creates a list with the packets
    packets_list = [[[2]], [[6]]]
    for pair in packets:
        packets_list += [pair[0], pair[1]]

    # Sorts the list
    idx_list = list(range(len(packets_list)))
    bubble_sort(idx_list, compare, packets_list)
    sorted_packets = [packets_list[idx] for idx in idx_list]

    return (sorted_packets.index(packets_list[0]) + 1) * (
        sorted_packets.index(packets_list[1]) + 1
    )


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solves Day 13 puzzles")
    parser.add_argument("--file", type=str, help="Path to puzzle file")
    args = parser.parse_args()

    sol1 = part_1(file=args.file)
    sol2 = part_2(file=args.file)

    print(f"Part 1 solution: {sol1}")
    print(f"Part 2 solution: {sol2}")
