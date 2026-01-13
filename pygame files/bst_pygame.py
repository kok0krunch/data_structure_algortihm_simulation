import pygame
import sys
import os

current_dir = os.path.dirname(__file__)

bst_path = os.path.abspath(
    os.path.join(current_dir, "..", "core_programs", "core_programs")
)

sys.path.append(bst_path)

from binary_search_tree import BinarySearchTree

def bst_menu(screen, clock, globalbg_img, back_btn):
    """Binary Search Tree menu function"""
    running = True
    while running:

        # show global background image
        screen.blit(globalbg_img, (0, 0))

        # RENDER YOUR BINARY SEARCH TREE CONTENT HERE
        width = screen.get_width()
        height = screen.get_height()
        x_intercept=width//2
        y_intercept=height//6

        for event in pygame.event.get():# poll for events
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Enter key
                    if user_input != "":
                        number = int(user_input)
                        binary_search_tree.insert(number)  # insert into BST
                        pygame.draw.circle(screen, (255,0,0), (x_intercept,y_intercept), 50, width=0)
                        font = pygame.font.SysFont(None, 30)
                        text = font.render("5", True, (255, 255, 255))
                        text_rect = text.get_rect(center=(x_intercept, y_intercept))
                        screen.blit(text, text_rect)
                        user_input = ""  # clear for next input
                elif event.key == pygame.K_BACKSPACE:  # allow deleting
                    user_input = user_input[:-1]
                elif event.unicode.isdigit():  # allow only digits
                    user_input += event.unicode

        # Draw back button
        if back_btn.draw():
            running = False

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    return True
