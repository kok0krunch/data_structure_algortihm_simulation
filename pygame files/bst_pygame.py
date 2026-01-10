import pygame

def bst_menu(screen, clock, globalbg_img, back_btn):
    """Binary Search Tree menu function"""
    running = True
    while running:
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        # show global background image
        screen.blit(globalbg_img, (0, 0))

        # RENDER YOUR BINARY SEARCH TREE CONTENT HERE
        width = screen.get_width()
        height = screen.get_height()
        x_center=width//2
        y_center=height//2
        pygame.draw.circle(screen, (255,0,0), (x_center,y_center), 100, width=0)

        # Draw back button
        if back_btn.draw():
            running = False

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    return True
