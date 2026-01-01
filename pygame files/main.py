# import pygame module
import pygame
from stacks_pygame import stacks_menu
from queue_pygame import queue_menu
from bt_pygame import bt_menu
from bst_pygame import bst_menu
from recursion_pygame import recursion_menu

# pygame setup
pygame.init()

screen = pygame.display.set_mode((1366, 768))
clock = pygame.time.Clock()

""" load images """

# start elements
activities_img = pygame.image.load("images/activities_img.png").convert_alpha()
bst_img = pygame.image.load("images/bst_img.png")
bt_img = pygame.image.load("images/bt_img.png")
queue_img = pygame.image.load("images/queue_img.png")
recursion_img = pygame.image.load("images/recursion_img.png")
stacks_img = pygame.image.load("images/stacks_img.png")
back_img = pygame.image.load("images/back_img.png")

# main menu elements
start_img = pygame.image.load("images/start_img.png")
exit_img = pygame.image.load("images/exit_img.png")
gametitle_img = pygame.image.load("images/gametitle_img.png").convert_alpha()

# game background image
globalbg_img = pygame.image.load("images/globalbg_img.jpg")
globalbg_img= pygame.transform.scale(globalbg_img,(1366, 768))  # scale image to fit the game window

""" class for button functionality """

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
back_btn = Button(0, 0, back_img, 0.4)
stacks_btn = Button(0, 450, stacks_img, 0.7)
queue_btn = Button(470, 450, queue_img, 0.7)
bt_btn = Button(945, 450, bt_img, 0.7)
bst_btn = Button(220, 600, bst_img, 0.7)
recursion_btn = Button(710, 600, recursion_img, 0.7)


"""" main game loop """

def main_menu():
    running = True
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # show global background image
        screen.blit(globalbg_img)
        screen.blit(gametitle_img, (380, -60))  # the offset is -125 for y coordinate

        # RENDER YOUR GAME HERE
        if start_btn.draw():
            wait_for_mouse_release()
            if start_menu() == False:
                running = False
        if exit_btn.draw():
            wait_for_mouse_release()
            running = False

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()

def start_menu():
    running = True
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        # show global background image
        screen.blit(globalbg_img)
        screen.blit(activities_img, (380, -60))  # the offset is -125 for y coordinate

        # RENDER YOUR GAME HERE
        if back_btn.draw():  # Back Button
            wait_for_mouse_release()
            running = False

        if stacks_btn.draw():  # Stacks Button
            wait_for_mouse_release()
            if stacks_menu(screen, clock, globalbg_img, back_btn) == False:
                return False
            
        if queue_btn.draw():  # Queue Button
            wait_for_mouse_release()
            if queue_menu(screen, clock, globalbg_img, back_btn) == False:
                return False
            
        if bt_btn.draw():  # Binary Tree Button
            wait_for_mouse_release()
            if bt_menu(screen, clock, globalbg_img, back_btn) == False:
                return False
            
        if bst_btn.draw():  # Binary Search Tree Button
            wait_for_mouse_release()
            if bst_menu(screen, clock, globalbg_img, back_btn) == False:
                return False
            
        if recursion_btn.draw():  # Recursion Button
            wait_for_mouse_release()
            if recursion_menu(screen, clock, globalbg_img, back_btn) == False:
                return False

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    return True

# start game function call
main_menu()