"""Core Programs Module

Shared utilities and algorithm implementations for multiple projects.
- General Utilities: clear_console(), generate_random_value()
- Sections for algorithms: BST, etc.
"""

import os
import random
from typing import Optional, List

# === General Utilities ===

def clear_console() -> None:
    """Clear the console screen (Windows or POSIX)."""
    os.system("cls" if os.name == "nt" else "clear")


def generate_random_value(low: int = 0, high: int = 100) -> int:
    """Return a random integer in the inclusive range [low, high]."""
    return random.randint(low, high)


def pretty_print_diagonal(root, max_depth: int) -> None:
    """Render a top-down view of a tree using diagonal connectors.
    
    Args:
        root: The root node of the tree (must have .value, .left, .right attributes)
        max_depth: Maximum depth of the tree for visualization sizing
    """
    if root is None:
        print("<empty tree>")
        return

    def _height(node) -> int:
        return 0 if node is None else 1 + max(_height(node.left), _height(node.right))

    height = max(max_depth, _height(root))
    width = max(2 ** (height + 2), 16)
    rows = [list(" " * width) for _ in range(height * 2 - 1)]

    def place(node, depth: int, x: int, gap: int) -> None:
        node_row = depth * 2
        val = str(node.value)
        start = max(x - len(val) // 2, 0)
        end = min(start + len(val), width)
        rows[node_row][start:end] = val[: end - start]

        if depth == height - 1:
            return

        connector_row = node_row + 1
        child_gap = max(gap // 2, 1)

        if node.left:
            child_x = x - child_gap
            for i in range(1, child_gap + 1):
                pos = x - i
                if 0 <= pos < width:
                    rows[connector_row][pos] = "/"
            place(node.left, depth + 1, child_x, child_gap)

        if node.right:
            child_x = x + child_gap
            for i in range(1, child_gap + 1):
                pos = x + i
                if 0 <= pos < width:
                    rows[connector_row][pos] = "\\"
            place(node.right, depth + 1, child_x, child_gap)

    place(root, 0, width // 2, width // 2)
    for line in rows:
        print("".join(line).rstrip())


def render_tree_view(title: str, tree, max_depth: int, current_depth: int, status: str = "") -> None:
    """Shared tree renderer for console UIs.

    Args:
        title: Heading to display (e.g., "BINARY TREE VIEW")
        tree: Tree instance with a .root attribute
        max_depth: Maximum allowed depth for the tree
        current_depth: Currently selected/build depth
        status: Optional status line to display
    """
    clear_console()
    print(f"==================== {title} ====================")
    print(f"Max depth: {max_depth} | Current depth: {current_depth}")
    print(f"Status: {status if status else '(none)'}")
    print("--------------------------------------------------")
    if tree is None or getattr(tree, "root", None) is None:
        print("<no tree built>")
    else:
        pretty_print_diagonal(tree.root, max_depth)
    print("==================================================")


def ensure_tree(tree, tree_cls, current_depth: int, max_depth: int, low: int = 0, high: int = 1000):
    """Create and build a full tree when not already present.

    Returns (tree_instance, status_message).
    """
    if tree is not None:
        return tree, ""

    instance = tree_cls(max_depth=max_depth)
    instance.build_full_tree(target_depth=current_depth, low=low, high=high)
    return instance, f"Initialized tree at depth {current_depth}."


# === BST Implementation ===

class Node:
    """Represents a single node in the binary search tree."""

    def __init__(self, value: int) -> None:
        self.value = value
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None

    def __repr__(self) -> str:
        return f"Node({self.value})"


# === Binary Tree (general) Implementation ===

class BinaryTree:
    """Basic binary tree with traversals and level-order builders."""

    def __init__(self, max_depth: int = 5) -> None:
        self.root: Optional[Node] = None
        self.max_depth = max_depth

    def insert(self, value: int) -> None:
        """Insert by filling the first available slot in level order."""
        new_node = Node(value)
        if self.root is None:
            self.root = new_node
            return

        queue: List[Node] = [self.root]
        while queue:
            current = queue.pop(0)
            if current.left is None:
                current.left = new_node
                return
            queue.append(current.left)
            if current.right is None:
                current.right = new_node
                return
            queue.append(current.right)

    def build_full_tree(self, target_depth: int, low: int = 0, high: int = 1000) -> None:
        """Build a complete binary tree up to target_depth with random values."""
        if target_depth < 1 or target_depth > self.max_depth:
            raise ValueError(f"target_depth must be between 1 and {self.max_depth}")

        needed = 2 ** target_depth - 1
        available = high - low + 1
        if available < needed:
            raise ValueError(f"Value range too small: need at least {needed} distinct ints, have {available}")

        values = random.sample(range(low, high + 1), needed)
        nodes = [Node(v) for v in values]
        for idx, node in enumerate(nodes):
            left_idx = 2 * idx + 1
            right_idx = 2 * idx + 2
            if left_idx < len(nodes):
                node.left = nodes[left_idx]
            if right_idx < len(nodes):
                node.right = nodes[right_idx]
        self.root = nodes[0] if nodes else None

    def preorder(self) -> List[int]:
        result: List[int] = []

        def traverse(node: Optional[Node]) -> None:
            if node is None:
                return
            result.append(node.value)
            traverse(node.left)
            traverse(node.right)

        traverse(self.root)
        return result

    def inorder(self) -> List[int]:
        result: List[int] = []

        def traverse(node: Optional[Node]) -> None:
            if node is None:
                return
            traverse(node.left)
            result.append(node.value)
            traverse(node.right)

        traverse(self.root)
        return result

    def postorder(self) -> List[int]:
        result: List[int] = []

        def traverse(node: Optional[Node]) -> None:
            if node is None:
                return
            traverse(node.left)
            traverse(node.right)
            result.append(node.value)

        traverse(self.root)
        return result


class BinarySearchTree:
    """Binary Search Tree model with depth-limited operations.

    Methods return booleans or values and do not print to the console.
    """

    def __init__(self, max_depth: int = 5) -> None:
        self.root: Optional[Node] = None
        self.max_depth = max_depth

    def _height(self, node: Optional[Node]) -> int:
        if node is None:
            return 0
        return 1 + max(self._height(node.left), self._height(node.right))

    def insert(self, value: int) -> bool:
        """Insert a value. Returns True if inserted, False if duplicate or depth-limited."""
        if self.root is None:
            self.root = Node(value)
            return True

        current = self.root
        depth = 1
        while current:
            if depth >= self.max_depth:
                return False

            if value < current.value:
                if current.left is None:
                    current.left = Node(value)
                    return True
                current = current.left
            elif value > current.value:
                if current.right is None:
                    current.right = Node(value)
                    return True
                current = current.right
            else:
                return False

            depth += 1

        return False

    def search(self, value: int) -> bool:
        """Return True if value exists in the tree, else False."""
        current = self.root
        while current:
            if value < current.value:
                current = current.left
            elif value > current.value:
                current = current.right
            else:
                return True
        return False

    def delete(self, value: int) -> bool:
        """Delete a value from the BST. Returns True if deleted, False if not found."""

        def _delete(node: Optional[Node], target: int):
            if node is None:
                return None, False
            if target < node.value:
                node.left, deleted = _delete(node.left, target)
                return node, deleted
            if target > node.value:
                node.right, deleted = _delete(node.right, target)
                return node, deleted

            if node.left is None:
                return node.right, True
            if node.right is None:
                return node.left, True

            successor_parent = node
            successor = node.right
            while successor.left:
                successor_parent = successor
                successor = successor.left
            node.value = successor.value
            if successor_parent.left is successor:
                successor_parent.left = successor.right
            else:
                successor_parent.right = successor.right
            return node, True

        self.root, deleted_flag = _delete(self.root, value)
        return deleted_flag

    def build_full_tree(self, target_depth: int, low: int = 0, high: int = 1000) -> None:
        """Build a complete BST up to target_depth (<= max_depth) with random values."""
        if target_depth < 1 or target_depth > self.max_depth:
            raise ValueError(f"target_depth must be between 1 and {self.max_depth}")

        needed = 2 ** target_depth - 1
        available = high - low + 1
        if available < needed:
            raise ValueError(f"Value range too small: need at least {needed} distinct ints, have {available}")

        values = sorted(random.sample(range(low, high + 1), needed))

        def build(vals: List[int], depth: int) -> Node:
            mid = len(vals) // 2
            node = Node(vals[mid])
            if depth == target_depth:
                return node
            node.left = build(vals[:mid], depth + 1)
            node.right = build(vals[mid + 1 :], depth + 1)
            return node

        self.root = build(values, 1)
