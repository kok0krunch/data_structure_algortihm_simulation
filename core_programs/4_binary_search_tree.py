# Binary Search Tree
# Use class
class Node:
    def __init__(self,number,left,right): # Class attributes: top, left, right
        self.number=None
        self.left=None
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

# main
inputted_number=0
binary_search_tree=BinarySearchTree()
while inputted_number!=100:
    try: # Enable user to input until maximum input is reached(31 inputs)(Use while?)
        binary_search_tree.insert(int(input("Enter number:")))
# If number is reached/ user typed done. Print tree
    except:
        print("You have typed done, creating your tree.")
        break
