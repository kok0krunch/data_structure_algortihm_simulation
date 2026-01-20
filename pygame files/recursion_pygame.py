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
peg_img = pygame.image.load("images/menu_images/peg_img.png").convert_alpha()
disk_img = pygame.image.load("images/menu_images/disk_img.png").convert_alpha()

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

def main():
    screen = pygame.display.set_mode((900, 500))
    pygame.display.set_caption("Tower of Hanoi")

    font = pygame.font.SysFont(None, 32)

    num_disks = 0
    origin = 0
    destination = 0
    stage = 0
    user_input = ""

    while stage < 3:
        screen.fill(white)

        if stage == 0:
            text = font.render("Enter number of disks (1-7): " + user_input, True, black)
        elif stage == 1:
            text = font.render("Enter origin tower (1,2,3): " + user_input, True, black)
        else:
            text = font.render("Enter destination tower (1,2,3): " + user_input, True, black)

        draw_pegs(screen)
        draw_disks(screen, towers)

        screen.blit(text, (50, 200))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if stage == 0:
                        num_disks = int(user_input)
                        if 1 <= num_disks <= max_disks:
                            stage += 1
                            user_input = ""
                    elif stage == 1:
                            origin = int(user_input)
                            stage += 1
                            user_input = ""
                    else:
                        destination = int(user_input)
                        stage += 1
                elif event.unicode.isdigit():
                    user_input += event.unicode

    towers = {1: list(range(num_disks, 0, -1)) if origin == 1 else [],2: list(range(num_disks, 0, -1)) if origin == 2 else [],
        3: list(range(num_disks, 0, -1)) if origin == 3 else []}

    hanoi = TowerOfHanoi()

    if origin == 1 and destination == 2:
        hanoi.tower_one_to_tower_two(num_disks, 1, 2, 3)
    elif origin == 1 and destination == 3:
        hanoi.tower_one_to_tower_three(num_disks, 1, 2, 3)
    elif origin == 2 and destination == 1:
        hanoi.tower_two_to_tower_one(num_disks, 2, 3, 1)
    elif origin == 2 and destination == 3:
        hanoi.tower_two_to_tower_three(num_disks, 2, 1, 3)
    elif origin == 3 and destination == 1:
        hanoi.tower_three_to_tower_one(num_disks, 3, 2, 1)
    elif origin == 3 and destination == 2:
        hanoi.tower_three_to_tower_two(num_disks, 3, 1, 2)

    move_index = 0
    last_move = time.time()
    clock = pygame.time.Clock()

    while True:
        screen.fill((250, 250, 250))
        draw_pegs(screen)
        draw_disks(screen, towers)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if move_index < len(hanoi.moves):
            if time.time() - last_move > move_delay:
                src, dst = hanoi.moves[move_index]
                disk = towers[src].pop()
                towers[dst].append(disk)
                move_index += 1
                last_move = time.time()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
