import argparse
import math
import re


def nb_steps_until_condition(
        node: str,
        node_to_children: dict[str, dict[str, str]],
        steps_to_perform: list[str],
        condition: callable) -> int:
    """Counts the number of steps needed to go from node until matching the
    given condition."""
    idx, found = 0, False
    while not found:
        direction = steps_to_perform[idx % len(steps_to_perform)]
        node = node_to_children[node][direction]
        if condition(node):
            found = True
        idx += 1
    return idx


def part_1(file: str) -> int:
    """Computes the number of steps needed to go from AAA to ZZZ.

    Args:
        file (str): Path to the puzzle input

    Returns:
        int: Total number of steps needed.
    """
    # Parse input
    pattern = re.compile(r'(\w+) = \((\w+), (\w+)\)')
    node_to_children = {}
    with open(file) as f:
        for idx, line in enumerate(f.readlines()):
            if not idx:
                steps_to_perform = list(line.rstrip())
            else:
                match = pattern.match(line.rstrip())
                if match:
                    parent, left, right = match.groups()
                    node_to_children[parent] = {'L': left, 'R': right}

    start_node = "AAA"
    def condition(node: str) -> bool: return node == "ZZZ"
    nb_steps = nb_steps_until_condition(
        start_node, node_to_children, steps_to_perform, condition)
    return nb_steps


def part_2(file: str) -> int:
    """Computes the number of steps needed for all starting nodes to visit at
    the same time nodes having 'Z' as a final character.

    Args:
        file (str): Path to the puzzle input

    Returns:
        int: The minimal number of steps needed.
    """
    # Parse input
    pattern = re.compile(r'(\w+) = \((\w+), (\w+)\)')
    node_to_children = {}
    with open(file) as f:
        for idx, line in enumerate(f.readlines()):
            if not idx:
                steps_to_perform = list(line.rstrip())
            else:
                match = pattern.match(line.rstrip())
                if match:
                    parent, left, right = match.groups()
                    node_to_children[parent] = {'L': left, 'R': right}

    start_nodes = [node for node in node_to_children if node[-1] == "A"]
    def condition(node: str) -> bool: return node[-1] == "Z"
    lengths = []
    for node in start_nodes:
        lengths.append(nb_steps_until_condition(
            node, node_to_children, steps_to_perform, condition))

    return math.lcm(*lengths)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solves Day 8 puzzles")
    parser.add_argument("--file", type=str, help="Path to puzzle file")
    args = parser.parse_args()

    sol1 = part_1(file=args.file)
    sol2 = part_2(file=args.file)

    print(f"Part 1 solution: {sol1}")
    print(f"Part 2 solution: {sol2}")
