import pygame
import sys
import time 

pygame.init()

screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Tower of Hanoi')
clock = pygame.time.Clock()
max_disks = 7
peg_y_placement = 120
peg_x_placement = { 1: 250, 2: 450, 3: 650}
black = (0, 0, 0)
blue = (100, 149, 237)
white = (250, 250, 250)
move_delay = 0.6
peg_img = pygame.image.load("images/peg_img.png").convert_alpha()
disk_img = pygame.image.load("images/disk_img.png").convert_alpha()

class TowerOfHanoi:
    def __init__(self):
        self.tower_1 = 1
        self.tower_2 = 2
        self.tower_3 = 3
        self.moves = []


    # Functions for solving Tower of Hanoi using recursion
    def tower_one_to_tower_two(self, user_input, tower_1, tower_2, tower_3):
        if user_input == 0:
            return
        self.tower_one_to_tower_two(int(user_input) - 1, tower_1, tower_3, tower_2)
        self.moves.append((tower_1, tower_2))
        self.tower_one_to_tower_two(int(user_input) - 1, tower_3, tower_2, tower_1)

    def tower_one_to_tower_three(self, user_input, tower_1, tower_2, tower_3):
        if user_input == 0:
            return
        
        self.tower_one_to_tower_three(int(user_input) - 1, tower_1, tower_3, tower_2)
        self.moves.append((tower_1, tower_3))
        self.tower_one_to_tower_three(int(user_input) - 1, tower_2, tower_1, tower_3)

    def tower_two_to_tower_one(self, user_input, tower_2, tower_3, tower_1):
        if user_input == 0:
            return
        
        self.tower_two_to_tower_one(int(user_input) - 1, tower_2, tower_1, tower_3)
        self.moves.append((tower_2, tower_1))
        self.tower_two_to_tower_one(int(user_input) - 1, tower_3, tower_2, tower_1)

    def tower_two_to_tower_three(self, user_input, tower_2, tower_1, tower_3):
        if user_input == 0:
            return
        self.tower_two_to_tower_three(int(user_input) - 1, tower_2, tower_3, tower_1)
        self.moves.append((tower_2, tower_3))
        self.tower_two_to_tower_three(int(user_input) - 1, tower_1, tower_2, tower_3)

    def tower_three_to_tower_one(self, user_input, tower_3, tower_2, tower_1):
        if user_input == 0:
            return
        self.tower_three_to_tower_one(int(user_input) - 1, tower_3, tower_1, tower_2)
        self.moves.append((tower_3, tower_1))
        self.tower_three_to_tower_one(int(user_input) - 1, tower_2, tower_3, tower_1)

    def tower_three_to_tower_two(self, user_input, tower_3, tower_1, tower_2):
        if user_input == 0:
            return
        self.tower_three_to_tower_two(int(user_input) - 1, tower_3, tower_2, tower_1)
        self.moves.append((tower_3, tower_2))
        self.tower_three_to_tower_two(int(user_input) - 1, tower_1, tower_3, tower_2)

def draw_pegs(screen):
    peg_width = 60
    peg_height = 280
    peg_dimensions = pygame.transform.scale(peg_img, peg_width, peg_height)
    for x in peg_x_placement.values():
        screen.blit(peg_img, (x - peg_img.get_width() // 2, 120))

def draw_disks(screen, towers):
    disk_images = {}
    base_width = 60
    width_step = 25
    disk_height = disk_img.get_height()

    for disk in range(1, max_disks + 1):
        width = base_width + (disk - 1) * width_step
        disk_images[disk] = pygame.transform.scale(disk_img,(width, disk_height))

    for peg, disks in towers.items():
        for i, disk in enumerate(disks):
            img = disk_images[disk]
            peg_x = peg_x_placement[peg] - peg_img.get_width() // 2
            peg_y = peg_y_placement - (i+1) * img.get_height()
            screen.blit(img, (peg_x, peg_y))
