#Make background - done
#Make buttons for activities - done
#Make title text - done
#Make options that change sound volume and screen resolution -done
#Make exit button - done
# Make credits
import pygame
import sys
import os

# Import activity modules
try:
    from stackpygame import run_stack
    from queuepygame import run_queue
    from btpygame import run_bt
    from bstpygame import run_bst
    from recursionpygame import run_recursion
except ImportError as e:
    print(f"Warning: Could not import activity modules: {e}")

# pygame setup
pygame.init()
pygame.font.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# Global settings
settings = {
    'volume': 0.5,  # 0.0 to 1.0
    'resolution': (1280, 720)  # Current resolution
}

def get_scale_factor():
    """Returns scale factor based on current resolution (base is 1280x720)"""
    base_width = 1280
    current_width = settings['resolution'][0]
    return current_width / base_width

#Load images
bg_image = pygame.image.load("main_menu_img/background_img/1920x1080_background.png")
bg_image = pygame.transform.scale(bg_image,(1280, 720))
title_image_original = pygame.image.load("main_menu_img/background_img/title.png").convert_alpha()
title_image = pygame.transform.scale(title_image_original,(600, 600))

#Load images of buttons (store originals)
start_img_original = pygame.image.load('main_menu_img/startbutton_img.png').convert_alpha()
options_img_original = pygame.image.load('main_menu_img/optionsbutton_img.png').convert_alpha()
exit_img_original = pygame.image.load('main_menu_img/exitbutton_img.png').convert_alpha()
credits_img_original = pygame.image.load('main_menu_img/creditsbutton_img.png').convert_alpha()

#Load images of start options and back button (store originals)
stack_img_original = pygame.image.load('main_menu_img/start_img/stacks_img.png').convert_alpha()
queue_img_original = pygame.image.load('main_menu_img/start_img/queue_img.png').convert_alpha()
bt_img_original = pygame.image.load('main_menu_img/start_img/bt_img.png').convert_alpha()
bst_img_original = pygame.image.load('main_menu_img/start_img/bst_img.png').convert_alpha()
recursion_img_original = pygame.image.load('main_menu_img/start_img/recursion_img.png').convert_alpha()
activities_title_img_original = pygame.image.load('main_menu_img/start_img/activities_title.png')

#Back button
back_img_original = pygame.image.load('main_menu_img/bbutton_img.png').convert_alpha()


#Class Button
class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
    
    def draw(self):
        action = False
        #get mouse position
        mouse_pos = pygame.mouse.get_pos()
        
        #check mouse hover and clicked conditions
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        # always reset clicked state when mouse button is released
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        #draw button on screen
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

#Class Slider
class Slider():
    def __init__(self, x, y, width, height, min_val, max_val, initial_val):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.dragging = False
        
        # Calculate handle position based on initial value
        val_range = max_val - min_val
        val_percent = (initial_val - min_val) / val_range
        self.handle_x = x + int(val_percent * width)
        self.handle_radius = 12
    
    def draw(self):
        # Draw slider bar
        pygame.draw.rect(screen, (100, 100, 100), self.rect)
        # Draw filled portion
        filled_width = self.handle_x - self.rect.x
        if filled_width > 0:
            pygame.draw.rect(screen, (0, 200, 0), (self.rect.x, self.rect.y, filled_width, self.rect.height))
        # Draw handle
        pygame.draw.circle(screen, (255, 255, 255), (self.handle_x, self.rect.centery), self.handle_radius)
        pygame.draw.circle(screen, (0, 0, 0), (self.handle_x, self.rect.centery), self.handle_radius, 2)
    
    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if clicking on handle
            dist = ((mouse_pos[0] - self.handle_x) ** 2 + (mouse_pos[1] - self.rect.centery) ** 2) ** 0.5
            if dist <= self.handle_radius:
                self.dragging = True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                # Update handle position
                self.handle_x = max(self.rect.x, min(mouse_pos[0], self.rect.x + self.rect.width))
                # Calculate value
                val_percent = (self.handle_x - self.rect.x) / self.rect.width
                self.value = self.min_val + val_percent * (self.max_val - self.min_val)
    
    def get_value(self):
        return self.value

def create_buttons():
    """Create or recreate all buttons with proper scaling based on resolution"""
    global start_button, options_button, exit_button, credits_button
    global stack_button, queue_button, bt_button, bst_button, recursion_button
    global back_button, title_image, activities_title_img
    
    scale = get_scale_factor()
    
    # Main menu buttons (base positions for 1280x720)
    start_button = Button(int(0 * scale), int(400 * scale), start_img_original, 0.5 * scale)
    options_button = Button(int(320 * scale), int(400 * scale), options_img_original, 0.5 * scale)
    exit_button = Button(int(640 * scale), int(400 * scale), exit_img_original, 0.5 * scale)
    credits_button = Button(int(980 * scale), int(400 * scale), credits_img_original, 0.5 * scale)
    
    # Scale activity images
    stack_img = pygame.transform.scale(stack_img_original, (int(200 * scale), int(200 * scale)))
    queue_img = pygame.transform.scale(queue_img_original, (int(200 * scale), int(200 * scale)))
    bt_img = pygame.transform.scale(bt_img_original, (int(200 * scale), int(200 * scale)))
    bst_img = pygame.transform.scale(bst_img_original, (int(200 * scale), int(200 * scale)))
    recursion_img = pygame.transform.scale(recursion_img_original, (int(200 * scale), int(200 * scale)))
    
    # Activity buttons (base positions for 1280x720)
    stack_button = Button(int(0 * scale), int(400 * scale), stack_img, 1)
    queue_button = Button(int(256 * scale), int(400 * scale), queue_img, 1)
    bt_button = Button(int(512 * scale), int(400 * scale), bt_img, 1)
    bst_button = Button(int(768 * scale), int(400 * scale), bst_img, 1)
    recursion_button = Button(int(1080 * scale), int(400 * scale), recursion_img, 1)
    
    # Back button
    back_button = Button(int(0 * scale), int(-70 * scale), back_img_original, 0.4 * scale)
    
    # Scale title images
    title_image = pygame.transform.scale(title_image_original, (int(600 * scale), int(600 * scale)))
    activities_title_img = pygame.transform.scale(activities_title_img_original, 
                                                  (int(activities_title_img_original.get_width() * scale), 
                                                   int(activities_title_img_original.get_height() * scale)))

# Create initial button instances
create_buttons()

""" Functions For The Main Menu """

def wait_for_mouse_release():
    # Prevent click-through when switching screens by waiting until the
    # left mouse button is released. Also pump events to keep window responsive.
    while pygame.mouse.get_pressed()[0]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
        clock.tick(60)

def main_menu():
    running = True
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        scale = get_scale_factor()
        screen.blit(bg_image,(0,0))  #Background Image
        screen.blit(title_image,(int(320 * scale), 0)) #Title Image

        if start_button.draw():
            print('Start')
            wait_for_mouse_release()
            start()
        if options_button.draw():
            print('Options')
            wait_for_mouse_release()
            options()
        if exit_button.draw():
            running = False
        if credits_button.draw():
            print('Credits')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()

def start():
    running = True
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        scale = get_scale_factor()
        screen.blit(bg_image,(0,0))  #Background Image
        screen.blit(activities_title_img,(int(300 * scale), 0)) #Title Image
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # RENDER YOUR GAME HERE
        if stack_button.draw():
            print('Stacks')
            wait_for_mouse_release()
            run_stack(screen, clock, bg_image, back_img_original, settings)
        if queue_button.draw():
            print('Queue')
            wait_for_mouse_release()
            run_queue(screen, clock, bg_image, back_img_original, settings)
        if bt_button.draw():
            print('Binary Tree')
            wait_for_mouse_release()
            run_bt(screen, clock, bg_image, back_img_original, settings)
        if bst_button.draw():
            print('Binary Search Tree')
            wait_for_mouse_release()
            run_bst(screen, clock, bg_image, back_img_original, settings)
        if recursion_button.draw():
            print('Recursion')
            wait_for_mouse_release()
            run_recursion(screen, clock, bg_image, back_img_original, settings)
        if back_button.draw():
            print('Back')
            wait_for_mouse_release()
            running = False

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    # Return control to the caller (main_menu) without quitting pygame
    return

def options():
    global screen, bg_image, settings
    
    scale = get_scale_factor()
    
    # Create volume slider with scaling
    volume_slider = Slider(int(400 * scale), int(200 * scale), int(400 * scale), int(20 * scale), 0.0, 1.0, settings['volume'])
    
    # Fonts with scaling
    font = pygame.font.Font(None, int(48 * scale))
    small_font = pygame.font.Font(None, int(36 * scale))
    
    running = True
    while running:
        scale = get_scale_factor()
        screen.blit(bg_image, (0, 0))
        
        # Title
        title_text = font.render('Options', True, (255, 255, 255))
        screen.blit(title_text, (int(540 * scale), int(50 * scale)))
        
        # Volume section
        volume_label = small_font.render('Volume', True, (255, 255, 255))
        screen.blit(volume_label, (int(400 * scale), int(150 * scale)))
        volume_slider.draw()
        volume_value = small_font.render(f'{int(volume_slider.get_value() * 100)}%', True, (255, 255, 255))
        screen.blit(volume_value, (int(820 * scale), int(190 * scale)))
        
        # Resolution section
        resolution_label = small_font.render('Resolution', True, (255, 255, 255))
        screen.blit(resolution_label, (int(400 * scale), int(300 * scale)))
        
        # Resolution buttons
        res_1280_text = small_font.render('1280x720', True, (255, 255, 255))
        res_1920_text = small_font.render('1920x1080', True, (255, 255, 255))
        
        res_1280_rect = pygame.Rect(int(400 * scale), int(350 * scale), int(200 * scale), int(50 * scale))
        res_1920_rect = pygame.Rect(int(620 * scale), int(350 * scale), int(200 * scale), int(50 * scale))
        
        # Highlight current resolution
        if settings['resolution'] == (1280, 720):
            pygame.draw.rect(screen, (0, 200, 0), res_1280_rect)
            pygame.draw.rect(screen, (100, 100, 100), res_1920_rect)
        else:
            pygame.draw.rect(screen, (100, 100, 100), res_1280_rect)
            pygame.draw.rect(screen, (0, 200, 0), res_1920_rect)
        
        pygame.draw.rect(screen, (255, 255, 255), res_1280_rect, 2)
        pygame.draw.rect(screen, (255, 255, 255), res_1920_rect, 2)
        
        screen.blit(res_1280_text, (int(415 * scale), int(360 * scale)))
        screen.blit(res_1920_text, (int(630 * scale), int(360 * scale)))
        
        # Back button
        if back_button.draw():
            print('Back from options')
            wait_for_mouse_release()
            running = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                raise SystemExit
            
            # Handle slider events
            volume_slider.handle_event(event)
            
            # Handle resolution button clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if res_1280_rect.collidepoint(mouse_pos):
                    settings['resolution'] = (1280, 720)
                    screen = pygame.display.set_mode((1280, 720))
                    # Rescale background
                    bg_image = pygame.image.load("main_menu_img/background_img/1920x1080_background.png")
                    bg_image = pygame.transform.scale(bg_image, (1280, 720))
                    # Recreate all buttons with new scaling
                    create_buttons()
                    # Recreate slider and fonts with new scaling
                    scale = get_scale_factor()
                    volume_slider = Slider(int(400 * scale), int(200 * scale), int(400 * scale), int(20 * scale), 0.0, 1.0, settings['volume'])
                    font = pygame.font.Font(None, int(48 * scale))
                    small_font = pygame.font.Font(None, int(36 * scale))
                elif res_1920_rect.collidepoint(mouse_pos):
                    settings['resolution'] = (1920, 1080)
                    screen = pygame.display.set_mode((1920, 1080))
                    # Rescale background
                    bg_image = pygame.image.load("main_menu_img/background_img/1920x1080_background.png")
                    bg_image = pygame.transform.scale(bg_image, (1920, 1080))
                    # Recreate all buttons with new scaling
                    create_buttons()
                    # Recreate slider and fonts with new scaling
                    scale = get_scale_factor()
                    volume_slider = Slider(int(400 * scale), int(200 * scale), int(400 * scale), int(20 * scale), 0.0, 1.0, settings['volume'])
                    font = pygame.font.Font(None, int(48 * scale))
                    small_font = pygame.font.Font(None, int(36 * scale))
        
        # Update volume setting
        settings['volume'] = volume_slider.get_value()
        pygame.mixer.music.set_volume(settings['volume'])
        
        pygame.display.flip()
        clock.tick(60)
    
    return

def credits():
    pass
#Function call for starting the game
main_menu()