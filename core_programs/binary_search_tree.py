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
            self.insertion_branching(self.root,number)

    def insertion_branching(self,current,number):
        if number<=current.number: # smaller/equal = left
            if current.left is None:
                current.left=Node(number) # Insert in binary tree
            else:
                self.insertion_branching(current.left,number) # Traverse the tree until it reaches an empty node
        else: # bigger = right
            if current.right is None:
                current.right=Node(number)  # Insert in binary tree
            else:
                self.insertion_branching(current.right,number) # Traverse the tree until it reaches an empty node
    
    def delete(self, number):
        self.root=self.deletion_branching(self.root, number)
        input_number()
        
    def deletion_branching(self, node, number):
        if node is None: # line of code to avoid exception when no node value is found equal to inputted number
            print(f"You do not have a {number} in your binary search tree.")
            input_number()
            return node
        
        if number<node.left:# traverse tree to find inputted number, no delete (left=smaller/same)
            node.left=self.deletion_branching(node.left,number)
        elif number>node.right:# traverse tree to find inputted number, no delete (right=higher)
            node.right=self.deletion_branching(node.right,number)
        else: # Value to be deleted is found
            if node.left is None:   # If there no left child parents node is replaced by right child
                return node.right
            elif node.right is None:  # If there no right child parents node is replaced by left child
                return node.left
            elif node.left is None and node.right is None: #for deletion of leaf nodes
                return None  # the node is removed
        
            new_node = self._min_value_node(node.right) # For nodes with two child nodes
            node.number = new_node.number #Changes parent node with the right child node
            node.right = self._delete(node.right, new_node.number)
        
        return node

    def _min_value_node(self, node): 
        current = node
        while current.left is not None:
            current = current.left
        return current

    def print_tree(self): #show the tree
        self._print_tree(self.root, 0)

    def _print_tree(self, node, level):
        if node is not None:
            self._print_tree(node.right, level + 2)
            print("   " * level + str(node.number))
            self._print_tree(node.left, level + 2)

#definitions
def input_number():
    user_action=input("Binary Search Tree\nTo start type:\n 'I': Insert value\n'D':Delete value\n'F':Finish input\nYour choice:")
    while True:
        if user_action.lower()=="f": #programs prints tree when user types done
            print("You have typed 'Done'. Creating tree...")
            binary_search_tree.print_tree()
            break #stops loop
        elif user_action.lower()=="i":
            user_input=input("Enter number to insert:")
            inputted=int(user_input)
            binary_search_tree.insert(inputted)
            binary_search_tree.print_tree()
        elif user_action.lower()=="d":
            user_input=input("Enter number to remove:")
            inputted=int(user_input)
            binary_search_tree.delete(inputted)
            binary_search_tree.print_tree()
            
        else:
            print("Invalid input. You have entered any of the possible actions.") # If user did not type a number or did not type done, program continues to ask for input.
            input_number()

# main program
inputted_number=0
max_input=31
binary_search_tree=BinarySearchTree()
user_action=input("Binary Search Tree\nTo start type:\n 'I': Insert value\n'D':Delete value\n'F':Finish input\nYour choice:")
while inputted_number<max_input:# Enable user to input until maximum input is reached(31 inputs)(Use while?)
    if not input_number():
        break
    if user_action.lower()=="i":
        inputted_number+=1
    elif user_action.lower()=="d":
        inputted_number-=1

if inputted_number==max_input:
    print("You have reached the maximum amount of inputs. Creating tree.") # If number is reached/ user typed done. Print tree
    binary_search_tree.print_tree()