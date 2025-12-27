#Binary Tree Pseudocode
class Node:
    def __init__(self,number): # Class attributes: top, left, right
        self.number=number
        self.left=None
        self.right=None

class BinaryTree: 
    def __init__(self):
        self.root=None

    # Functions needed
    def insert(self, number): #Insert the input into tree (left to right per level)
        if self.root==None: # First number as root
            self.root=Node(number)
    
    def preorder(Self): #organizes each item in the tree in the order: Top, left, right
        pass

    def inorder(self): #organizes each item in the tree in the order: left, top right
        pass

    def postorder(Self): #organizes each item in the tree in the order: left, right, top
        pass

#Make user input numbers
#Let user input until maximum levels are reached (max of 5 levels, 32 inputs)
    #Ask user if they want to add another level after filling in each level. User can:
        # Add level
        # finish input
#Print Tree(optional), print the traversal for tree (preorder, inorder, postorder) when any of the two conditions are met