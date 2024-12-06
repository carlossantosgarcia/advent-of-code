import argparse
import collections


def read_data(file: str) -> tuple[dict[int, list[int]], list]:
    """Returns:
        - goes_after: a dictionary where values are lists of pages that go
            after the key page.
        - page_updates: a list of pages to update.
    """
    goes_after = collections.defaultdict(list)
    page_updates = []
    with open(file, 'r') as f:
        for line in f.readlines():
            if "|" in line:
                before, after = line.split("|")
                goes_after[int(before)].append(int(after))
            elif "," in line:
                update = line.strip().split(",")
                page_updates.append([int(n) for n in update])
            else:
                continue
    return goes_after, page_updates


def part_1(file: str) -> int:
    goes_after, page_updates = read_data(file)
    middle = []
    for update in page_updates:
        for idx in range(len(update)):
            if any(
                update[idx] in goes_after[val] for val in update[idx:]
            ):
                break
        else:
            middle.append(update[len(update)//2])
    return sum(middle)


def find_first_page(update: list, goes_after: dict[int, list[int]]) -> int:
    """Finds the first page given the update and goes_after dictionary."""
    if len(update) == 1:
        return update[0]
    for idx in range(len(update)):
        curr = update[idx]
        if all(
            val in goes_after[curr] or curr not in goes_after[val]
            for val in update[:idx] + update[idx+1:]
        ):
            return update[idx]
    return None


def part_2(file: str) -> int:
    goes_after, page_updates = read_data(file)

    incorrectly_ordered = []
    for update in page_updates:
        update_seen = False
        for idx in range(len(update)):
            if any(
                update[idx] in goes_after[val] for val in update[idx:]
            ):
                if not update_seen:
                    incorrectly_ordered.append(update)
                    update_seen = True

    corrected = []
    for update in incorrectly_ordered:
        new_update, remaining = [], update.copy()
        while len(new_update) != len(update):
            new_update.append(find_first_page(remaining, goes_after))
            remaining.pop(remaining.index(new_update[-1]))
        corrected.append(new_update)
    return sum([update[len(update)//2] for update in corrected])


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solves current day puzzles")
    parser.add_argument("--file", type=str, help="Path to puzzle file")
    args = parser.parse_args()

    sol1 = part_1(file=args.file)
    sol2 = part_2(file=args.file)

    print(f"Part 1 solution: {sol1}")
    print(f"Part 2 solution: {sol2}")
