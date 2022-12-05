import argparse
import re


def input_to_dict(stacks: list[str]) -> dict[int, list[str]]:
    """Converts a list of strings into a dictionary with each of the stacks.
    e.g. {1:['Z'], 2: ['M', 'C'], 3: []}

    Args:
        stacks (list[str]): List of the rows from the puzzle

    Returns:
        dict[int, list[str]]: A dictionary mapping integers to their stack
    """
    n_stacks = max([int(n) for n in stacks[-1].replace(" ", "")])
    crates_stacks = {}

    # Only saves actual crates for each stack
    for k in range(n_stacks):
        i = stacks[-1].index(str(k + 1))
        crates_stacks[k + 1] = [
            v
            for j in range(len(stacks) - 1)
            if (v := stacks[j][i]) not in (("["), (" "), ("]"))
        ]
    return n_stacks, crates_stacks


def apply_rearrangements(
    instructions: list[str],
    initial_stacks: dict[int, list[str]],
    crane_model: str = "CrateMover 9000",
) -> dict[int, list[str]]:
    """Applies the rearrangements given as instructions, modifying the stacks of crates.
    Args:
        instructions (list[str]): List of instructions, e.g. ['move 3 from 1 to 3']
        initial_stacks (dict[int, list[str]]): Initial positions of the crates
        crane_model (str, optional): Crane model used rearrange crates. Defaults to "CrateMover 9000".

    Returns:
        dict[int, list[str]]: Final stacks obtained with the given instructions
    """
    for row in instructions:
        number, origin, target = re.findall(r"\d+", row)
        number, origin, target = int(number), int(origin), int(target)

        if crane_model == "CrateMover 9000":
            # Part 1
            for _ in range(number):
                element = initial_stacks[origin].pop(0)
                initial_stacks[target].insert(0, element)

        elif crane_model == "CrateMover 9001":
            # Part 2
            elements = initial_stacks[origin][:number]
            initial_stacks[origin] = initial_stacks[origin][number:]
            initial_stacks[target] = elements + initial_stacks[target]

    return initial_stacks


def solver(file: str, crane_model="CrateMover 9000") -> str:
    """Determines the crates ending up on top of each stack.

    Args:
        file (str): Path to puzzle file
        crane_model (str, optional): Crane model used (useful for part 2). Defaults to 'CrateMover 9000'.

    Returns:
        str: String of crates on top of each stack
    """
    lines = open(file).readlines()
    jump = lines.index("\n")

    # Creates lists with initial arrangement and instructions
    stacks = [row.rstrip("\n") for row in lines[:jump]]
    instructions = [row.rstrip("\n") for row in lines[jump + 1 :]]

    N, initial_stacks = input_to_dict(stacks=stacks)

    final_stacks = apply_rearrangements(
        instructions=instructions,
        initial_stacks=initial_stacks,
        crane_model=crane_model,
    )

    return "".join([final_stacks[i + 1][0] for i in range(N)])


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solves Day 5 puzzles")
    parser.add_argument("--file", type=str, help="Path to puzzle file")
    args = parser.parse_args()

    sol1 = solver(file=args.file, crane_model="CrateMover 9000")
    sol2 = solver(file=args.file, crane_model="CrateMover 9001")

    print(f"Part 1 solution: {sol1}")
    print(f"Part 2 solution: {sol2}")
