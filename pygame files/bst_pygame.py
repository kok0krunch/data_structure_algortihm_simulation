import pygame
import sys
import os

current_dir = os.path.dirname(__file__)
bst_path = os.path.abspath(os.path.join(current_dir, "..", "core_programs", "core_programs"))
sys.path.append(bst_path)
from binary_search_tree import BinarySearchTree

def draw_bst(screen, node, x, y, font, h_spacing=500, v_spacing=110):
    if node is None:
        return
    node_img = pygame.image.load("images/bst_images/bst_node.png").convert_alpha()
    node_img = pygame.transform.scale(node_img, (75, 75))
    node_rect = node_img.get_rect(center=(x+5, y-2))
    radius=31.5
    screen.blit(node_img, node_rect)
    text = font.render(str(node.number), True, (0, 0, 0)) #shows text in screen
    screen.blit(text, text.get_rect(center=(x, y)))

    if node.left: #left child, number is lower/ equal to root.
        child_x = x - h_spacing
        child_y = y + v_spacing
        new_h_spacing=max(h_spacing/2,30)
        pygame.draw.line(screen, (0,0,0), (x, y + radius), (child_x, child_y - radius), 2)
        node_rect = node_img.get_rect(center=(child_x, child_y))
        draw_bst(screen, node.left, child_x, child_y, font, new_h_spacing, v_spacing)
    
    if node.right: #right child, number is higher than the root.
        child_x = x + h_spacing
        child_y = y + v_spacing
        new_h_spacing=max(h_spacing/2,30)
        pygame.draw.line(screen, (0,0,0), (x, y + radius), (child_x, child_y - radius), 2)
        node_rect = node_img.get_rect(center=(child_x, child_y))
        draw_bst(screen, node.right, child_x, child_y, font, new_h_spacing, v_spacing)

def bst_menu(screen, clock, globalbg_img, back_btn):
    # graphics
    input_box_img = pygame.image.load("images/bst_images/bst_input_box.png").convert_alpha()
    delete_button_img = pygame.image.load("images/bst_images/bst_delete.png").convert_alpha()
    insert_button_img = pygame.image.load("images/bst_images/bst_insert.png").convert_alpha()
    center_button_img = pygame.image.load("images/bst_images/bst_center.png").convert_alpha()
    reset_button_img = pygame.image.load("images/bst_images/bst_reset.png").convert_alpha()
    search_button_img = pygame.image.load("images/bst_images/bst_search.png").convert_alpha()

    #graphics_scale
    input_box_img = pygame.transform.scale(input_box_img, (300, 300))
    delete_button_img = pygame.transform.scale(delete_button_img, (100, 100))
    insert_button_img = pygame.transform.scale(insert_button_img, (100, 100))
    center_button_img = pygame.transform.scale(center_button_img, (100, 100))
    reset_button_img = pygame.transform.scale(reset_button_img, (100, 100))
    search_button_img = pygame.transform.scale(search_button_img, (100, 100))

    #graphics_rect
    input_box_rect = input_box_img.get_rect()
    delete_button_rect = delete_button_img.get_rect(topleft=(25,200))
    insert_button_rect = insert_button_img.get_rect(topleft=(25,150))
    center_button_rect = center_button_img.get_rect(topleft=(25,250))
    reset_button_rect = reset_button_img.get_rect(topleft=(25,300))
    search_button_rect = search_button_img.get_rect(topleft=(25,350))

    user_input = ""
    bst = BinarySearchTree()
    #graphics position
    input_box_rect.center = (screen.get_width() // 2, screen.get_height() - 30)
    font = pygame.font.SysFont(None, 26)
    input_font = pygame.font.SysFont(None, 40) 
    tree_offset_x = 0
    tree_offset_y = 0
    current_action="insert"
    past_action="insert"
    
    running = True
    while running:

        # show global background image
        screen.blit(globalbg_img, (0, 0))

        # RENDER YOUR BINARY SEARCH TREE CONTENT HERErf
        for event in pygame.event.get():# poll for events
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tree_offset_x += 50  # move tree right

                elif event.key == pygame.K_RIGHT:
                    tree_offset_x -= 50  # move tree left
                
                elif event.key == pygame.K_UP:
                    tree_offset_y += 50  # move tree up

                elif event.key == pygame.K_DOWN:
                    tree_offset_y -= 50  # move tree down

                elif event.key == pygame.K_RETURN:  # Enter key
                    if user_input != "":
                        number = int(user_input)
                        bst.insert(number)  # insert into BST
                        user_input = ""  # clear for next input

                elif event.key == pygame.K_BACKSPACE:  # allow deleting
                    user_input = user_input[:-1]

                elif event.unicode.isdigit():  # allow only digits
                    user_input += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if delete_button_rect.collidepoint(event.pos):
                    mouse_pos = event.pos

                    if insert_button_rect.collidepoint(mouse_pos):
                        past_action=current_action
                        current_action="insert"

                    elif delete_button_rect.collidepoint(mouse_pos):
                        past_action=current_action
                        current_action="delete"

                    elif search_button_rect.collidepoint(mouse_pos):
                        past_Action=current_action
                        current_action="serch"
                    
                    elif center_button_rect.collidepoint(mouse_pos):
                            draw_bst(screen, bst.root, screen.get_width()//2-tree_offset_x, 180-tree_offset_y, font)
                            tree_offset_x = 0
                            tree_offset_y = 0

        
        if bst.root:
            draw_bst(screen, bst.root, screen.get_width()//2+tree_offset_x, 180+tree_offset_y, font)

        instruction_font = pygame.font.SysFont(None, 48)
        instruction = "Welcome to Binary Search Tree maker! Input your number and enter to\n see it in front of you. If your binary search tree is cut off screen, use your \n up, left, down, and right keys to maneuver the tree. "
        instruction_surface = instruction_font.render(instruction, True, (0,0,0))
        x_margin=120
        y_margin=20+tree_offset_y
        instruction_rect = instruction_surface.get_rect(topleft=(x_margin,y_margin))
        screen.blit(instruction_surface, instruction_rect)

        #blit buttons
        screen.blit(input_box_img, input_box_rect)
        screen.blit(delete_button_img, delete_button_rect)
        screen.blit(reset_button_img, reset_button_rect)
        screen.blit(center_button_img, center_button_rect)
        screen.blit(search_button_img, search_button_rect)
        screen.blit(insert_button_img, insert_button_rect)

        if current_action=="insert":
            input_surface = input_font.render("Input: " + user_input, True, (0, 0, 0))
            input_rect = input_surface.get_rect(
            center=(screen.get_width() // 2, screen.get_height() - 45))
            screen.blit(input_surface, input_rect)
        
        if current_action=="delete":
            input_surface = input_font.render("Input: " + user_input, True, (0, 0, 0))
            input_rect = input_surface.get_rect(
            center=(screen.get_width() // 2, screen.get_height() - 45))
            screen.blit(input_surface, input_rect)

        # Draw back button
        if back_btn.draw():
            running = False

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    return True