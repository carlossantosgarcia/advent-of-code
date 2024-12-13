import argparse
import functools


def blink(input_str: str) -> list[str]:
    """Applies one blinking step to the input stone."""
    match input_str:
        case '0':
            return ['1']
        case _ if len(input_str) % 2 == 0:
            return [
                input_str[:len(input_str)//2],
                str(int(input_str[len(input_str)//2:])),
            ]
        case _:
            return [str(2024 * int(input_str))]


def part_1(file: str) -> int:
    with open(file) as f:
        stones = f.readlines()[0].split(" ")
    for _ in range(25):
        new_stones = []
        for stone in stones:
            new_stones.extend(blink(stone))
        stones = new_stones
    return len(stones)


@functools.cache
def recursively_count_stones(input_str: str, depth: int) -> int:
    """Recursively counts stones after applying the blinking rule."""
    if not depth:
        return 1
    elif input_str == '0':
        return recursively_count_stones('1', depth - 1)
    elif (length := len(input_str)) % 2 == 0:
        return (
            recursively_count_stones(input_str[:length//2], depth - 1) +
            recursively_count_stones(
                str(int(input_str[length//2:])), depth - 1)
        )

    else:
        return recursively_count_stones(str(2024 * int(input_str)), depth - 1)


def part_2(file: str) -> int:
    with open(file) as f:
        stones = f.readlines()[0].split(" ")
    return sum(recursively_count_stones(stone, 75) for stone in stones)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solves current day puzzles")
    parser.add_argument("--file", type=str, help="Path to puzzle file")
    args = parser.parse_args()

    sol1 = part_1(file=args.file)
    sol2 = part_2(file=args.file)

    print(f"Part 1 solution: {sol1}")
    print(f"Part 2 solution: {sol2}")
