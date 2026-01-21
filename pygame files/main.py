# import pygame module
import pygame
import os
from stacks_pygame import stacks_menu
from queue_pygame import queue_menu
from bt_pygame import bt_menu
from bst_pygame import bst_menu
#from recursion_pygame import recursion_menu

# pygame setup
pygame.mixer.pre_init(22050, -16, 1, 16)  # Lower frequency, mono, smallest buffer
pygame.init()

# Get the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Load audio files
audio_dir = os.path.join(script_dir, "..", "audio")
bgm_path = os.path.join(audio_dir, "bgm_music.flac")
click_sfx_path = os.path.join(audio_dir, "click_sfx.mp3")

print(f"Loading background music from: {os.path.abspath(bgm_path)}")
print(f"Loading click sound from: {os.path.abspath(click_sfx_path)}")

# Load and play background music
try:
    pygame.mixer.music.load(bgm_path)
    pygame.mixer.music.set_volume(0.5)  # Set volume to 50%
    pygame.mixer.music.play(-1)  # Loop indefinitely
    print("Background music loaded and playing successfully!")
except Exception as e:
    print(f"Error loading background music: {e}")

# Load click sound effect
try:
    click_sound = pygame.mixer.Sound(click_sfx_path)
    click_sound.set_volume(0.7)  # Set volume to 70%
    # Reserve a dedicated channel for click sounds
    pygame.mixer.set_num_channels(8)
    click_channel = pygame.mixer.Channel(0)  # Dedicated channel for clicks
    print("Click sound loaded successfully!")
except Exception as e:
    print(f"Error loading click sound: {e}")
    click_sound = None
    click_channel = None

screen = pygame.display.set_mode((1366, 768))
clock = pygame.time.Clock()

""" load images """

# start elements
activities_img = pygame.image.load("images/menu_images/activities_img.png").convert_alpha()
bst_img = pygame.image.load("images/menu_images/bst_img.png")
bt_img = pygame.image.load("images/menu_images/bt_img.png")
queue_img = pygame.image.load("images/menu_images/queue_img.png")
recursion_img = pygame.image.load("images/menu_images/recursion_img.png")
stacks_img = pygame.image.load("images/menu_images/stacks_img.png")
back_img = pygame.image.load("images/menu_images/back_img.png")

# main menu elements
start_img = pygame.image.load("images/menu_images/start_img.png")
exit_img = pygame.image.load("images/menu_images/exit_img.png")
gametitle_img = pygame.image.load("images/menu_images/gametitle_img.png").convert_alpha()

# game background image
globalbg_img = pygame.image.load("images/menu_images/globalbg_img.jpg")
globalbg_img= pygame.transform.scale(globalbg_img,(1366, 768))  # scale image to fit the game window

""" class for button functionality """

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.original_image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.hover_scale = 1.0
        self.target_scale = 1.0
    
    def draw(self):
        action = False
        #get mouse position
        mouse_pos = pygame.mouse.get_pos()
        
        #check mouse hover and clicked conditions
        if self.rect.collidepoint(mouse_pos):
            self.target_scale = 1.1  # Scale up on hover
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                # Play click sound effect IMMEDIATELY before anything else
                if click_sound and click_channel:
                    click_channel.play(click_sound)
                self.clicked = True
                action = True
        else:
            self.target_scale = 1.0  # Normal scale
        
        # Smooth scaling animation
        self.hover_scale += (self.target_scale - self.hover_scale) * 0.2
        
        # Apply hover effect
        if abs(self.hover_scale - 1.0) > 0.01:
            new_width = int(self.original_image.get_width() * self.hover_scale)
            new_height = int(self.original_image.get_height() * self.hover_scale)
            self.image = pygame.transform.scale(self.original_image, (new_width, new_height))
            # Center the scaled image
            offset_x = (self.original_image.get_width() - new_width) // 2
            offset_y = (self.original_image.get_height() - new_height) // 2
            draw_x = self.rect.x - offset_x
            draw_y = self.rect.y - offset_y
        else:
            self.image = self.original_image
            draw_x = self.rect.x
            draw_y = self.rect.y
        
        # always reset clicked state when mouse button is released
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        #draw button on screen with hover effect
        screen.blit(self.image, (draw_x, draw_y))

        return action

def wait_for_mouse_release():
    # Prevent click-through when switching screens by waiting until the
    # left mouse button is released. Also pump events to keep window responsive.
    while pygame.mouse.get_pressed()[0]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
        clock.tick(60)

""" instanstiated buttons """

# main menu options buttons
start_btn = Button(200, 550, start_img, 0.7)
exit_btn = Button(720, 550, exit_img, 0.7)

# start options buttons
back_btn = Button(0, 0, back_img, 0.2)
stacks_btn = Button(0, 450, stacks_img, 0.7)
queue_btn = Button(470, 450, queue_img, 0.7)
bt_btn = Button(945, 450, bt_img, 0.7)
bst_btn = Button(220, 600, bst_img, 0.7)
recursion_btn = Button(710, 600, recursion_img, 0.7)


"""" main game loop """

def main_menu():
    running = True
    # Animation variables
    start_time = pygame.time.get_ticks()
    animation_duration = 1000  # 1 second in milliseconds
    
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Calculate animation progress (0.0 to 1.0)
        elapsed_time = pygame.time.get_ticks() - start_time
        animation_progress = min(elapsed_time / animation_duration, 1.0)
        
        # show global background image
        screen.blit(globalbg_img, (0, 0))
        
        # Apply fade-in effect to title
        title_surface = gametitle_img.copy()
        title_surface.set_alpha(int(255 * animation_progress))
        screen.blit(title_surface, (380, -60))

        # RENDER YOUR GAME HERE
        if animation_progress >= 0.5:  # Buttons start appearing halfway through
            button_alpha = int(255 * ((animation_progress - 0.5) * 2))
            
            # Create temporary surfaces with alpha for buttons
            start_temp = pygame.Surface(start_btn.original_image.get_size(), pygame.SRCALPHA)
            start_temp.blit(start_btn.original_image, (0, 0))
            start_temp.set_alpha(button_alpha)
            
            exit_temp = pygame.Surface(exit_btn.original_image.get_size(), pygame.SRCALPHA)
            exit_temp.blit(exit_btn.original_image, (0, 0))
            exit_temp.set_alpha(button_alpha)
            
            # Temporarily set button images to faded versions during animation
            if animation_progress < 1.0:
                start_btn.original_image.set_alpha(button_alpha)
                exit_btn.original_image.set_alpha(button_alpha)
            else:
                start_btn.original_image.set_alpha(255)
                exit_btn.original_image.set_alpha(255)
            
            if start_btn.draw():
                wait_for_mouse_release()
                if start_menu() == False:
                    running = False
                # Reset animation for returning to main menu
                start_time = pygame.time.get_ticks()
                
            if exit_btn.draw():
                wait_for_mouse_release()
                running = False

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()

def start_menu():
    running = True
    # Animation variables
    start_time = pygame.time.get_ticks()
    animation_duration = 1000  # 1 second in milliseconds
    
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        # Calculate animation progress (0.0 to 1.0)
        elapsed_time = pygame.time.get_ticks() - start_time
        animation_progress = min(elapsed_time / animation_duration, 1.0)
        
        # show global background image
        screen.blit(globalbg_img, (0, 0))
        
        # Apply fade-in effect to activities title
        activities_surface = activities_img.copy()
        activities_surface.set_alpha(int(255 * animation_progress))
        screen.blit(activities_surface, (380, -60))

        # RENDER YOUR GAME HERE
        if animation_progress >= 0.3:  # Back button appears early
            back_alpha = int(255 * min((animation_progress - 0.3) * 1.43, 1.0))
            back_btn.original_image.set_alpha(back_alpha if animation_progress < 1.0 else 255)
            
            if back_btn.draw():  # Back Button
                wait_for_mouse_release()
                running = False

        if animation_progress >= 0.5:  # Activity buttons start appearing
            button_alpha = int(255 * ((animation_progress - 0.5) * 2))
            
            if animation_progress < 1.0:
                stacks_btn.original_image.set_alpha(button_alpha)
                queue_btn.original_image.set_alpha(button_alpha)
                bt_btn.original_image.set_alpha(button_alpha)
                bst_btn.original_image.set_alpha(button_alpha)
                recursion_btn.original_image.set_alpha(button_alpha)
            else:
                stacks_btn.original_image.set_alpha(255)
                queue_btn.original_image.set_alpha(255)
                bt_btn.original_image.set_alpha(255)
                bst_btn.original_image.set_alpha(255)
                recursion_btn.original_image.set_alpha(255)
            
            if stacks_btn.draw():  # Stacks Button
                wait_for_mouse_release()
                if stacks_menu(screen, clock, globalbg_img, back_btn) == False:
                    return False
                start_time = pygame.time.get_ticks()  # Reset animation
                
            if queue_btn.draw():  # Queue Button
                wait_for_mouse_release()
                if queue_menu(screen, clock, globalbg_img, back_btn) == False:
                    return False
                start_time = pygame.time.get_ticks()  # Reset animation
                
            if bt_btn.draw():  # Binary Tree Button
                wait_for_mouse_release()
                if bt_menu(screen, clock, globalbg_img, back_btn) == False:
                    return False
                start_time = pygame.time.get_ticks()  # Reset animation
                
            if bst_btn.draw():  # Binary Search Tree Button
                wait_for_mouse_release()
                if bst_menu(screen, clock, globalbg_img, back_btn) == False:
                    return False
                start_time = pygame.time.get_ticks()  # Reset animation
                
            if recursion_btn.draw():  # Recursion Button
                wait_for_mouse_release()
                if recursion_menu(screen, clock, globalbg_img, back_btn) == False:
                    return False
                start_time = pygame.time.get_ticks()  # Reset animation

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    return True

# start game function call
main_menu()