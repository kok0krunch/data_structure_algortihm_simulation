#Binary Tree Pseudocode
import core_programs_module
from core_programs_module import Node
# Node class imported from core_programs_module
# Class attributes: value, left, right

class BinaryTree: 
    def __init__(self):
        self.root=None

    # Functions needed
    def insert(self, number): #Insert the input into tree (left to right per level)
        if self.root==None: # First number as root
            self.root=Node(number)  # Using Node from core_programs_module
    
    def preorder(self): #organizes each item in the tree in the order: Top, left, right
        result = []
        def traverse(node):
            if node:
                result.append(node.value)
                traverse(node.left)
                traverse(node.right)
        traverse(self.root)
        return result

    def inorder(self): #organizes each item in the tree in the order: left, top right
        result = []
        def traverse(node):
            if node:
                traverse(node.left)
                result.append(node.value)
                traverse(node.right)
        traverse(self.root)
        return result

    def postorder(self): #organizes each item in the tree in the order: left, right, top
        result = []
        def traverse(node):
            if node:
                traverse(node.left)
                traverse(node.right)
                result.append(node.value)
        traverse(self.root)
        return result

#Main Code
#Ask user if they want to add another level after filling in each level. User can:
    # Add level
    # finish input
#Print Tree(optional), print the traversal for tree (preorder, inorder, postorder) when any of the two conditions are met


#Binary Tree Implementation
#Import shared module for organization
#Use core_programs_module to implement Binary Tree


#Binary Tree Main Logic File
if __name__ == "__main__":

    def clear_console() -> None:
        core_programs_module.clear_console()

    tree = None
    MAX_LEVEL = 5
    current_depth = MAX_LEVEL

    def render_tree(status: str = "") -> None:
        clear_console()
        print("================= BINARY TREE VIEW ===============")
        print(f"Max depth: {MAX_LEVEL} | Current depth: {current_depth}")
        if status:
            print(f"Status: {status}")
        else:
            print("Status: (none)")
        print("--------------------------------------------------")
        if tree is None or tree.root is None:
            print("<no tree built>")
        else:
            core_programs_module.pretty_print_diagonal(tree.root, MAX_LEVEL)
        print("==================================================")

    while True:
        try:
            render_tree()
            print("\n============== BINARY TREE MENU ================")
            print(" 1) Build full tree (depth 1-5)")
            print(" 2) Quit")
            print("================================================")
            choice = input("Select an option (1-2): ").strip()

            if choice == "2":
                break

            if choice == "1":
                level_raw = input("Select tree depth (1-5): ").strip()
                level = int(level_raw)
                if level < 1 or level > MAX_LEVEL:
                    print(f"Please enter a number between 1 and {MAX_LEVEL}.")
                    continue
                current_depth = level
                tree = core_programs_module.BinarySearchTree(max_depth=MAX_LEVEL)
                tree.build_full_tree(target_depth=level, low=0, high=1000)
                render_tree(f"Built full tree to depth {level} (max depth = {MAX_LEVEL}).")
                # Interactive sub-menu for traversal operations
                while True:
                    print("\n-- Traversal Options --")
                    print(" 1) Pre-Order")
                    print(" 2) In-Order")
                    print(" 3) Post-Order")
                    print(" 4) Back to main menu")
                    sub_choice = input("Select an option (1-4): ").strip()

                    if sub_choice == "4":
                        tree = None
                        break

                    if sub_choice == "1":
                        # Pre-Order traversal (root, left, right)
                        def preorder(node):
                            if node is None:
                                return []
                            return [node.value] + preorder(node.left) + preorder(node.right)
                        
                        result = preorder(tree.root)
                        render_tree(f"Pre-Order: {result}")
                        continue

                    if sub_choice == "2":
                        # In-Order traversal (left, root, right)
                        def inorder(node):
                            if node is None:
                                return []
                            return inorder(node.left) + [node.value] + inorder(node.right)
                        
                        result = inorder(tree.root)
                        render_tree(f"In-Order: {result}")
                        continue

                    if sub_choice == "3":
                        # Post-Order traversal (left, right, root)
                        def postorder(node):
                            if node is None:
                                return []
                            return postorder(node.left) + postorder(node.right) + [node.value]
                        
                        result = postorder(tree.root)
                        render_tree(f"Post-Order: {result}")
                        continue

                    render_tree("Invalid choice. Enter a number 1-4.")
                continue

            print("Invalid choice. Enter a number 1-2.")
            render_tree("Invalid choice. Enter a number 1-2.")
        except ValueError:
            render_tree("Invalid input. Please try again.")