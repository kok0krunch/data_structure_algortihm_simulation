#Binary Search Tree
#Import shared module for organization
#Use core_programs_module to implement BST
import core_programs_module


def pretty_print_diagonal(root, max_depth: int) -> None:
    """Render a top-down view of the BST using diagonal connectors."""
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
class Node:
    def __init__(self,number): # Class attributes: top, left, right
        self.number=number
        self.left=None
        self.right=None

class BinarySearchTree: 
    def __init__(self):
        self.root=None

    # Functions needed
    def insert(self, number):
        if self.root==None: # First number as root
            self.root=Node(number)
        else: # Determine if number is bigger or smaller
            self.branching(self.root,number)

    def branching(self,current,number):
        if number<=current.number: # smaller/equal = left
            if current.left is None:
                current.left=Node(number) # Traverse the tree until it reaches an empty node
            else:
                self.branching(current.left,number)  # Insert in binary tree
        else: # bigger = right
            if current.right is None:
                current.right=Node(number) # Traverse the tree until it reaches an empty node
            else:
                self.branching(current.right,number) # Insert in binary tree

    def print_tree(self): #show the tree
        self._print_tree(self.root, 0)

    def _print_tree(self, node, level):
        if node is not None:
            self._print_tree(node.right, level + 2)
            print("   " * level + str(node.number))
            self._print_tree(node.left, level + 2)

#definitions
def input_number():
    try:
        user_input=int(input("Enter number:"))
        binary_search_tree.insert(user_input)
    except:
        print("You have entered a non-integer/have typed done. Creating tree") # If number is reached/ user typed done. Print tree
        binary_search_tree.print_tree()

# main program
inputted_number=0
binary_search_tree=BinarySearchTree()
while inputted_number!=100:# Enable user to input until maximum input is reached(31 inputs)(Use while?)
    input_number()
    inputted_number+=1

if inputted_number==100:
    print("You have reached the maximum amount of inputs. Creating tree.") # If number is reached/ user typed done. Print tree
    binary_search_tree.print_tree()
    exit
else:
    exit