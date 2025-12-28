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

#Main Code
#Definitions
def input_number(): #Make user input numbers
    try:
        user_input=input("Enter number (or type 'exit' to quit):")
        if user_input.lower()=="exit":
            return "exit"
        elif user_input=="":
            binary_tree.insert("-")
        else:
            binary_tree.insert(user_input)
        return "continue"
    except:
        return "continue"

#Main Porgram
inputted_number=0
binary_tree=BinaryTree()
while inputted_number!=31:# #Let user input until maximum levels are reached (max of 5 levels, 31 inputs)
    result = input_number()
    if result == "exit":
        break
    inputted_number+=1

    #Ask user if they want to add another level after filling in each level. User can:
        # Add level
        # finish input
#Print Tree(optional), print the traversal for tree (preorder, inorder, postorder) when any of the two conditions are met