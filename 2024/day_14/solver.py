import argparse
import copy
import re

import numpy as np
import scipy
import tqdm


def part_1(file: str) -> int:
    W, H = (11, 7) if 'test' in file else (101, 103)
    pattern = r"p\=(-?\d+),(-?\d+) v\=(-?\d+),(-?\d+)"
    positions, speeds = [], []
    with open(file, 'r') as f:
        for line in f.readlines():
            # print(line)
            coords = re.findall(pattern, line)[0]
            positions.append(tuple(int(n) for n in coords[:2]))
            speeds.append(tuple(int(n) for n in coords[2:]))

    seconds = 100

    end_pos = []
    for (x, y), (dx, dy) in zip(positions, speeds):
        end_pos.append(
            (
                (x+(seconds*dx)) % W,
                (y+(seconds*dy)) % H,
            ))

    end = np.zeros((W, H)).astype(int)
    for x, y in end_pos:
        end[x, y] += 1
    end[:, H//2] = 0
    end[W//2, :] = 0

    quadrants = [
        (slice(0, W//2), slice(0, H//2)),
        (slice(0, W//2), slice(H//2, H)),
        (slice(W//2, W), slice(0, H//2)),
        (slice(W//2, W), slice(H//2, H)),
    ]

    return np.prod([end[sl1, sl2].sum() for sl1, sl2 in quadrants])


def largest_cc(data) -> int:
    structure = np.ones((3, 3), dtype=int)
    bin_end = data > 0
    labeled_array, num_features = scipy.ndimage.label(
        bin_end, structure=structure)

    # Calculate the size of each connected component
    component_sizes = scipy.ndimage.sum_labels(
        bin_end, labeled_array, index=np.arange(1, num_features + 1))

    return component_sizes.max()


def part_2(file: str) -> int:
    W, H = (11, 7) if 'test' in file else (101, 103)
    pattern = r"p\=(-?\d+),(-?\d+) v\=(-?\d+),(-?\d+)"
    positions, speeds = [], []
    with open(file, 'r') as f:
        for line in f.readlines():
            # print(line)
            coords = re.findall(pattern, line)[0]
            positions.append(tuple(int(n) for n in coords[:2]))
            speeds.append(tuple(int(n) for n in coords[2:]))

    MAX_SECS = 10000
    ccs = []
    positions2 = copy.deepcopy(positions)
    for _ in tqdm.trange(1, MAX_SECS):
        end_pos = []
        for (x, y), (dx, dy) in zip(positions2, speeds):
            end_pos.append(
                (
                    (x+dx) % W,
                    (y+dy) % H,
                ))
        positions2 = copy.deepcopy(end_pos)

        end = np.zeros((W, H))
        for x, y in end_pos:
            end[x, y] += 1

        ccs.append(largest_cc(end))

    return np.argmax(np.abs(ccs)) + 1


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solves current day puzzles")
    parser.add_argument("--file", type=str, help="Path to puzzle file")
    args = parser.parse_args()

    sol1 = part_1(file=args.file)
    sol2 = part_2(file=args.file)

    print(f"Part 1 solution: {sol1}")
    print(f"Part 2 solution: {sol2}")
