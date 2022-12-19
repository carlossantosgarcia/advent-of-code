import argparse
import math
import re


def create_initial_state(file: str) -> dict:
    """Creates a dict with each monkey's information.

    Args:
        file (str): Path to puzzle file

    Returns:
        dict: Initial state of the problem
    """
    monkeys = {}
    operations = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
    }

    with open(file) as f:
        for line in f:
            line = line.strip()
            if line.startswith("Monkey"):
                # Creates monkey
                curr_monkey = int(re.findall(r"\d+", line)[0])
                monkeys[curr_monkey] = {"inspections": 0}
                monkeys[curr_monkey]["throws"] = [None, None]
            elif line.startswith("Starting items:"):
                # Adds items to monkey
                items = [int(v) for v in re.findall(r"\d+", line)]
                monkeys[curr_monkey]["items"] = items
            elif line.startswith("Operation:"):
                # Adds operation to monkey
                _, op, b = line.split("=")[1].split(" ")[1:]
                monkeys[curr_monkey]["basic_op"] = op
                try:
                    monkeys[curr_monkey]["val"] = int(b)
                    monkey_op = lambda x, n: operations[monkeys[n]["basic_op"]](
                        x, monkeys[n]["val"]
                    )
                except:
                    if b == "old":
                        monkey_op = lambda x, n: operations[monkeys[n]["basic_op"]](
                            x, x
                        )
                monkeys[curr_monkey]["op"] = monkey_op
            elif line.startswith("Test:"):
                monkeys[curr_monkey]["divisible_by"] = int(re.findall(r"\d+", line)[0])
            elif line.startswith("If true"):
                monkeys[curr_monkey]["throws"][1] = int(re.findall(r"\d+", line)[0])
            elif line.startswith("If false"):
                monkeys[curr_monkey]["throws"][0] = int(re.findall(r"\d+", line)[0])
    return monkeys


def apply_monkey_operation(monkey_nb: int, input_val: int, monkeys: dict) -> int:
    """Applies the operation of a given monkey on the input value.

    Args:
        monkey_nb (int): Number of the given monkey
        input_val (int): Input value
        monkeys (dict): State of the problem

    Returns:
        int: Result of the operation
    """
    return monkeys[monkey_nb]["op"](input_val, monkey_nb)


def play_rounds(monkeys: dict, nb_rounds: int, part: int) -> dict:
    """Plays a chosen number of rounds where the monkeys inspect and play with the items.

    Args:
        monkeys (dict): Dictionary with the state of the game
        nb_rounds (int): Number of rounds to play
        part (int): Part 1 or 2 of the problem

    Returns:
        dict: Final state of the game
    """
    if part == 2:
        ppcm = math.prod([monkeys[i]["divisible_by"] for i in range(len(monkeys))])

    for _ in range(nb_rounds):
        for m in range(len(monkeys)):
            while len(monkeys[m]["items"]) > 0:

                worry = monkeys[m]["items"].pop(0)
                if part == 1:
                    final_worry = math.floor(
                        apply_monkey_operation(m, worry, monkeys) / 3
                    )
                else:
                    final_worry = apply_monkey_operation(m, worry, monkeys) % ppcm

                # Target monkey
                target = monkeys[m]["throws"][
                    1 * (final_worry % monkeys[m]["divisible_by"] == 0)
                ]

                # Item sent to target
                monkeys[target]["items"].append(final_worry)

                # Counts inspections
                monkeys[m]["inspections"] += 1
    return monkeys


def compute_result(final_state: dict) -> int:
    """Computes final monkey business score.

    Args:
        monkeys (dict): Dictionary with the final state of the game

    Returns:
        int: Final level of monkey business
    """
    inspections = [final_state[i]["inspections"] for i in range(len(final_state))]
    inspections.sort()
    return math.prod(inspections[-2:])


def solver(file: str, part: int) -> int:
    """Runs Monkey in the Middle game and computes the final monkey business level.

    Args:
        file (str): Path to puzzle file
        part (int): Part of the problem to solve.

    Returns:
        int: Returns the final monkey business score
    """
    monkeys = create_initial_state(file=file)
    nb_rounds = 20 if part == 1 else 10000

    # Plays the rounds
    final_state = play_rounds(monkeys=monkeys, nb_rounds=nb_rounds, part=part)

    return compute_result(final_state)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solves Day 11 puzzles")
    parser.add_argument("--file", type=str, help="Path to puzzle file")
    args = parser.parse_args()

    sol1 = solver(file=args.file, part=1)
    sol2 = solver(file=args.file, part=2)

    print(f"Part 1 solution: {sol1}")
    print(f"Part 2 solution: {sol2}")
