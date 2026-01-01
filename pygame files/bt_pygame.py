import pygame

def bt_menu(screen, clock, globalbg_img, back_btn):
    """Binary Tree menu function"""
    running = True
    while running:
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        # show global background image
        screen.blit(globalbg_img, (0, 0))

        # RENDER YOUR BINARY TREE CONTENT HERE
        
        # Draw back button
        if back_btn.draw():
            running = False

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    return True
