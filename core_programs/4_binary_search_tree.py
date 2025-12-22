# Binary Search Tree
# Use class
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

        # 🌳 PRINT TREE
    def print_tree(self):
        self._print_tree(self.root, 0)

    def _print_tree(self, node, level):
        if node is not None:
            self._print_tree(node.right, level + 1)
            print("   " * level + str(node.number))
            self._print_tree(node.left, level + 1)
# main
inputted_number=0
binary_search_tree=BinarySearchTree()
while inputted_number!=100:# Enable user to input until maximum input is reached(31 inputs)(Use while?)
    try:
        user_input=int(input("Enter number:"))
        binary_search_tree.insert(user_input)
        inputted_number+=1
    except:
        print("You have entered a non-integer/have typed done. Creating tree") # If number is reached/ user typed done. Print tree
        binary_search_tree.print_tree()
        break

if inputted_number==100:
    print("You have reached the maximum amount of inputs. Creating tree.") # If number is reached/ user typed done. Print tree
    binary_search_tree.print_tree()
    exit
else:
    exit