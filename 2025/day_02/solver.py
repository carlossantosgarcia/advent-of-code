import argparse


def is_string_doubled(input_string: str) -> bool:
    """Check if string consists of exactly two repetitions of a substring."""
    max_len = len(input_string) // 2
    for k in range(1, max_len + 1):
        chunks = input_string.split(input_string[:k])
        if len(set(chunks)) == 1 and len(chunks) == 3:
            return True
    return False


def has_repeating_pattern(input_string: str) -> bool:
    """Check if string consists of a repeating substring pattern."""
    max_len = len(input_string) // 2
    for k in range(1, max_len + 1):
        chunks = input_string.split(input_string[:k])
        if len(set(chunks)) == 1:
            return True
    return False


def part_1(file: str) -> int:
    with open(file, 'r') as file:
        data = file.read().split(",")

    count = 0
    for row in data:
        start, end = row.split("-")
        start, end = int(start), int(end)
        for i in range(end - start + 1):
            candidate = str(start + i)
            if is_string_doubled(candidate):
                count += int(candidate)
    return count


def part_2(file: str) -> int:
    with open(file, 'r') as file:
        data = file.read().split(",")

    count = 0
    for row in data:
        start, end = row.split("-")
        start, end = int(start), int(end)
        for i in range(end - start + 1):
            candidate = str(start + i)
            if has_repeating_pattern(candidate):
                count += int(candidate)
    return count


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solves current day puzzles")
    parser.add_argument("--file", type=str, help="Path to puzzle file")
    args = parser.parse_args()

    sol1 = part_1(file=args.file)
    sol2 = part_2(file=args.file)

    print(f"Part 1 solution: {sol1}")
    print(f"Part 2 solution: {sol2}")
