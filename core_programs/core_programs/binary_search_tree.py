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

    def print_tree(self): #show the tree
        self._print_tree(self.root, 0)

    def _print_tree(self, node, level):
        if node is not None:
            self._print_tree(node.right, level + 2)
            print("   " * level + str(node.number))
            self._print_tree(node.left, level + 2)

#definitions
def input_number():
    while True:
        user_input=input("Enter number(or type 'done'):")
        if user_input.lower()=="done": #programs prints tree when user types done
            print("You have typed 'Done'. Creating tree...")
            binary_search_tree.print_tree()
            break #stops loop
        try:
            inputted=int(user_input)
            binary_search_tree.insert(inputted)
            binary_search_tree.print_tree()
        except:
            print("Invalid input. You have entered a non-integer and did not type 'Done'") # If user did not type a number or did not type done, program continues to ask for input.
            binary_search_tree.print_tree()

# main program
inputted_number=0
max_input=31
binary_search_tree=BinarySearchTree()

if __name__ == "__main__":
    while inputted_number<max_input:# Enable user to input until maximum input is reached(31 inputs)(Use while?)
        if not input_number():
            break
        inputted_number+=1

        if inputted_number==max_input:
            print("You have reached the maximum amount of inputs. Creating tree.") # If number is reached/ user typed done. Print tree
            binary_search_tree.print_tree()