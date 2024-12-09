import argparse
import itertools

int2func = {
    "0": lambda x, y: x + y,
    "1": lambda x, y: x * y,
    "2": lambda x, y: int(str(x) + str(y)),
}


def read_input(file: str) -> tuple[list, list]:
    lst_results, lst_options = [], []
    with open(file, 'r') as f:
        for line in f.readlines():
            eq = line.split(":")
            res = eq[0]
            options = eq[1].strip().split(" ")
            lst_results.append(int(res))
            lst_options.append([int(n) for n in options])
    return lst_results, lst_options


def equation_is_true(result: int, options: list[int], ops: str = "01") -> bool:
    combs = itertools.product(ops, repeat=len(options)-1)
    for comb in combs:
        updated_options = options.copy()
        for op in comb:
            v1, v2 = updated_options.pop(0), updated_options.pop(0)
            new_value = int2func[op](v1, v2)
            updated_options.insert(0, new_value)
        if updated_options[0] == result:
            return True
    return False


def part_1(file: str, ops="01") -> int:
    lst_results, lst_options = read_input(file)
    total = 0
    for res, options in zip(lst_results, lst_options):
        if equation_is_true(res, options, ops=ops):
            total += res
    return total


def part_2(file: str) -> int:
    return part_1(file, ops="012")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solves current day puzzles")
    parser.add_argument("--file", type=str, help="Path to puzzle file")
    args = parser.parse_args()

    sol1 = part_1(file=args.file)
    sol2 = part_2(file=args.file)

    print(f"Part 1 solution: {sol1}")
    print(f"Part 2 solution: {sol2}")
