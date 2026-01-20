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

    def draw_node(self, screen, x, y, value, highlighted=False):
        """Draw a single node at the given position"""
        if self.node_img:
            # Use the BST node image
            node_rect = self.node_img.get_rect(center=(x, y))
            if highlighted:
                # Add pulsing highlight effect
                pulse = abs(math.sin(pygame.time.get_ticks() * 0.01)) * 50 + 50
                highlight_surf = pygame.Surface((100, 100))
                highlight_surf.fill((255, 255, 0))
                highlight_surf.set_alpha(pulse)
                screen.blit(highlight_surf, (x - 50, y - 50))
            screen.blit(self.node_img, node_rect)
        else:
            # Fallback to circle
            if highlighted:
                # Pulsing highlight effect
                pulse = abs(math.sin(pygame.time.get_ticks() * 0.01)) * 30 + 30
                pygame.draw.circle(screen, (255, 255, 0), (x, y), 45 + pulse//2)
            
            color = (100, 255, 100) if highlighted else self.node_color
            pygame.draw.circle(screen, color, (x, y), 45)
            pygame.draw.circle(screen, (0, 0, 0), (x, y), 45, 3)
        
        # Draw value text with different color when highlighted
        text_color = (255, 0, 0) if highlighted else (0, 0, 0)
        text = self.font.render(str(value), True, text_color)
        text_rect = text.get_rect(center=(x, y))
        screen.blit(text, text_rect)

    def draw_line(self, screen, start_pos, end_pos):
        """Draw a line between two nodes"""
        pygame.draw.line(screen, self.line_color, start_pos, end_pos, 3)

    def calculate_positions(self, depth):
        """Calculate node positions for the tree based on depth"""
        positions = {}
        if depth == 0 or not self.tree.root:
            return positions
        
        # Tree drawing area - adjusted for larger trees
        tree_area_x = 50
        tree_area_y = 120
        tree_area_width = self.screen_width - 400
        tree_area_height = 500
        
        # Calculate minimum spacing needed for nodes (considering node size)
        min_node_spacing = 100  # Minimum distance between nodes
        
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
        
        def position_nodes_recursive(node, level, position_in_level, positions_at_level):
            if node is None or level >= depth:
                return
            
            if level not in positions:
                positions[level] = {}
            
            # Calculate vertical position
            level_spacing = tree_area_height // max(depth, 1)
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
        tree_panel_width = self.screen_width - 430
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
            if (50 <= node_pos[0] <= self.screen_width - 450 and 
                80 <= node_pos[1] <= self.screen_height - 50):
                
                # Check if this node should be highlighted
                highlighted = (self.animation_active and 
                             self.current_highlight_index < len(self.animation_nodes) and
                             node == self.animation_nodes[self.current_highlight_index])
                
                self.draw_node(screen, node_pos[0], node_pos[1], node.value, highlighted)
            
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
        panel_x = self.screen_width - 380
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
        
        # Depth selector
        depth_label = self.font.render(f"Tree Depth: {self.current_depth}", True, (50, 50, 50))
        screen.blit(depth_label, (panel_x + 20, panel_y + y_offset))
        y_offset += 30
        
        # Buttons
        button_width = 110
        button_height = 30
        button_spacing = 12
        
        # Build Tree button
        build_rect = pygame.Rect(panel_x + 20, panel_y + y_offset, button_width, button_height)
        pygame.draw.rect(screen, (100, 200, 100), build_rect)
        pygame.draw.rect(screen, (50, 150, 50), build_rect, 2)
        build_text = self.font.render("Build Tree", True, (255, 255, 255))
        screen.blit(build_text, (build_rect.centerx - build_text.get_width() // 2,
                                build_rect.centery - build_text.get_height() // 2))
        y_offset += button_height + button_spacing
        
        # Depth buttons
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
        
        return (build_rect, depth_up_rect, depth_down_rect, clear_rect, 
                preorder_rect, inorder_rect, postorder_rect)
    
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

    def handle_event(self, event, rects):
        """Handle user input events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            build_rect, depth_up_rect, depth_down_rect, clear_rect, preorder_rect, inorder_rect, postorder_rect = rects
            
            if build_rect.collidepoint(event.pos):
                try:
                    self.tree = BinaryTree(max_depth=self.max_depth)
                    self.tree.build_full_tree(self.current_depth)
                    self.message = f"Built tree with depth {self.current_depth}"
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
            
            elif depth_up_rect.collidepoint(event.pos):
                if self.current_depth < self.max_depth:
                    self.current_depth += 1
                    self.message = f"Depth set to {self.current_depth}"
                    self.message_timer = 60
            
            elif depth_down_rect.collidepoint(event.pos):
                if self.current_depth > 1:
                    self.current_depth -= 1
                    self.message = f"Depth set to {self.current_depth}"
                    self.message_timer = 60
            
            elif clear_rect.collidepoint(event.pos):
                self.tree = BinaryTree()
                self.traversal_result = ""
                self.traversal_type = ""
                self.message = "Tree cleared"
                self.message_timer = 60
            
            elif preorder_rect.collidepoint(event.pos):
                if self.tree.root:
                    result, nodes = self.tree.preorder()
                    self.traversal_result = result
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
            
            elif inorder_rect.collidepoint(event.pos):
                if self.tree.root:
                    result, nodes = self.tree.inorder()
                    self.traversal_result = result
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
            
            elif postorder_rect.collidepoint(event.pos):
                if self.tree.root:
                    result, nodes = self.tree.postorder()
                    self.traversal_result = result
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
        
        # Draw controls and get button rectangles
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
