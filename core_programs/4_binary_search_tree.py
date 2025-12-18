# Binary Search Tree
# Use class
class Node:
    def __init__(self,number,left,right): # Class attributes: top, left, right
        self.number=number
        self.left=left
        self.right=right

class BinarySearchTree: 
    def __init__(self):
        self.root=None

    # Functions needed
    def insert(self, number):
        if self.root==None: # First number as root
            self.root=number
            return self.root
        
            # Determine if number is bigger or smaller
                # smaller/equal = left
                # bigger = right
            # Traverse the tree until it reaches an empty node
            # Insert in binary tree
                
    #Use definition
        # input
def input_number():
    number_input=input("Enter number:")
    binary_search_tree.number=number_input
    print(binary_search_tree.number)
    binary_search_tree.insert(number_input)
    print(binary_search_tree.root)
    #Ask user to input number (input)
    # main

binary_search_tree=BinarySearchTree()
input_number()
            # Enable user to input until maximum input is reached(31 inputs)(Use while?)
            # If number is reached/ typed done. Print tree