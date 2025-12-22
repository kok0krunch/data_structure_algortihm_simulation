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
        if number>current.number: # smaller/equal = left
            if self.left is None:
                current.left=Node(number) # Traverse the tree until it reaches an empty node
            else:
                self.branching(number)  # Insert in binary tree
        else: # bigger = right
            if self.right is None:
                current.right=Node(number) # Traverse the tree until it reaches an empty node
            else:
                self.branching(number) # Insert in binary tree

# main
inputted_number=0
binary_search_tree=BinarySearchTree()
while inputted_number!=100:# Enable user to input until maximum input is reached(31 inputs)(Use while?)
    user_input=int(input("Enter number:"))
    binary_search_tree.insert(user_input)
# If number is reached/ user typed done. Print tree
