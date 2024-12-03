import argparse
import re


def part_1(file: str) -> int:
    with open(file, 'r') as f:
        instructions = "".join(line.strip() for line in f.readlines())
    pattern = r"mul\((\d+),(\d+)\)"
    return sum(int(a) * int(b) for a, b in re.findall(pattern, instructions))


def part_2(file: str) -> int:
    with open(file, 'r') as f:
        instructions = "".join(line.strip() for line in f.readlines())
    pattern = r"mul\((\d+),(\d+)\)"
    to_remove = [(m.start(), m.end())
                 for m in re.finditer(r"don't\(\)(.*?)do\(\)", instructions)]
    start = 0
    new_instructions = ""
    for i, j in to_remove:
        end = i
        new_instructions += instructions[start:end]
        start = j
    new_instructions += instructions[start:]
    return sum(int(a) * int(b) for a, b in
               re.findall(pattern, new_instructions))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solves current day puzzles")
    parser.add_argument("--file", type=str, help="Path to puzzle file")
    args = parser.parse_args()

    sol1 = part_1(file=args.file)
    sol2 = part_2(file=args.file)

    print(f"Part 1 solution: {sol1}")
    print(f"Part 2 solution: {sol2}")
