import argparse


def part_1(file: str) -> tuple[list, int]:
    """Computes the calories carried per Elf

    Args:
        file (str): Path to the puzzle input

    Returns:
        tuple[list,int]: List of calories per elf and largest amount of calories carried
    """
    calories_per_elf = []
    with open(file) as f:
        tmp_count = 0
        line = f.readline()
        while line:
            if line != "\n":
                tmp_count += int(line.split("\n")[0])
            else:
                calories_per_elf.append(tmp_count)
                tmp_count = 0
            line = f.readline()
        calories_per_elf.append(tmp_count)
    return calories_per_elf, max(calories_per_elf)


def part_2(file: str) -> int:
    """Computes the sum of the calories carried by the top three Elves.

    Args:
        file (str): Path to the puzzle input

    Returns:
        int: Amount of calories carried in total
    """
    calories_per_elf, _ = part_1(file)
    sorted_calories = sorted(calories_per_elf, reverse=True)
    return sum(sorted_calories[:3])


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solves Day 1 puzzles")
    parser.add_argument("--file", type=str, help="Path to puzzle file")
    args = parser.parse_args()

    _, sol1 = part_1(file=args.file)
    sol2 = part_2(file=args.file)

    print(f"Part 1 solution: {sol1}")
    print(f"Part 2 solution: {sol2}")
