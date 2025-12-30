import pygame
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core_programs'))
import core_programs_module as cpm

def run_queue(screen, clock, bg_image, back_img_original, settings):
    """Run the queue activity"""
    # Create back button
    scale = settings['resolution'][0] / 1280
    back_button = create_button_class()(int(0 * scale), int(-70 * scale), back_img_original, 0.4 * scale)
    
    running = True
    while running:
        # Display background
        screen.blit(bg_image, (0, 0))
        
        # Draw title
        font = pygame.font.Font(None, int(48 * scale))
        title_text = font.render('Queue - 4 Lane Parking Garage', True, (255, 255, 255))
        screen.blit(title_text, (int(350 * scale), int(50 * scale)))
        
        # Draw back button
        if back_button.draw(screen):
            running = False
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        pygame.display.flip()
        clock.tick(60)


def create_button_class():
    """Create Button class for this module"""
    class Button():
        def __init__(self, x, y, image, scale):
            width = image.get_width()
            height = image.get_height()
            self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)
            self.clicked = False
        
        def draw(self, screen):
            action = False
            mouse_pos = pygame.mouse.get_pos()
            
            if self.rect.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True
                    action = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            
            screen.blit(self.image, (self.rect.x, self.rect.y))
            return action
    
    return Button
