#Binary Tree Pseudocode
import core_programs_module as cpm

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
    tree = None
    MAX_LEVEL = 5
    current_depth = MAX_LEVEL
    status = ""

    while True:
        try:
            cpm.render_tree_view("BINARY TREE VIEW", tree, MAX_LEVEL, current_depth, status)
            status = ""
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
                tree = cpm.BinaryTree(max_depth=MAX_LEVEL)
                tree.build_full_tree(target_depth=level, low=0, high=1000)
                status = f"Built full tree to depth {level} (max depth = {MAX_LEVEL})."
                cpm.render_tree_view("BINARY TREE VIEW", tree, MAX_LEVEL, current_depth, status)
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
                        status = ""
                        break

                    if sub_choice == "1":
                        # Pre-Order traversal (root, left, right)
                        result = tree.preorder()
                        status = f"Pre-Order: {result}"
                        cpm.render_tree_view("BINARY TREE VIEW", tree, MAX_LEVEL, current_depth, status)
                        continue

                    if sub_choice == "2":
                        # In-Order traversal (left, root, right)
                        result = tree.inorder()
                        status = f"In-Order: {result}"
                        cpm.render_tree_view("BINARY TREE VIEW", tree, MAX_LEVEL, current_depth, status)
                        continue

                    if sub_choice == "3":
                        # Post-Order traversal (left, right, root)
                        result = tree.postorder()
                        status = f"Post-Order: {result}"
                        cpm.render_tree_view("BINARY TREE VIEW", tree, MAX_LEVEL, current_depth, status)
                        continue

                    status = "Invalid choice. Enter a number 1-4."
                    cpm.render_tree_view("BINARY TREE VIEW", tree, MAX_LEVEL, current_depth, status)
                continue

            status = "Invalid choice. Enter a number 1-2."
            cpm.render_tree_view("BINARY TREE VIEW", tree, MAX_LEVEL, current_depth, status)
        except ValueError:
            status = "Invalid input. Please try again."
            cpm.render_tree_view("BINARY TREE VIEW", tree, MAX_LEVEL, current_depth, status)