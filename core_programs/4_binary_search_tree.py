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
        else: # Determine if number is bigger or smaller
            if number>self.number: # smaller/equal = left
                if self.left is None:
                    self.left=Node(number) # Traverse the tree until it reaches an empty node
                else:
                    self.left.insert(number)  # Insert in binary tree
            else: # bigger = right
                if self.right is None:
                    self.right=Node(number) # Traverse the tree until it reaches an empty node
                else:
                    self.right.insert(number) # Insert in binary tree
                
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

inputted_number=0
binary_search_tree=BinarySearchTree()
while inputted_number!=100:
    input_number()
    binary_search_tree.insert()
    inputted_number+=1
            # Enable user to input until maximum input is reached(31 inputs)(Use while?)
            # If number is reached/ typed done. Print tree