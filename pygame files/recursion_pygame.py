import pygame
import sys
import time 

pygame.init()

# Images
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
