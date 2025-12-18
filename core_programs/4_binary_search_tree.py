# Binary Search Tree
class BinarySearchTree: # Use class
    def __init__(self, number, left, right):
        self.number=number
        self.left=left
        self.right=right # Class attributes: top, left, right
        self.root=None
    
    # Functions needed
    def insert(self):
        if self.root==None: # First number as root
            self.root=self.number
            return self.root
        
            # Determine if number is bigger or smaller
                # smaller/equal = left
                # bigger = right
            # Traverse the tree until it reaches an empty node
            # Insert in binary tree
                
    #Use definition
        # input
def input_number():
    number_input=int(input("Enter number:"))
    BinarySearchTree.number=number_input
    #Ask user to input number (input)
    # main

input_number()
            # Enable user to input until maximum input is reached(31 inputs)(Use while?)
            # If number is reached/ typed done. Print tree