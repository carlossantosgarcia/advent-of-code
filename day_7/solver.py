import argparse


class Node:
    def __init__(self, name: str, parent, depth: int, node_type: str, size: int = None):
        """Creates nodes for a tree structure

        Args:
            name (str): Name of the file/directory
            parent (_type_): Parent node
            depth (int): Depth in the tree
            node_type (str): Can either be "file" or "dir"
            size (int, optional): Size of the file/directory. Defaults to None.
        """
        self.name = name
        self.parent = parent
        self.children = []
        self.depth = depth
        self.node_type = node_type
        self.size = size

    def add_child(self, child):
        self.children.append(child)


def create_depth_to_nodes_dict(file: str) -> dict[int, list[Node]]:
    """Creates a dictionary mapping tree depths to the corresponding nodes in the tree

    Args:
        file (str): Path to puzzle file

    Returns:
        dict[int,list[Node]]: Dictionary mapping depths to nodes
    """

    # Initialization
    depth = 0
    depth_to_node = {}
    parent = None

    with open(file) as f:
        for line in f:
            line = line.strip()
            if line.startswith("$ cd") and line != "$ cd ..":
                # Handles cd commands
                dir_name = line.split(" ")[2]
                if line == "$ cd /":
                    # Root of the tree
                    curr_dir = Node(
                        name=dir_name, parent=parent, depth=depth, node_type="dir"
                    )
                else:
                    idx = [child.name for child in parent.children].index(dir_name)
                    curr_dir = parent.children[idx]

                try:
                    depth_to_node[depth].append(curr_dir)
                except:
                    depth_to_node[depth] = [curr_dir]

                # Updates parents and depth
                parent = curr_dir
                depth += 1

            elif not line.startswith("$"):
                # Handles ls commands
                filetype, name = line.split(" ")
                if filetype == "dir":
                    node = Node(name=name, parent=parent, depth=depth, node_type="dir")
                else:
                    node = Node(
                        name=name,
                        parent=parent,
                        depth=depth,
                        node_type="file",
                        size=int(filetype),
                    )

                curr_dir.add_child(node)
            elif line == "$ cd ..":
                parent = parent.parent
                depth -= 1
    return depth_to_node


def computes_sizes(depth_to_node: dict[int, list[Node]]) -> None:
    """Updates the attribute size of each node in the tree

    Args:
        depth_to_node (dict[int,list[Node]]): Dictionary mapping depths to nodes
    """
    to_visit = []

    # Initializes sizes for the leafs
    for depth in range(max(depth_to_node.keys()) + 1):
        for node in depth_to_node[depth]:
            if "dir" not in [child.node_type for child in node.children]:
                node.size = sum([child.size for child in node.children])
                to_visit.append(node.parent)

    while len(to_visit) > 0:
        node = to_visit.pop()
        node.size = sum([child.size for child in node.children])
        if node.name != "/" and None not in [v.size for v in node.parent.children]:
            to_visit.append(node.parent)


def part_1(file: str) -> int:
    """Computes the sum of sizes of directories below 100000 units.

    Args:
        file (str): Path to puzzle file

    Returns:
        int: Sum of directories smaller than 100000 units of storage
    """
    # Maps each tree's depth to its nodes
    depth_to_node = create_depth_to_nodes_dict(file)

    # Computes sizes for each node
    computes_sizes(depth_to_node=depth_to_node)

    # Computes the sum of sizes of directories
    sol1 = 0
    for depth in range(max(depth_to_node.keys()) + 1):
        for node in depth_to_node[depth]:
            if node.size < 100000:
                sol1 += node.size
    return sol1


def part_2(file: str) -> int:
    """Finds the size of the smallest directory that needs to be removed to run the update.

    Args:
        file (str): Path to puzzle file

    Returns:
        int: Size of the smallest folder giving enough disk space to run the update
    """
    # Maps each tree's depth to its nodes
    depth_to_node = create_depth_to_nodes_dict(file)

    # Computes sizes for each node
    computes_sizes(depth_to_node=depth_to_node)

    nodes_sizes = []
    for depth in range(max(depth_to_node.keys()) + 1):
        for node in depth_to_node[depth]:
            nodes_sizes.append(node.size)
    nodes_sizes.sort()

    # Computes the size of the smallest directory that gives enough space
    target = 70000000 - nodes_sizes[-1]
    for i in range(len(nodes_sizes)):
        if target + nodes_sizes[i] > 30000000:
            return nodes_sizes[i]


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solves Day 7 puzzles")
    parser.add_argument("--file", type=str, help="Path to puzzle file")
    args = parser.parse_args()

    sol1 = part_1(file=args.file)
    sol2 = part_2(file=args.file)

    print(f"Part 1 solution: {sol1}")
    print(f"Part 2 solution: {sol2}")
