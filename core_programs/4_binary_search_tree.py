#Binary Search Tree
#Import shared module for organization
#Use core_programs_module to implement BST
import core_programs_module

#Render tree lines
def pretty_print_diagonal(root, max_depth: int) -> None:
    """Render a top-down view of the BST using diagonal connectors."""
    if root is None:
        print("<empty tree>")
        return

    def _height(node) -> int:
        return 0 if node is None else 1 + max(_height(node.left), _height(node.right))

    height = max(max_depth, _height(root))
    width = max(2 ** (height + 2), 16)
    rows = [list(" " * width) for _ in range(height * 2 - 1)]

    def place(node, depth: int, x: int, gap: int) -> None:
        node_row = depth * 2
        val = str(node.value)
        start = max(x - len(val) // 2, 0)
        end = min(start + len(val), width)
        rows[node_row][start:end] = val[: end - start]

        if depth == height - 1:
            return

        connector_row = node_row + 1
        child_gap = max(gap // 2, 1)

        if node.left:
            child_x = x - child_gap
            for i in range(1, child_gap + 1):
                pos = x - i
                if 0 <= pos < width:
                    rows[connector_row][pos] = "/"
            place(node.left, depth + 1, child_x, child_gap)

        if node.right:
            child_x = x + child_gap
            for i in range(1, child_gap + 1):
                pos = x + i
                if 0 <= pos < width:
                    rows[connector_row][pos] = "\\"
            place(node.right, depth + 1, child_x, child_gap)

    place(root, 0, width // 2, width // 2)
    for line in rows:
        print("".join(line).rstrip())


#Binary Search Tree Main Logic File
if __name__ == "__main__":

    def clear_console() -> None:
        core_programs_module.clear_console()

    bst = None
    MAX_LEVEL = 5
    current_depth = MAX_LEVEL

    def render_tree(status: str = "") -> None:
        clear_console()
        print("==================== BST VIEW ====================")
        print(f"Max depth: {MAX_LEVEL} | Current depth: {current_depth}")
        if status:
            print(f"Status: {status}")
        else:
            print("Status: (none)")
        print("--------------------------------------------------")
        if bst is None or bst.root is None:
            print("<no tree built>")
        else:
            pretty_print_diagonal(bst.root, MAX_LEVEL)
        print("==================================================")

    def ensure_tree() -> None:
        # Use module-level variables for current tree state
        global bst, current_depth
        if bst is None:
            bst = core_programs_module.BinarySearchTree(max_depth=MAX_LEVEL)
            bst.build_full_tree(target_depth=current_depth, low=0, high=1000)
            render_tree(f"Initialized tree at depth {current_depth}.")

    while True:
        try:
            render_tree()
            print("\n==================== BST MENU ====================")
            print(" 1) Build full tree (depth 1-5)")
            print(" 2) Insert a value")
            print(" 3) Delete a value")
            print(" 4) Search for a value")
            print(" 5) Quit")
            print("================================================")
            choice = input("Select an option (1-5): ").strip()

            if choice == "5":
                break

            if choice == "1":
                level_raw = input("Select tree depth (1-5): ").strip()
                level = int(level_raw)
                if level < 1 or level > MAX_LEVEL:
                    print(f"Please enter a number between 1 and {MAX_LEVEL}.")
                    continue
                current_depth = level
                bst = core_programs_module.BinarySearchTree(max_depth=MAX_LEVEL)
                bst.build_full_tree(target_depth=level, low=0, high=1000)
                render_tree(f"Built full BST to depth {level} (max depth = {MAX_LEVEL}).")
                # Interactive sub-menu for operations after building
                while True:
                    print("\n-- Actions --")
                    print(" 1) Insert a value")
                    print(" 2) Delete a value")
                    print(" 3) Search for a value")
                    print(" 4) Back to main menu")
                    sub_choice = input("Select an option (1-4): ").strip()

                    if sub_choice == "4":
                        break

                    if sub_choice == "1":
                        try:
                            val = int(input("Value to insert: ").strip())
                            ok = bst.insert(val)
                            status = f"Inserted {val}." if ok else ("Insert blocked: duplicate value." if bst.search(val) else "Insert blocked: depth limit or no space.")
                            render_tree(status)
                        except ValueError:
                            render_tree("Invalid number.")
                        continue

                    if sub_choice == "2":
                        try:
                            val = int(input("Value to delete: ").strip())
                            removed = bst.delete(val)
                            render_tree("Deleted." if removed else "Value not found; nothing deleted.")
                        except ValueError:
                            render_tree("Invalid number.")
                        continue

                    if sub_choice == "3":
                        try:
                            val = int(input("Value to search: ").strip())
                            found = bst.search(val)
                            render_tree("Found." if found else "Not found.")
                        except ValueError:
                            render_tree("Invalid number.")
                        continue

                    render_tree("Invalid choice. Enter a number 1-4.")
                continue

            if choice == "2":
                ensure_tree()
                val = int(input("Value to insert: ").strip())
                ok = bst.insert(val)
                status = f"Inserted {val}." if ok else ("Insert blocked: duplicate value." if bst.search(val) else "Insert blocked: depth limit or no space.")
                render_tree(status)
                continue

            if choice == "3":
                ensure_tree()
                val = int(input("Value to delete: ").strip())
                removed = bst.delete(val)
                render_tree("Deleted." if removed else "Value not found; nothing deleted.")
                continue

            if choice == "4":
                ensure_tree()
                val = int(input("Value to search: ").strip())
                found = bst.search(val)
                render_tree("Found." if found else "Not found.")
                continue

            print("Invalid choice. Enter a number 1-5.")
            render_tree("Invalid choice. Enter a number 1-5.")
        except ValueError:
            render_tree("Invalid input. Please try again.")
