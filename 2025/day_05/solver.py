import argparse


def read_file(file: str) -> tuple[list[str], list[int]]:
    with open(file, "r") as f:
        content = f.read().strip()
        ranges_section, ingredients_section = content.split("\n\n")
        ranges = ranges_section.split("\n")
        ingredients = [int(line) for line in ingredients_section.split("\n")]
        return ranges, ingredients


def ingredient_in_ranges(ingredient: int, ranges: list[str]) -> bool:
    """Checks if ingredient falls within any of the given ranges."""
    for r in ranges:
        low, high = map(int, r.split('-'))
        if low <= ingredient <= high:
            return True
    return False


def part_1(file: str) -> int:
    ranges, ingredients = read_file(file)
    count = 0
    for n in ingredients:
        if not ingredient_in_ranges(n, ranges):
            count += 1
    return count


def count_valid_ingredients(ranges: list[str]) -> int:
    "Counts the valid ingredients withing non-overlapping ranges."
    count = 0
    for r in ranges:
        low, high = map(int, r.split('-'))
        count += (high - low + 1)
    return count


def part_2(file: str) -> int:
    ranges, _ = read_file(file)
    while True:
        merged_ranges = [ranges[0]]
        for r in ranges[1:]:
            low, high = map(int, r.split('-'))
            was_merged = False
            for i, seen_r in enumerate(merged_ranges):
                merged_low, merged_high = map(int, seen_r.split('-'))
                # Check for overlap (easier to reason about non-overlap)
                if not (merged_high < low or high < merged_low):
                    new_low = min(low, merged_low)
                    new_high = max(high, merged_high)
                    merged_ranges[i] = f"{new_low}-{new_high}"
                    was_merged = True
            if not was_merged:
                merged_ranges.append(r)
        if (merged_ranges == ranges):
            break
        ranges = merged_ranges.copy()
    return count_valid_ingredients(merged_ranges)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solves current day puzzles")
    parser.add_argument("--file", type=str, help="Path to puzzle file")
    args = parser.parse_args()

    sol1 = part_1(file=args.file)
    sol2 = part_2(file=args.file)

    print(f"Part 1 solution: {sol1}")
    print(f"Part 2 solution: {sol2}")
