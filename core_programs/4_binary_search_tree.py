#Binary Search Tree
#Import shared module for organization
#Use core_programs_module to implement BST
import core_programs_module as cpm


#Binary Search Tree Main Logic File
if __name__ == "__main__":
    bst = None
    MAX_LEVEL = 5
    current_depth = MAX_LEVEL
    status = ""

    while True:
        try:
            cpm.render_tree_view("BST VIEW", bst, MAX_LEVEL, current_depth, status)
            status = ""
            print("\n==================== BST MENU ====================")
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
                bst = cpm.BinarySearchTree(max_depth=MAX_LEVEL)
                bst.build_full_tree(target_depth=level, low=0, high=1000)
                status = f"Built full BST to depth {level} (max depth = {MAX_LEVEL})."
                cpm.render_tree_view("BST VIEW", bst, MAX_LEVEL, current_depth, status)
                # Interactive sub-menu for operations after building
                while True:
                    print("\n-- Actions --")
                    print(" 1) Insert a value")
                    print(" 2) Delete a value")
                    print(" 3) Search for a value")
                    print(" 4) Back to main menu")
                    sub_choice = input("Select an option (1-4): ").strip()

                    if sub_choice == "4":
                        bst = None
                        status = ""
                        break

                    if sub_choice == "1":
                        try:
                            val = int(input("Value to insert: ").strip())
                            ok = bst.insert(val)
                            status = f"Inserted {val}." if ok else ("Insert blocked: duplicate value." if bst.search(val) else "Insert blocked: depth limit or no space.")
                            cpm.render_tree_view("BST VIEW", bst, MAX_LEVEL, current_depth, status)
                        except ValueError:
                            status = "Invalid number."
                            cpm.render_tree_view("BST VIEW", bst, MAX_LEVEL, current_depth, status)
                        continue

                    if sub_choice == "2":
                        try:
                            val = int(input("Value to delete: ").strip())
                            removed = bst.delete(val)
                            status = "Deleted." if removed else "Value not found; nothing deleted."
                            cpm.render_tree_view("BST VIEW", bst, MAX_LEVEL, current_depth, status)
                        except ValueError:
                            status = "Invalid number."
                            cpm.render_tree_view("BST VIEW", bst, MAX_LEVEL, current_depth, status)
                        continue

                    if sub_choice == "3":
                        try:
                            val = int(input("Value to search: ").strip())
                            found = bst.search(val)
                            status = "Found." if found else "Not found."
                            cpm.render_tree_view("BST VIEW", bst, MAX_LEVEL, current_depth, status)
                        except ValueError:
                            status = "Invalid number."
                            cpm.render_tree_view("BST VIEW", bst, MAX_LEVEL, current_depth, status)
                        continue

                    status = "Invalid choice. Enter a number 1-4."
                    cpm.render_tree_view("BST VIEW", bst, MAX_LEVEL, current_depth, status)
                continue

            status = "Invalid choice. Enter a number 1-2."
            cpm.render_tree_view("BST VIEW", bst, MAX_LEVEL, current_depth, status)
        except ValueError:
            status = "Invalid input. Please try again."
            cpm.render_tree_view("BST VIEW", bst, MAX_LEVEL, current_depth, status)
