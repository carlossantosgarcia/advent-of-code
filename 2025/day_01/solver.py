import argparse


def part_1(file: str) -> int:
    with open(file, 'r') as file:
        data = file.read().strip().split('\n')
    theta = 50
    total_count = 0
    for row in data:
        mul = 1 if row.startswith('R') else -1
        theta += mul * int(row[1:])
        theta %= 100
        if not theta:
            total_count += 1
    return total_count


def part_2(file: str) -> int:
    with open(file, 'r') as file:
        data = file.read().strip().split('\n')
    theta = 50
    through_zero = 0
    history = [theta]
    for row in data:
        mul = 1 if row.startswith('R') else -1
        rot, res = divmod(int(row[1:]), 100)
        theta += mul * res
        through_zero += rot
        if theta * history[-1] < 0 or (theta > 100):
            through_zero += 1
        theta = theta % 100
        if not theta:
            through_zero += 1
        history.append(theta)
    return through_zero


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solves current day puzzles")
    parser.add_argument("--file", type=str, help="Path to puzzle file")
    args = parser.parse_args()

    sol1 = part_1(file=args.file)
    sol2 = part_2(file=args.file)

    print(f"Part 1 solution: {sol1}")
    print(f"Part 2 solution: {sol2}")
