import pygame

pygame.init()

# Images
background_img = pygame.image.load
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Tower of Hanoi')
clock = pygame.time.Clock()

class TowerOFHanoi:
    def __init__(self, tower_1, tower_2, tower_3):
        self.tower_1 = 1
        self.tower_2 = 2
        self.tower_3 = 3



    # Functions for solving Tower of Hanoi using recursion
    def tower_one_to_tower_two(self, user_input, tower_1, tower_2, tower_3):
        if user_input == 0:
            return
        self.tower_one_to_tower_two(int(user_input) - 1, tower_1, tower_3, tower_2)
        print("Move disk", user_input, "from", tower_1, "to", tower_2)
        self.tower_one_to_tower_two(int(user_input) - 1, tower_3, tower_2, tower_1)

    def tower_one_to_tower_three(self, user_input, tower_1, tower_2, tower_3):
        if user_input == 0:
            return
        
        self.tower_one_to_tower_three(int(user_input) - 1, tower_1, tower_3, tower_2)
        print('Move disk', user_input, 'from', tower_1, 'to', tower_3)
        self.tower_one_to_tower_three(int(user_input) - 1, tower_2, tower_1, tower_3)

    def tower_two_to_tower_one(self, user_input, tower_2, tower_3, tower_1):
        if user_input == 0:
            return
        
        self.tower_two_to_tower_one(int(user_input) - 1, tower_2, tower_1, tower_3)
        print("Move disk", user_input, "from", tower_2, "to", tower_1)
        self.tower_two_to_tower_one(int(user_input) - 1, tower_3, tower_2, tower_1)

    def tower_two_to_tower_three(self, user_input, tower_2, tower_1, tower_3):
        if user_input == 0:
            return
        self.tower_two_to_tower_three(int(user_input) - 1, tower_2, tower_3, tower_1)
        print("Move disk", user_input, "from", tower_2, "to", tower_3)
        self.tower_two_to_tower_three(int(user_input) - 1, tower_1, tower_2, tower_3)

    def tower_three_to_tower_one(self, user_input, tower_3, tower_2, tower_1):
        if user_input == 0:
            return
        self.tower_three_to_tower_one(int(user_input) - 1, tower_3, tower_1, tower_2)
        print("Move disk", user_input, "from", tower_3, "to", tower_1)
        self.tower_three_to_tower_one(int(user_input) - 1, tower_2, tower_3, tower_1)

    def tower_three_to_tower_two(self, user_input, tower_3, tower_1, tower_2):
        if user_input == 0:
            return
        self.tower_three_to_tower_two(int(user_input) - 1, tower_3, tower_2, tower_1)
        print("Move disk", user_input, "from", tower_3, "to", tower_2)
        self.tower_three_to_tower_two(int(user_input) - 1, tower_1, tower_3, tower_2)

    def