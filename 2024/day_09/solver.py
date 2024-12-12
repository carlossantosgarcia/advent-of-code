import argparse


def compute_score(blocks: list[str], idx2uids, new2old) -> int:
    """Computes the score of the current configuration."""
    count = 0
    for idx, val in enumerate(blocks):
        if val == "f":
            uid = idx2uids[new2old[idx]] if idx in new2old else idx2uids[idx]
            count += idx * uid
        else:
            continue
    return count


def part_1(file: str) -> int:
    with open(file) as f:
        data = f.readlines()[0].strip()
    blocks, idx2uids = "", {}
    is_file, uid = True, 0
    for char in data:
        if is_file:
            for idx, _ in enumerate(range(int(char))):
                idx2uids[len(blocks)+idx] = uid
            blocks = blocks + "".join(['f' for _ in range(int(char))])
            uid += 1
            is_file = False
        else:
            blocks = blocks + "".join(["." for _ in range(int(char))])
            is_file = True
    
    def rev(n):
        return len(blocks) - 1 - n
    
    blocks = list(blocks)
    rev_blocks = list(reversed(blocks))

    idx_to_fill = blocks.index(".")
    new2old = {}
    while 'f' in blocks[idx_to_fill:]:
        idx = rev(rev_blocks.index("f"))
        blocks[idx_to_fill], blocks[idx] = blocks[idx], blocks[idx_to_fill]
        rev_blocks[rev(idx_to_fill)], rev_blocks[rev(idx)] = rev_blocks[rev(idx)], rev_blocks[rev(idx_to_fill)]
        new2old[idx_to_fill] = idx
        idx_to_fill = blocks.index(".")
    
    return compute_score(blocks, idx2uids, new2old)


def block_fits(blocks, length, right_idx) -> tuple[bool, int]:
    """Checks wether a block of a given length fits in empty space."""
    target = ["."] * length
    for idx in range(0, right_idx):
        if blocks[idx: idx + length] == target:
            return True, idx
    return False, None


def part_2(file: str) -> int:
    with open(file) as f:
        data = f.readlines()[0].strip()
    blocks, uids2idx, idx2uids = "", {}, {}
    is_file, uid = True, 0
    for char in data:
        if is_file:
            for idx, _ in enumerate(range(int(char))):
                idx2uids[len(blocks)+idx] = uid
            uids2idx[uid] = [len(blocks) + idx for idx, _ in enumerate(range(int(char)))]
            blocks = blocks + "".join(['f' for _ in range(int(char))])
            uid += 1
            is_file = False
        else:
            blocks = blocks + "".join(["." for _ in range(int(char))])
            is_file = True
    blocks = list(blocks)
    new2old = {}
    for uid, indices in reversed(uids2idx.items()):
        length = len(indices)
        can_fit, start_idx = block_fits(blocks, length, right_idx=min(indices))
        if can_fit:
            for b, idx in zip(range(length), indices):
                new2old[start_idx + b] = idx
                blocks[start_idx + b], blocks[idx] = blocks[idx], blocks[start_idx + b]
        else:
            continue
    return compute_score(blocks, idx2uids, new2old)
    

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solves current day puzzles")
    parser.add_argument("--file", type=str, help="Path to puzzle file")
    args = parser.parse_args()

    sol1 = part_1(file=args.file)
    sol2 = part_2(file=args.file)

    print(f"Part 1 solution: {sol1}")
    print(f"Part 2 solution: {sol2}")
