import argparse

import numpy as np

move2delta = {'<': (0, -1), '>': (0, 1), '^': (-1, 0), 'v': (1, 0)}


def coords_to_move(data, pos, move):
    to_move = []
    x, y = pos
    dx, dy = move2delta[move]
    while not np.isin(data[x+dx, y+dy], ["#", "."]):
        to_move.append((x, y))
        x, y = (x + dx, y + dy)
    if data[x+dx, y+dy] == ".":
        # Found an empty space
        to_move.append((x, y))
    elif data[x+dx, y+dy] == "#":
        # Only found a wall so cannot move
        to_move = []
    return to_move


def move_small_blocks(data, pos, move):
    to_move = coords_to_move(data, pos, move)
    if not len(to_move):
        return pos, data
    dx, dy = move2delta[move]
    for x, y in reversed(to_move):
        data[x+dx, y+dy] = data[x, y]
    data[x, y] = "."
    return (x+dx, y+dy), data


def part_1(file: str) -> int:
    data = []
    moves = []
    found_separator = False

    with open(file, "r") as f:
        for line in f:
            if not found_separator:
                if line.strip() == "":
                    found_separator = True
                else:
                    data.append(list(line.strip()))
            else:
                moves.extend(list(line.strip()))
    data = np.array(data)
    pos = np.where(data == "@")
    pos = (int(pos[0][0]), int(pos[1][0]))

    for move in moves:
        pos, data = move_small_blocks(data, pos, move)

    return sum(100*x + y for x, y in zip(*np.where(data == "O")))


def add_next_big_blocks(data, x, dx, cols):
    cols_to_add = []
    for col in cols:
        if np.isin(data[x, col], ["[", "]"]):
            match data[x+dx, col]:
                case ".":
                    # pass
                    cols_to_add.append(col)
                case "[":
                    cols_to_add.extend([col, col+1])
                case "]":
                    cols_to_add.extend([col-1, col])
                case "#":
                    # pass
                    cols_to_add.append(col)
    return sorted(list(set(cols_to_add)))


def find_coords_to_move(data, pos, move):
    if move in ["<", ">"]:
        # Use part 1 solution to move small blocks
        return coords_to_move(data, pos, move)
    else:
        x, y = pos
        dx, dy = move2delta[move]
        if data[x+dx, y+dy] == ".":
            return [(x, y)]
        elif data[x+dx, y+dy] == "#":
            return []
        else:
            # Found a big block
            dcol = 1 if data[x+dx, y+dy] == "[" else -1
            curr_x = x + dx
            x2cols = {x + dx: [y, y+dcol]}
            x2blocks = {x: [y], x + dx: [y, y+dcol]}
            while ("#" not in data[curr_x, x2cols[curr_x]] and
                   not np.all(data[curr_x, x2cols[curr_x]] == ".")):
                cols_to_add = add_next_big_blocks(
                    data, curr_x, dx, x2cols[curr_x])
                x2cols[curr_x+dx] = cols_to_add
                curr_x += dx
                x2blocks[curr_x] = [y for y in cols_to_add if np.isin(
                    data[curr_x, y], ["[", "]"])]
            if "#" in data[curr_x, x2cols[curr_x]] or not x2cols[curr_x]:
                return []
            else:
                to_move = [(x, y) for x, cols in x2blocks.items()
                           for y in cols]
                return to_move


def move_bigger_blocks(data, pos, move):
    to_move = find_coords_to_move(data, pos, move)
    if not len(to_move):
        return pos, data
    dx, dy = move2delta[move]
    # print("Coords", to_move, "will be moved by", dx, dy)
    if dy:
        for x, y in reversed(to_move):
            data[x+dx, y+dy] = data[x, y]
        data[x, y] = "."
        return (x+dx, y+dy), data
    else:
        sorted_moves = sorted(to_move, key=lambda x: (2*int(dx < 0)-1)*x[0])
        # print(sorted_moves)
        for x, y in sorted_moves:
            data[x+dx, y+dy] = data[x, y]
            if (x-dx, y-dy) not in sorted_moves and data[x, y] != "@":
                # print(x-dx, y-dy)
                data[x, y] = "."
        data[x, y] = "."
        return (x + dx, y + dy), data


def part_2(file: str) -> int:
    data = []
    moves = []
    found_separator = False

    char2value = {
        "#": ["#"] * 2,
        "O": ["[", "]"],
        ".": ["."] * 2,
        "@": ["@", "."],
    }

    with open(file, "r") as f:
        for line in f:
            if not found_separator:
                if line.strip() == "":
                    found_separator = True
                else:
                    row = []
                    for char in list(line.strip()):
                        row.extend(char2value[char])
                    data.append(row)
            else:
                moves.extend(list(line.strip()))
    data = np.array(data)
    pos = np.where(data == "@")
    pos = (int(pos[0][0]), int(pos[1][0]))

    for move in moves:
        pos, data = move_bigger_blocks(data, pos, move)

    return sum(100*x + y for x, y in zip(*np.where(data == "[")))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solves current day puzzles")
    parser.add_argument("--file", type=str, help="Path to puzzle file")
    args = parser.parse_args()

    sol1 = part_1(file=args.file)
    sol2 = part_2(file=args.file)

    print(f"Part 1 solution: {sol1}")
    print(f"Part 2 solution: {sol2}")
