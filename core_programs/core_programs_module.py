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


# === BST Implementation ===

class Node:
    """Represents a single node in the binary search tree."""

    def __init__(self, value: int) -> None:
        self.value = value
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None

    def __repr__(self) -> str:
        return f"Node({self.value})"


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
