import pygame
import sys
import os

current_dir = os.path.dirname(__file__)
bst_path = os.path.abspath(os.path.join(current_dir, "..", "core_programs", "core_programs"))
sys.path.append(bst_path)
from binary_search_tree import BinarySearchTree

def draw_bst(screen, node, x, y, font, h_spacing=500, v_spacing=100):
    if node is None:
        return
    pygame.draw.circle(screen, (0, 120, 255), (x, y), 30) # draw circle for node
    text = font.render(str(node.number), True, (255, 255, 255)) #determines characteristic of text
    screen.blit(text, text.get_rect(center=(x, y))) #shows text in screen

    if node.left: #left child, number is lower/ equal to root.
        child_x = x - h_spacing
        child_y = y + v_spacing
        new_h_spacing=max(h_spacing/2,30)
        pygame.draw.line(screen, (0, 0, 0), (x, y), (child_x, child_y), 2)
        pygame.draw.circle(screen, (0, 120, 255), (child_x, child_y), 30) # draw circle for node
        draw_bst(screen, node.left, child_x, child_y, font, new_h_spacing, v_spacing)
    
    if node.right: #right child, number is higher than the root.
        child_x = x + h_spacing
        child_y = y + v_spacing
        new_h_spacing=max(h_spacing/2,30)
        pygame.draw.line(screen, (0, 0, 0), (x, y), (child_x, child_y), 2)
        pygame.draw.circle(screen, (0, 120, 255), (child_x, child_y), 30) # draw circle for node
        draw_bst(screen, node.right, child_x, child_y, font, new_h_spacing, v_spacing)

def bst_menu(screen, clock, globalbg_img, back_btn):
    """Binary Search Tree menu function"""
    user_input = ""
    bst = BinarySearchTree()
    font = pygame.font.SysFont(None, 26)
    input_font = pygame.font.SysFont(None, 40)
    input_box_img = pygame.image.load("images/bst_input_box.png").convert_alpha()
    input_box_img = pygame.transform.scale(input_box_img, (300, 300)) 
    input_box_rect = input_box_img.get_rect()
    input_box_rect.center = (screen.get_width() // 2, screen.get_height() - 30)
    tree_offset_x = 0
    tree_offset_y = 0
    
    
    running = True
    while running:

        # show global background image
        screen.blit(globalbg_img, (0, 0))

        # RENDER YOUR BINARY SEARCH TREE CONTENT HERErf
        for event in pygame.event.get():# poll for events
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
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
        
        if bst.root:
            draw_bst(screen, bst.root, screen.get_width()//2+tree_offset_x, 80+tree_offset_y, font)

        screen.blit(input_box_img, input_box_rect)
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