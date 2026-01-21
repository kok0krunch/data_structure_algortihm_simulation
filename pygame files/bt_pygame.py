import pygame
import random
import math
from typing import Optional, List

# Node class for binary tree
class Node:
    """Represents a single node in the binary tree."""
    def __init__(self, value: int) -> None:
        self.value = value
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None

    def __repr__(self) -> str:
        return f"Node({self.value})"

# Binary Tree class
class BinaryTree:
    """Basic binary tree with traversals and level-order builders."""
    def __init__(self, max_depth: int = 4) -> None:
        self.root: Optional[Node] = None
        self.max_depth = max_depth

    def insert(self, value: int) -> None:
        """Insert by filling the first available slot in level order."""
        new_node = Node(value)
        if self.root is None:
            self.root = new_node
            return

        queue: List[Node] = [self.root]
        while queue:
            current = queue.pop(0)
            if current.left is None:
                current.left = new_node
                return
            queue.append(current.left)
            if current.right is None:
                current.right = new_node
                return
            queue.append(current.right)

    def build_full_tree(self, target_depth: int, low: int = 10, high: int = 99) -> None:
        """Build a complete binary tree up to target_depth with random values."""
        if target_depth < 1 or target_depth > self.max_depth:
            raise ValueError(f"target_depth must be between 1 and {self.max_depth}")

        needed = 2 ** target_depth - 1
        available = high - low + 1
        if available < needed:
            # Use repeating values if range is too small
            values = [random.randint(low, high) for _ in range(needed)]
        else:
            values = random.sample(range(low, high + 1), needed)
        
        nodes = [Node(v) for v in values]
        for idx, node in enumerate(nodes):
            left_idx = 2 * idx + 1
            right_idx = 2 * idx + 2
            if left_idx < len(nodes):
                node.left = nodes[left_idx]
            if right_idx < len(nodes):
                node.right = nodes[right_idx]
        self.root = nodes[0] if nodes else None

    def build_incomplete_tree(self, target_depth: int, low: int = 10, high: int = 99) -> None:
        """Build an incomplete binary tree up to target_depth with random values.
        An incomplete tree is filled level by level, but the last level may not be completely filled."""
        if target_depth < 1 or target_depth > self.max_depth:
            raise ValueError(f"target_depth must be between 1 and {self.max_depth}")

        # For incomplete trees, we'll generate a random number of nodes
        # that's between a complete tree and a full tree
        max_nodes = 2 ** target_depth - 1
        min_nodes = 2 ** (target_depth - 1)  # At least fill up to previous level
        
        # Generate random number of nodes for incomplete tree
        num_nodes = random.randint(min_nodes, max_nodes)
        
        available = high - low + 1
        if available < num_nodes:
            values = [random.randint(low, high) for _ in range(num_nodes)]
        else:
            values = random.sample(range(low, high + 1), num_nodes)
        
        # Build tree by inserting values in level-order (breadth-first)
        self.root = None
        for value in values:
            self.insert(value)

    def preorder(self) -> List[int]:
        result: List[int] = []
        nodes: List[Node] = []  # Store node objects for animation
        
        def traverse(node: Optional[Node]) -> None:
            if node is None:
                return
            result.append(node.value)
            nodes.append(node)
            traverse(node.left)
            traverse(node.right)
        
        traverse(self.root)
        return result, nodes

    def inorder(self) -> List[int]:
        result: List[int] = []
        nodes: List[Node] = []
        
        def traverse(node: Optional[Node]) -> None:
            if node is None:
                return
            traverse(node.left)
            result.append(node.value)
            nodes.append(node)
            traverse(node.right)
        
        traverse(self.root)
        return result, nodes

    def postorder(self) -> List[int]:
        result: List[int] = []
        nodes: List[Node] = []
        
        def traverse(node: Optional[Node]) -> None:
            if node is None:
                return
            traverse(node.left)
            traverse(node.right)
            result.append(node.value)
            nodes.append(node)
        
        traverse(self.root)
        return result, nodes

class BinaryTreeVisualizer:
    def __init__(self, screen_width=1366, screen_height=768):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.tree = BinaryTree()
        self.current_depth = 1
        self.max_depth = 5
        self.input_value = ""
        self.message = ""
        self.message_timer = 0
        self.traversal_result = ""
        self.traversal_type = ""
        self.manual_mode = False  # Flag for manual input mode
        self.manual_input_buffer = ""  # Buffer for manual node input (bulk mode)
        self.manual_selected_parent: Optional[Node] = None  # Currently selected parent node
        self.manual_insert_side: str = "left"  # Side to insert ('left' or 'right')
        self.manual_value_buffer: str = ""  # Single value buffer for interactive insert
        
        # Animation state for traversal highlighting
        self.animation_active = False
        self.animation_nodes = []  # List of nodes in traversal order
        self.current_highlight_index = 0
        self.animation_timer = 0
        self.highlight_duration = 60  # Frames to highlight each node
        
        # Load images
        try:
            self.node_img = pygame.image.load("images/bst_images/bst_node.png").convert_alpha()
            self.node_img = pygame.transform.scale(self.node_img, (90, 90))
        except:
            self.node_img = None
            
        # Colors
        self.node_color = (100, 150, 255)
        self.text_color = (255, 255, 255)
        self.line_color = (80, 80, 80)
        self.bg_color = (245, 245, 245)
        
        # Fonts
        self.font = pygame.font.SysFont("Courier New", 16, bold=True)
        self.small_font = pygame.font.SysFont("Courier New", 12)
        self.large_font = pygame.font.SysFont("Courier New", 20, bold=True)
        self.title_font = pygame.font.SysFont("Courier New", 22, bold=True)

    def draw_node(self, screen, x, y, value, highlighted=False, radius=35):
        """Draw a single node at the given position with dynamic radius"""
        # Ensure all coordinates are integers for pixel-perfect rendering
        radius = int(radius)
        x = int(x)
        y = int(y)
        
        if self.node_img:
            # Use the BST node image with proper scaling
            # Image is a circle, so scale it to be a perfect circle with diameter = 2 * radius
            img_size = int(radius * 2)
            scaled_img = pygame.transform.scale(self.node_img, (img_size, img_size))
            
            # Draw highlight if needed
            if highlighted:
                # Pulsing highlight effect
                pulse = int(abs(math.sin(pygame.time.get_ticks() * 0.005)) * 3) + 1
                highlight_size = img_size + pulse * 2
                highlight_surf = pygame.Surface((highlight_size, highlight_size), pygame.SRCALPHA)
                pygame.draw.circle(highlight_surf, (255, 255, 0, 150), (highlight_size//2, highlight_size//2), highlight_size//2)
                screen.blit(highlight_surf, (x - highlight_size//2, y - highlight_size//2))
            
            # Blit the scaled image centered at (x, y)
            node_rect = scaled_img.get_rect(center=(x, y))
            screen.blit(scaled_img, node_rect)
        else:
            # Fallback to perfect circles if image not available
            if highlighted:
                pulse = int(abs(math.sin(pygame.time.get_ticks() * 0.005)) * 8) + 2
                pygame.draw.circle(screen, (255, 255, 0), (x, y), radius + pulse)
            
            color = (100, 255, 100) if highlighted else self.node_color
            pygame.draw.circle(screen, color, (x, y), radius)
            pygame.draw.circle(screen, (0, 0, 0), (x, y), radius, 3)
        
        # Draw value text centered inside the node (offset slightly to the left)
        font_size = max(10, int(radius * 0.45))
        dynamic_font = pygame.font.SysFont("Courier New", font_size, bold=True)
        text_color = (255, 0, 0) if highlighted else (0, 0, 0)
        text_surface = dynamic_font.render(str(value), True, text_color)
        
        # Center text with slight left offset
        text_x = x - text_surface.get_width() // 2 - 5
        text_y = y - text_surface.get_height() // 2
        screen.blit(text_surface, (text_x, text_y))

    def draw_line(self, screen, start_pos, end_pos):
        """Draw a line between two nodes"""
        pygame.draw.line(screen, self.line_color, start_pos, end_pos, 3)

    def calculate_positions(self, depth):
        """Calculate node positions for the tree based on depth"""
        positions = {}
        if depth == 0 or not self.tree.root:
            return positions
        
        # Tree drawing area - adjusted for larger trees
        tree_area_x = 0
        tree_area_y = 120
        tree_area_width = self.screen_width - 350
        tree_area_height = 500
        
        # Calculate minimum spacing needed for nodes (considering node size + padding)
        # Node diameter is 70 (radius 35), add extra padding for clarity
        min_node_spacing = 85  # Increased from 65 to prevent overlap
        
        # Calculate positions using a different approach for better spacing
        def get_tree_width(level):
            """Get the required width for a given level"""
            nodes_at_level = 2 ** level
            return nodes_at_level * min_node_spacing
        
        # Find the widest level
        max_width_level = depth - 1
        max_width = get_tree_width(max_width_level)
        
        # Scale down if tree is too wide
        scale_factor = min(1.0, tree_area_width / max_width) if max_width > 0 else 1.0
        
        # Adjust node radius based on depth to prevent overlap at deeper levels
        adjusted_node_radius = max(20, 35 - (depth - 3) * 3) if depth > 3 else 35
        
        def position_nodes_recursive(node, level, position_in_level, positions_at_level):
            if node is None or level >= depth:
                return
            
            if level not in positions:
                positions[level] = {}
            
            # Calculate vertical position with better spacing
            level_spacing = max(90, tree_area_height // max(depth, 1))  # Minimum vertical spacing
            y = tree_area_y + level * level_spacing + 30  # Add offset
            
            # Calculate horizontal position using tree structure
            if level == 0:
                # Root node centered
                x = tree_area_x + tree_area_width // 2
            else:
                # Calculate position based on parent and sibling structure
                nodes_at_this_level = 2 ** level
                level_width = nodes_at_this_level * min_node_spacing * scale_factor
                spacing_between_nodes = level_width / (nodes_at_this_level + 1)
                
                x = tree_area_x + (tree_area_width - level_width) // 2 + spacing_between_nodes * (position_in_level + 1)
            
            positions[level][node] = (int(x), int(y))
            
            # Position children
            if node.left:
                position_nodes_recursive(node.left, level + 1, position_in_level * 2, 2 ** (level + 1))
            if node.right:
                position_nodes_recursive(node.right, level + 1, position_in_level * 2 + 1, 2 ** (level + 1))
        
        position_nodes_recursive(self.tree.root, 0, 0, 1)
        return positions

    def draw_tree(self, screen):
        """Draw the entire binary tree"""
        # Draw tree background panel first
        tree_panel_x = 30
        tree_panel_y = 100
        tree_panel_width = self.screen_width - 410
        tree_panel_height = 520
        
        # White background with black border
        pygame.draw.rect(screen, (255, 255, 255), (tree_panel_x, tree_panel_y, tree_panel_width, tree_panel_height))
        pygame.draw.rect(screen, (0, 0, 0), (tree_panel_x, tree_panel_y, tree_panel_width, tree_panel_height), 3)
        
        if not self.tree.root:
            # Draw "No tree" message in the center of the panel
            no_tree_font = pygame.font.SysFont("Courier New", 20, bold=True)
            no_tree_text = no_tree_font.render("No tree built yet", True, (150, 150, 150))
            text_x = tree_panel_x + (tree_panel_width - no_tree_text.get_width()) // 2
            text_y = tree_panel_y + (tree_panel_height - no_tree_text.get_height()) // 2
            screen.blit(no_tree_text, (text_x, text_y))
            return
        
        positions = self.calculate_positions(self.current_depth)
        
        # Calculate node radius based on depth - ensure it's an integer for perfect circles
        node_radius = int(max(20, 35 - (self.current_depth - 3) * 3)) if self.current_depth > 3 else 35
        
        # Draw connections first
        def draw_connections(node, level):
            if node is None or level not in positions or node not in positions[level]:
                return
            
            node_pos = positions[level][node]
            
            # Draw lines to children
            if level + 1 in positions:
                if node.left and node.left in positions[level + 1]:
                    child_pos = positions[level + 1][node.left]
                    self.draw_line(screen, node_pos, child_pos)
                
                if node.right and node.right in positions[level + 1]:
                    child_pos = positions[level + 1][node.right]
                    self.draw_line(screen, node_pos, child_pos)
            
            # Recursively draw connections for children
            if node.left:
                draw_connections(node.left, level + 1)
            if node.right:
                draw_connections(node.right, level + 1)
        
        draw_connections(self.tree.root, 0)
        
        # Draw nodes on top of connections
        def draw_nodes(node, level):
            if node is None or level not in positions or node not in positions[level]:
                return
            
            node_pos = positions[level][node]
            # Only draw if node is within visible bounds
            if (35 <= node_pos[0] <= self.screen_width - 380 and 
                80 <= node_pos[1] <= self.screen_height - 50):
                
                # Check if this node should be highlighted
                # Hide manual selection highlighting when traversal is active
                highlighted = (
                    (self.animation_active and 
                     self.current_highlight_index < len(self.animation_nodes) and
                     node == self.animation_nodes[self.current_highlight_index])
                    or (self.manual_mode and self.manual_selected_parent is node and not self.animation_active)
                )
                
                self.draw_node(screen, node_pos[0], node_pos[1], node.value, highlighted, node_radius)
            
            # Recursively draw children
            if node.left:
                draw_nodes(node.left, level + 1)
            if node.right:
                draw_nodes(node.right, level + 1)
        
        draw_nodes(self.tree.root, 0)
    
    def update_animation(self):
        """Update traversal animation"""
        if not self.animation_active or not self.animation_nodes:
            return
            
        self.animation_timer += 1
        
        if self.animation_timer >= self.highlight_duration:
            self.current_highlight_index += 1
            self.animation_timer = 0
            
            if self.current_highlight_index >= len(self.animation_nodes):
                # Animation complete
                self.animation_active = False
                self.current_highlight_index = 0
                self.animation_nodes = []

    def draw_controls(self, screen):
        """Draw control panel"""
        panel_x = self.screen_width - 370
        panel_y = 100
        panel_width = 360
        panel_height = 520
        
        # Panel background
        pygame.draw.rect(screen, self.bg_color, (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(screen, (100, 100, 100), (panel_x, panel_y, panel_width, panel_height), 3)
        
        # Title
        title = self.title_font.render("BINARY TREE CONTROLS", True, (50, 50, 50))
        screen.blit(title, (panel_x + 20, panel_y + 10))
        
        y_offset = 50
        
        # Depth selector with Manual toggle on same line
        depth_label = self.font.render(f"Tree Depth: {self.current_depth}", True, (50, 50, 50))
        screen.blit(depth_label, (panel_x + 20, panel_y + y_offset))
        
        # Manual mode toggle (right side of depth text)
        manual_toggle_rect = pygame.Rect(panel_x + 200, panel_y + y_offset - 2, 90, 28)
        pygame.draw.rect(screen, (120, 160, 220) if self.manual_mode else (180, 180, 180), manual_toggle_rect)
        pygame.draw.rect(screen, (80, 120, 180), manual_toggle_rect, 2)
        toggle_text = self.small_font.render("Manual" if self.manual_mode else "Manual", True, (255, 255, 255))
        screen.blit(toggle_text, (manual_toggle_rect.centerx - toggle_text.get_width() // 2,
                                  manual_toggle_rect.centery - toggle_text.get_height() // 2))
        
        y_offset += 30
        
        # Manual input controls section (only show when manual mode is active)
        # Initialize all manual control rects
        manual_input_rect = None
        left_rect = None
        right_rect = None
        manual_insert_rect = None
        set_root_rect = None
        clear_sel_rect = None
        
        if self.manual_mode:
            # Manual input section - aligned to the right
            manual_start_y = panel_y + y_offset
            manual_right_x = panel_x + 155  # Align to right side below manual button
            
            # Input label and box (compact, on same line)
            input_label = self.small_font.render("Val:", True, (50, 50, 50))
            screen.blit(input_label, (manual_right_x, manual_start_y))
            
            manual_input_rect = pygame.Rect(manual_right_x + 35, manual_start_y - 2, 145, 24)
            pygame.draw.rect(screen, (255, 255, 255), manual_input_rect)
            pygame.draw.rect(screen, (100, 100, 100), manual_input_rect, 2)
            input_text = self.small_font.render(self.manual_value_buffer, True, (0, 0, 0))
            screen.blit(input_text, (manual_input_rect.x + 6, manual_input_rect.y + 4))
            
            # Parent selection info
            parent_val = self.manual_selected_parent.value if self.manual_selected_parent else "None"
            parent_text = self.small_font.render(f"Parent: {parent_val}", True, (50, 50, 50))
            screen.blit(parent_text, (manual_right_x, manual_start_y + 28))
            
            # Side selection buttons (Left/Right)
            side_y = manual_start_y + 52
            left_rect = pygame.Rect(manual_right_x, side_y, 55, 26)
            right_rect = pygame.Rect(manual_right_x + 60, side_y, 55, 26)
            
            pygame.draw.rect(screen, (100, 200, 100) if self.manual_insert_side == "left" else (180, 180, 180), left_rect)
            pygame.draw.rect(screen, (50, 150, 50), left_rect, 2)
            left_text = self.small_font.render("Left", True, (255, 255, 255))
            screen.blit(left_text, (left_rect.centerx - left_text.get_width() // 2,
                                    left_rect.centery - left_text.get_height() // 2))
            
            pygame.draw.rect(screen, (100, 200, 100) if self.manual_insert_side == "right" else (180, 180, 180), right_rect)
            pygame.draw.rect(screen, (50, 150, 50), right_rect, 2)
            right_text = self.small_font.render("Right", True, (255, 255, 255))
            screen.blit(right_text, (right_rect.centerx - right_text.get_width() // 2,
                                     right_rect.centery - right_text.get_height() // 2))
            
            # Insert button
            manual_insert_rect = pygame.Rect(manual_right_x + 120, side_y, 65, 26)
            pygame.draw.rect(screen, (150, 100, 200), manual_insert_rect)
            pygame.draw.rect(screen, (100, 50, 150), manual_insert_rect, 2)
            ins_text = self.small_font.render("Insert", True, (255, 255, 255))
            screen.blit(ins_text, (manual_insert_rect.centerx - ins_text.get_width() // 2,
                                   manual_insert_rect.centery - ins_text.get_height() // 2))
            
            # Set Root / Clear Selection buttons
            action_y = side_y + 32
            if self.tree.root is None:
                set_root_rect = pygame.Rect(manual_right_x, action_y, 85, 24)
                pygame.draw.rect(screen, (100, 200, 100), set_root_rect)
                pygame.draw.rect(screen, (50, 150, 50), set_root_rect, 2)
                root_text = self.small_font.render("Set Root", True, (255, 255, 255))
                screen.blit(root_text, (set_root_rect.centerx - root_text.get_width() // 2,
                                        set_root_rect.centery - root_text.get_height() // 2))
            else:
                clear_sel_rect = pygame.Rect(manual_right_x, action_y, 110, 24)
                pygame.draw.rect(screen, (200, 150, 120), clear_sel_rect)
                pygame.draw.rect(screen, (150, 100, 80), clear_sel_rect, 2)
                clr_text = self.small_font.render("Clear Sel.", True, (255, 255, 255))
                screen.blit(clr_text, (clear_sel_rect.centerx - clr_text.get_width() // 2,
                                       clear_sel_rect.centery - clr_text.get_height() // 2))
        
        # Build buttons section (fixed position - not affected by manual mode)
        button_width = 110
        button_height = 30
        button_spacing = 12
        
        # Build Complete Tree button
        complete_rect = pygame.Rect(panel_x + 20, panel_y + y_offset, 105, button_height)
        pygame.draw.rect(screen, (100, 200, 100), complete_rect)
        pygame.draw.rect(screen, (50, 150, 50), complete_rect, 2)
        complete_text = self.small_font.render("Complete", True, (255, 255, 255))
        screen.blit(complete_text, (complete_rect.centerx - complete_text.get_width() // 2,
                                complete_rect.centery - complete_text.get_height() // 2))
        y_offset += button_height + button_spacing
        
        # Build Incomplete Tree button
        incomplete_build_rect = pygame.Rect(panel_x + 20, panel_y + y_offset, 105, button_height)
        pygame.draw.rect(screen, (180, 140, 100), incomplete_build_rect)
        pygame.draw.rect(screen, (130, 90, 50), incomplete_build_rect, 2)
        incomplete_build_text = self.small_font.render("Incomplete", True, (255, 255, 255))
        screen.blit(incomplete_build_text, (incomplete_build_rect.centerx - incomplete_build_text.get_width() // 2,
                                incomplete_build_rect.centery - incomplete_build_text.get_height() // 2))
        y_offset += button_height + button_spacing
        
        # Depth adjustment buttons
        depth_up_rect = pygame.Rect(panel_x + 20, panel_y + y_offset, 55, 28)
        depth_down_rect = pygame.Rect(panel_x + 85, panel_y + y_offset, 55, 28)
        
        pygame.draw.rect(screen, (150, 150, 200), depth_up_rect)
        pygame.draw.rect(screen, (100, 100, 150), depth_up_rect, 2)
        up_text = self.small_font.render("Depth+", True, (255, 255, 255))
        screen.blit(up_text, (depth_up_rect.centerx - up_text.get_width() // 2,
                             depth_up_rect.centery - up_text.get_height() // 2))
        
        pygame.draw.rect(screen, (200, 150, 150), depth_down_rect)
        pygame.draw.rect(screen, (150, 100, 100), depth_down_rect, 2)
        down_text = self.small_font.render("Depth-", True, (255, 255, 255))
        screen.blit(down_text, (depth_down_rect.centerx - down_text.get_width() // 2,
                               depth_down_rect.centery - down_text.get_height() // 2))
        
        y_offset += 45
        
        # Clear button
        clear_rect = pygame.Rect(panel_x + 20, panel_y + y_offset, button_width, button_height)
        pygame.draw.rect(screen, (200, 100, 100), clear_rect)
        pygame.draw.rect(screen, (150, 50, 50), clear_rect, 2)
        clear_text = self.font.render("Clear Tree", True, (255, 255, 255))
        screen.blit(clear_text, (clear_rect.centerx - clear_text.get_width() // 2,
                                clear_rect.centery - clear_text.get_height() // 2))
        y_offset += button_height + 20
        
        # Traversal buttons
        traversal_label = self.font.render("Traversals:", True, (50, 50, 50))
        screen.blit(traversal_label, (panel_x + 20, panel_y + y_offset))
        y_offset += 30
        
        preorder_rect = pygame.Rect(panel_x + 20, panel_y + y_offset, button_width, button_height)
        pygame.draw.rect(screen, (150, 100, 200), preorder_rect)
        pygame.draw.rect(screen, (100, 50, 150), preorder_rect, 2)
        pre_text = self.font.render("Pre-Order", True, (255, 255, 255))
        screen.blit(pre_text, (preorder_rect.centerx - pre_text.get_width() // 2,
                              preorder_rect.centery - pre_text.get_height() // 2))
        y_offset += button_height + 10
        
        inorder_rect = pygame.Rect(panel_x + 20, panel_y + y_offset, button_width, button_height)
        pygame.draw.rect(screen, (200, 150, 100), inorder_rect)
        pygame.draw.rect(screen, (150, 100, 50), inorder_rect, 2)
        in_text = self.font.render("In-Order", True, (255, 255, 255))
        screen.blit(in_text, (inorder_rect.centerx - in_text.get_width() // 2,
                             inorder_rect.centery - in_text.get_height() // 2))
        y_offset += button_height + 10
        
        postorder_rect = pygame.Rect(panel_x + 20, panel_y + y_offset, button_width, button_height)
        pygame.draw.rect(screen, (100, 200, 150), postorder_rect)
        pygame.draw.rect(screen, (50, 150, 100), postorder_rect, 2)
        post_text = self.font.render("Post-Order", True, (255, 255, 255))
        screen.blit(post_text, (postorder_rect.centerx - post_text.get_width() // 2,
                               postorder_rect.centery - post_text.get_height() // 2))
        y_offset += button_height + 20
        
        # Message display
        if self.message_timer > 0:
            msg = self.font.render(self.message, True, (0, 100, 0))
            screen.blit(msg, (panel_x + 20, panel_y + panel_height - 50))
            self.message_timer -= 1
        
        return (complete_rect, incomplete_build_rect, depth_up_rect, depth_down_rect, clear_rect,
                preorder_rect, inorder_rect, postorder_rect,
                manual_toggle_rect, manual_input_rect, left_rect, right_rect, manual_insert_rect, set_root_rect, clear_sel_rect)
    
    def draw_setup_prompt(self, screen):
        """Draw the initial setup prompt to choose auto-generate or manual input"""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(200)
        overlay.fill((50, 50, 50))
        screen.blit(overlay, (0, 0))
        
        # Dialog box
        dialog_width = 500
        dialog_height = 300
        dialog_x = (self.screen_width - dialog_width) // 2
        dialog_y = (self.screen_height - dialog_height) // 2
        
        # Draw dialog background
        pygame.draw.rect(screen, (240, 240, 240), (dialog_x, dialog_y, dialog_width, dialog_height))
        pygame.draw.rect(screen, (50, 50, 50), (dialog_x, dialog_y, dialog_width, dialog_height), 3)
        
        # Draw title
        title_font = pygame.font.SysFont("Courier New", 28, bold=True)
        title = title_font.render("Binary Tree Setup", True, (50, 50, 50))
        screen.blit(title, (dialog_x + (dialog_width - title.get_width()) // 2, dialog_y + 30))
        
        # Draw question
        question_font = pygame.font.SysFont("Courier New", 16)
        question = question_font.render("How do you want to build the tree?", True, (50, 50, 50))
        screen.blit(question, (dialog_x + (dialog_width - question.get_width()) // 2, dialog_y + 90))
        
        # Auto-generate button
        auto_rect = pygame.Rect(dialog_x + 30, dialog_y + 150, 200, 50)
        pygame.draw.rect(screen, (100, 200, 100), auto_rect)
        pygame.draw.rect(screen, (50, 150, 50), auto_rect, 3)
        auto_text = pygame.font.SysFont("Courier New", 16, bold=True).render("Auto-Generate", True, (255, 255, 255))
        screen.blit(auto_text, (auto_rect.centerx - auto_text.get_width() // 2,
                               auto_rect.centery - auto_text.get_height() // 2))
        
        # Manual input button
        manual_rect = pygame.Rect(dialog_x + 270, dialog_y + 150, 200, 50)
        pygame.draw.rect(screen, (200, 150, 100), manual_rect)
        pygame.draw.rect(screen, (150, 100, 50), manual_rect, 3)
        manual_text = pygame.font.SysFont("Courier New", 16, bold=True).render("Manual Input", True, (255, 255, 255))
        screen.blit(manual_text, (manual_rect.centerx - manual_text.get_width() // 2,
                                 manual_rect.centery - manual_text.get_height() // 2))
        
        return auto_rect, manual_rect
    
    def draw_manual_input_screen(self, screen):
        """Draw interactive manual input interface with live tree preview."""
        # Draw tree behind the overlay for real-time preview
        self.draw_tree(screen)
        
        # Semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(160)
        overlay.fill((50, 50, 50))
        screen.blit(overlay, (0, 0))
        
        # Input panel
        panel_width = 700
        panel_height = 420
        panel_x = (self.screen_width - panel_width) // 2
        panel_y = (self.screen_height - panel_height) // 2
        
        # Draw panel background
        pygame.draw.rect(screen, (240, 240, 240), (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(screen, (50, 50, 50), (panel_x, panel_y, panel_width, panel_height), 3)
        
        # Draw title
        title_font = pygame.font.SysFont("Courier New", 24, bold=True)
        title = title_font.render("Build Tree Manually", True, (50, 50, 50))
        screen.blit(title, (panel_x + (panel_width - title.get_width()) // 2, panel_y + 16))
        
        # Instructions
        instr_font = pygame.font.SysFont("Courier New", 14)
        instr1 = instr_font.render("1) Type a number", True, (50, 50, 50))
        instr2 = instr_font.render("2) Click a node to select parent", True, (50, 50, 50))
        instr3 = instr_font.render("3) Choose Left/Right, then Insert", True, (50, 50, 50))
        screen.blit(instr1, (panel_x + 20, panel_y + 54))
        screen.blit(instr2, (panel_x + 20, panel_y + 74))
        screen.blit(instr3, (panel_x + 20, panel_y + 94))
        
        # Input box for single value
        input_box_rect = pygame.Rect(panel_x + 20, panel_y + 122, panel_width - 40, 46)
        pygame.draw.rect(screen, (255, 255, 255), input_box_rect)
        pygame.draw.rect(screen, (100, 100, 100), input_box_rect, 2)
        input_text = instr_font.render(self.manual_value_buffer, True, (0, 0, 0))
        screen.blit(input_text, (input_box_rect.x + 10, input_box_rect.y + 12))
        
        # Selected parent info
        info_font = pygame.font.SysFont("Courier New", 14, bold=True)
        parent_val = self.manual_selected_parent.value if self.manual_selected_parent else "None"
        parent_text = info_font.render(f"Selected Parent: {parent_val}", True, (50, 50, 50))
        screen.blit(parent_text, (panel_x + 20, panel_y + 180))
        
        # Side selection buttons
        left_rect = pygame.Rect(panel_x + 20, panel_y + 210, 90, 36)
        right_rect = pygame.Rect(panel_x + 120, panel_y + 210, 90, 36)
        
        left_active = (self.manual_insert_side == "left")
        right_active = (self.manual_insert_side == "right")
        pygame.draw.rect(screen, (100, 200, 100) if left_active else (180, 180, 180), left_rect)
        pygame.draw.rect(screen, (50, 150, 50), left_rect, 2)
        left_text = pygame.font.SysFont("Courier New", 14, bold=True).render("Left", True, (255, 255, 255))
        screen.blit(left_text, (left_rect.centerx - left_text.get_width() // 2,
                                left_rect.centery - left_text.get_height() // 2))
        
        pygame.draw.rect(screen, (100, 200, 100) if right_active else (180, 180, 180), right_rect)
        pygame.draw.rect(screen, (50, 150, 50), right_rect, 2)
        right_text = pygame.font.SysFont("Courier New", 14, bold=True).render("Right", True, (255, 255, 255))
        screen.blit(right_text, (right_rect.centerx - right_text.get_width() // 2,
                                 right_rect.centery - right_text.get_height() // 2))
        
        # Insert / Set Root / Finish / Cancel buttons
        insert_rect = pygame.Rect(panel_x + 230, panel_y + 210, 120, 38)
        pygame.draw.rect(screen, (150, 100, 200), insert_rect)
        pygame.draw.rect(screen, (100, 50, 150), insert_rect, 2)
        insert_text = pygame.font.SysFont("Courier New", 16, bold=True).render("Insert", True, (255, 255, 255))
        screen.blit(insert_text, (insert_rect.centerx - insert_text.get_width() // 2,
                                  insert_rect.centery - insert_text.get_height() // 2))
        
        set_root_rect = None
        if self.tree.root is None:
            set_root_rect = pygame.Rect(panel_x + 360, panel_y + 210, 140, 38)
            pygame.draw.rect(screen, (100, 200, 100), set_root_rect)
            pygame.draw.rect(screen, (50, 150, 50), set_root_rect, 2)
            set_root_text = pygame.font.SysFont("Courier New", 16, bold=True).render("Set as Root", True, (255, 255, 255))
            screen.blit(set_root_text, (set_root_rect.centerx - set_root_text.get_width() // 2,
                                        set_root_rect.centery - set_root_text.get_height() // 2))
        
        finish_rect = pygame.Rect(panel_x + 20, panel_y + 268, 150, 40)
        pygame.draw.rect(screen, (100, 150, 200), finish_rect)
        pygame.draw.rect(screen, (50, 100, 150), finish_rect, 2)
        finish_text = pygame.font.SysFont("Courier New", 16, bold=True).render("Finish", True, (255, 255, 255))
        screen.blit(finish_text, (finish_rect.centerx - finish_text.get_width() // 2,
                                  finish_rect.centery - finish_text.get_height() // 2))
        
        cancel_rect = pygame.Rect(panel_x + panel_width - 170, panel_y + 268, 150, 40)
        pygame.draw.rect(screen, (200, 100, 100), cancel_rect)
        pygame.draw.rect(screen, (150, 50, 50), cancel_rect, 2)
        cancel_text = pygame.font.SysFont("Courier New", 16, bold=True).render("Cancel", True, (255, 255, 255))
        screen.blit(cancel_text, (cancel_rect.centerx - cancel_text.get_width() // 2,
                                 cancel_rect.centery - cancel_text.get_height() // 2))
        
        # Guidance
        guide_font = pygame.font.SysFont("Courier New", 12)
        guide = guide_font.render("Tip: Click a node in the background to select parent.", True, (100, 100, 100))
        screen.blit(guide, (panel_x + 20, panel_y + panel_height - 52))
        
        return input_box_rect, left_rect, right_rect, insert_rect, set_root_rect, finish_rect, cancel_rect

    def _compute_depth(self, node: Optional[Node]) -> int:
        if node is None:
            return 0
        return 1 + max(self._compute_depth(node.left), self._compute_depth(node.right))

    def _update_current_depth(self) -> None:
        self.current_depth = max(1, self._compute_depth(self.tree.root))

    def get_node_at_click(self, pos) -> Optional[Node]:
        """Return the node at the clicked position, if any."""
        positions = self.calculate_positions(self.current_depth)
        radius = 35
        for level in positions:
            for node, (x, y) in positions[level].items():
                dx = pos[0] - x
                dy = pos[1] - y
                if dx * dx + dy * dy <= radius * radius:
                    return node
        return None

    def insert_manual_value(self) -> bool:
        """Insert the value in manual_value_buffer using current selection."""
        try:
            value = int(self.manual_value_buffer.strip())
        except ValueError:
            self.message = "Enter a valid integer"
            self.message_timer = 120
            return False

        # Insert as root if empty or requested
        if self.tree.root is None:
            self.tree.root = Node(value)
            self.manual_selected_parent = self.tree.root
            self._update_current_depth()
            self.message = "Root node set"
            self.message_timer = 90
            return True

        # Need a selected parent
        if not self.manual_selected_parent:
            self.message = "Select a parent by clicking a node"
            self.message_timer = 120
            return False

        parent = self.manual_selected_parent
        side = self.manual_insert_side
        if side == "left":
            if parent.left is None:
                parent.left = Node(value)
                self._update_current_depth()
                self.message = "Inserted at left child"
                self.message_timer = 90
                return True
            else:
                self.message = "Left child already occupied"
                self.message_timer = 120
                return False
        else:
            if parent.right is None:
                parent.right = Node(value)
                self._update_current_depth()
                self.message = "Inserted at right child"
                self.message_timer = 90
                return True
            else:
                self.message = "Right child already occupied"
                self.message_timer = 120
                return False
    
    def draw_traversal_output(self, screen):
        """Draw traversal results at the bottom of the window"""
        if not self.traversal_result:
            return
            
        # Bottom panel dimensions - made bigger
        bottom_panel_x = 30
        bottom_panel_y = self.screen_height - 140
        bottom_panel_width = self.screen_width - 60
        bottom_panel_height = 100
        
        # Draw bottom panel background
        pygame.draw.rect(screen, (245, 245, 245), (bottom_panel_x, bottom_panel_y, bottom_panel_width, bottom_panel_height))
        pygame.draw.rect(screen, (0, 0, 0), (bottom_panel_x, bottom_panel_y, bottom_panel_width, bottom_panel_height), 2)
        
        # Draw title with larger font
        title_y = bottom_panel_y + 15
        title_font = pygame.font.SysFont("Courier New", 18, bold=True)
        result_label = title_font.render(f"{self.traversal_type} Traversal Result:", True, (50, 50, 50))
        screen.blit(result_label, (bottom_panel_x + 20, title_y))
        
        # Draw result with larger font
        result_y = title_y + 35
        result_str = str(self.traversal_result)
        
        # Format the result nicely
        if len(result_str) > 2:  # Remove brackets if it's a list
            result_str = result_str.strip('[]')
        
        # Use larger font for results
        result_font = pygame.font.SysFont("Courier New", 16, bold=True)
        
        # Split long results into multiple lines if needed
        max_chars_per_line = (bottom_panel_width - 40) // 10  # Adjust for larger font
        
        if len(result_str) > max_chars_per_line:
            # Split into multiple lines
            words = result_str.split(', ')
            lines = []
            current_line = ""
            
            for word in words:
                test_line = current_line + (', ' if current_line else '') + word
                if len(test_line) <= max_chars_per_line:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word
            
            if current_line:
                lines.append(current_line)
            
            # Draw each line
            for i, line in enumerate(lines):
                if i < 2:  # Only show first 2 lines to fit in panel
                    line_y = result_y + (i * 22)
                    result_text = result_font.render(line, True, (100, 50, 50))
                    screen.blit(result_text, (bottom_panel_x + 20, line_y))
        else:
            result_text = result_font.render(result_str, True, (100, 50, 50))
            screen.blit(result_text, (bottom_panel_x + 20, result_y))

    def build_manual_tree(self, values_str):
        """Build tree from manually entered values"""
        try:
            # Parse the input string into integers
            values = [int(x) for x in values_str.split()]
            
            if not values:
                self.message = "Please enter at least one value"
                self.message_timer = 120
                return False
            
            # Clear and rebuild tree
            self.tree = BinaryTree(max_depth=self.max_depth)
            
            # Insert values using level-order insertion
            for value in values:
                self.tree.insert(value)
            
            self.message = f"Built manual tree with {len(values)} nodes"
            self.message_timer = 120
            self.traversal_result = ""
            self.traversal_type = ""
            # Reset animation
            self.animation_active = False
            self.animation_nodes = []
            self.current_highlight_index = 0
            
            return True
            
        except ValueError:
            self.message = "Error: Please enter valid integers only"
            self.message_timer = 120
            return False
    
    def handle_event(self, event, rects):
        """Handle user input events"""
        # Unpack rects including manual controls (some may be None)
        (
            complete_rect, incomplete_build_rect, depth_up_rect, depth_down_rect, clear_rect,
            preorder_rect, inorder_rect, postorder_rect,
            manual_toggle_rect, manual_input_rect, left_rect, right_rect, manual_insert_rect, set_root_rect, clear_sel_rect
        ) = rects

        # Keyboard input for manual mode
        if event.type == pygame.KEYDOWN and self.manual_mode:
            if event.key == pygame.K_BACKSPACE:
                self.manual_value_buffer = self.manual_value_buffer[:-1]
            elif event.key == pygame.K_RETURN:
                if self.insert_manual_value():
                    self.manual_value_buffer = ""
            else:
                # Allow digits and optional leading minus
                ch = event.unicode
                if len(self.manual_value_buffer) < 6 and (ch.isdigit() or (ch == '-' and len(self.manual_value_buffer) == 0)):
                    self.manual_value_buffer += ch

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Build Complete
            if complete_rect and complete_rect.collidepoint(event.pos):
                try:
                    self.tree = BinaryTree(max_depth=self.max_depth)
                    self.tree.build_full_tree(self.current_depth)
                    self.message = f"Built complete tree with depth {self.current_depth}"
                    self.message_timer = 120
                    self.traversal_result = ""
                    self.traversal_type = ""
                    # Reset animation
                    self.animation_active = False
                    self.animation_nodes = []
                    self.current_highlight_index = 0
                except Exception as e:
                    self.message = f"Error: {str(e)[:30]}..."
                    self.message_timer = 120
            # Build Incomplete
            elif incomplete_build_rect and incomplete_build_rect.collidepoint(event.pos):
                try:
                    self.tree = BinaryTree(max_depth=self.max_depth)
                    self.tree.build_incomplete_tree(self.current_depth)
                    self.message = f"Built incomplete tree with depth {self.current_depth}"
                    self.message_timer = 120
                    self.traversal_result = ""
                    self.traversal_type = ""
                    # Reset animation
                    self.animation_active = False
                    self.animation_nodes = []
                    self.current_highlight_index = 0
                except Exception as e:
                    self.message = f"Error: {str(e)[:30]}..."
                    self.message_timer = 120
            # Depth+
            elif depth_up_rect and depth_up_rect.collidepoint(event.pos):
                if self.current_depth < self.max_depth:
                    self.current_depth += 1
                    self.message = f"Depth set to {self.current_depth}"
                    self.message_timer = 60
            # Depth-
            elif depth_down_rect and depth_down_rect.collidepoint(event.pos):
                if self.current_depth > 1:
                    self.current_depth -= 1
                    self.message = f"Depth set to {self.current_depth}"
                    self.message_timer = 60
            # Clear Tree
            elif clear_rect and clear_rect.collidepoint(event.pos):
                self.tree = BinaryTree()
                self.traversal_result = ""
                self.traversal_type = ""
                self.message = "Tree cleared"
                self.message_timer = 60
            # Traversals
            elif preorder_rect and preorder_rect.collidepoint(event.pos):
                if self.tree.root:
                    result, nodes = self.tree.preorder()
                    # Extract values from nodes to ensure display matches animation
                    self.traversal_result = [node.value for node in nodes]
                    self.traversal_type = "Pre-Order"
                    self.animation_nodes = nodes
                    self.animation_active = True
                    self.current_highlight_index = 0
                    self.animation_timer = 0
                    self.message = "Pre-order traversal started"
                    self.message_timer = 60
                else:
                    self.message = "No tree to traverse!"
                    self.message_timer = 60
            elif inorder_rect and inorder_rect.collidepoint(event.pos):
                if self.tree.root:
                    result, nodes = self.tree.inorder()
                    # Extract values from nodes to ensure display matches animation
                    self.traversal_result = [node.value for node in nodes]
                    self.traversal_type = "In-Order"
                    self.animation_nodes = nodes
                    self.animation_active = True
                    self.current_highlight_index = 0
                    self.animation_timer = 0
                    self.message = "In-order traversal started"
                    self.message_timer = 60
                else:
                    self.message = "No tree to traverse!"
                    self.message_timer = 60
            elif postorder_rect and postorder_rect.collidepoint(event.pos):
                if self.tree.root:
                    result, nodes = self.tree.postorder()
                    # Extract values from nodes to ensure display matches animation
                    self.traversal_result = [node.value for node in nodes]
                    self.traversal_type = "Post-Order"
                    self.animation_nodes = nodes
                    self.animation_active = True
                    self.current_highlight_index = 0
                    self.animation_timer = 0
                    self.message = "Post-order traversal started"
                    self.message_timer = 60
                else:
                    self.message = "No tree to traverse!"
                    self.message_timer = 60

            # Manual controls
            elif manual_toggle_rect and manual_toggle_rect.collidepoint(event.pos):
                self.manual_mode = not self.manual_mode
                self.message = f"Manual mode {'ON' if self.manual_mode else 'OFF'}"
                self.message_timer = 60
            elif self.manual_mode and left_rect and left_rect.collidepoint(event.pos):
                self.manual_insert_side = "left"
            elif self.manual_mode and right_rect and right_rect.collidepoint(event.pos):
                self.manual_insert_side = "right"
            elif self.manual_mode and manual_insert_rect and manual_insert_rect.collidepoint(event.pos):
                if self.insert_manual_value():
                    self.manual_value_buffer = ""
            elif self.manual_mode and set_root_rect and set_root_rect.collidepoint(event.pos):
                if self.insert_manual_value():
                    self.manual_value_buffer = ""
            elif self.manual_mode and clear_sel_rect and clear_sel_rect.collidepoint(event.pos):
                self.manual_selected_parent = None
            else:
                # Click in tree area to select parent
                panel_x = self.screen_width - 370
                if self.manual_mode and event.pos[0] < panel_x:
                    node = self.get_node_at_click(event.pos)
                    if node:
                        self.manual_selected_parent = node

def bt_menu(screen, clock, globalbg_img, back_btn):
    """Binary Tree menu function"""
    running = True
    visualizer = BinaryTreeVisualizer(screen.get_width(), screen.get_height())
    
    while running:
        # Update animation
        visualizer.update_animation()
        
        # Show background
        screen.blit(globalbg_img, (0, 0))
        
        # Draw title
        title_font = pygame.font.SysFont("Courier New", 60, bold=True)
        title = title_font.render("Binary CaTree", True, (50, 50, 50))
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 30))
        
        # Draw tree
        visualizer.draw_tree(screen)
        
        # Draw controls and get button rectangles (includes manual input controls)
        rects = visualizer.draw_controls(screen)
        
        # Draw traversal output at bottom
        visualizer.draw_traversal_output(screen)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            visualizer.handle_event(event, rects)
        
        # Draw back button
        if back_btn.draw():
            running = False

        # Update display
        pygame.display.flip()
        clock.tick(60)  # limits FPS to 60

    return True
