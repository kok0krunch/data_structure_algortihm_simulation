import pygame
import sys
import time 

pygame.init()

screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Tower of Hanoi')
clock = pygame.time.Clock()

menu_bg = pygame.image.load("images\menu_images\globalbg_img.jpg").convert()
menu_bg = pygame.transform.scale(menu_bg, (900, 500))
base_width = 100
width_step = 40
peg_height = 280
disk_height = 35
move_delay = 0.6
rainbow_colors = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), 
                  (0, 0, 255), (75, 0, 130), (148, 0, 211)]
max_disks = 7
peg_y_placement = 320
peg_x_placement = { 1: 270, 2: 685, 3: 1100}
black = (0, 0, 0)
blue = (100, 149, 237)
white = (250, 250, 250)
move_delay = 0.6

def draw_game_background(screen):
    rect_width = 1250
    rect_height = 450
    rect_x = (1370 - rect_width) // 2
    rect_y = (810 - rect_height) // 2
    pygame.draw.rect(screen, white, (rect_x, rect_y, rect_width, rect_height))
    pygame.draw.rect(screen, black, (rect_x, rect_y, rect_width, rect_height), 3)

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
    for x in peg_x_placement.values():
        pygame.draw.rect(screen, black, (x -5, 300, 10, 300))

def draw_disks(screen, towers):
    peg_base = peg_y_placement + peg_height
    for peg_index, disks in towers.items():
            for i, disk in enumerate(disks):
                color = rainbow_colors[disk - 1]
                width = base_width + (disk - 1) * width_step
                x = peg_x_placement[peg_index] - width // 2
                y = peg_base - (i + 1) * disk_height
                pygame.draw.rect(screen, color, (x, y, width, disk_height))

def recursion_menu(screen, clock, globalbg_img, back_btn):
    """Menu function for Tower of Hanoi recursion simulation"""
    font = pygame.font.SysFont("couriernew", 32, bold=True)
    
    num_disks = 0
    origin = 0
    destination = 0
    stage = 0
    user_input = ""
    
    text_x = 1370 // 2
    text_y = 810 // 2
    
    while stage < 3:
        screen.blit(globalbg_img, (0, 0))
        draw_game_background(screen)
        
        if back_btn.draw():
            return None
        
        if stage == 0:
            text = "Enter number of disks (1-7): "
        elif stage == 1:
            text = "Enter origin tower (1,2,3): "
        else:
            text = "Enter destination tower (1,2,3): "

        text_surface = font.render(text + user_input, True, black)
        text_rect = text_surface.get_rect(center=(text_x, text_y))
        screen.blit(text_surface, text_rect)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if stage == 0:
                        if user_input and 1 <= int(user_input) <= max_disks:
                            num_disks = int(user_input)
                            stage += 1
                            user_input = ""
                    elif stage == 1:
                        if user_input and 1 <= int(user_input) <= 3:
                            origin = int(user_input)
                            stage += 1
                            user_input = ""
                    else:
                        if user_input and 1 <= int(user_input) <= 3:
                            destination = int(user_input)
                            stage += 1
                elif event.unicode.isdigit():
                    user_input += event.unicode
    
    # Run the simulation after getting user inputs
    towers = {1: list(range(num_disks, 0, -1)) if origin == 1 else [],
              2: list(range(num_disks, 0, -1)) if origin == 2 else [],
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

    while True:
        screen.blit(globalbg_img, (0, 0))
        draw_game_background(screen)
        draw_pegs(screen)
        draw_disks(screen, towers)
        
        if back_btn.draw():
            return True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        if move_index < len(hanoi.moves):
            if time.time() - last_move > move_delay:
                src, dst = hanoi.moves[move_index]
                disk = towers[src].pop()
                towers[dst].append(disk)
                move_index += 1
                last_move = time.time()

        pygame.display.flip()
        clock.tick(60)

def main():
    screen = pygame.display.set_mode((900, 500))
    pygame.display.set_caption("Tower of Hanoi")
    clock = pygame.time.Clock()
    
    globalbg_img = pygame.image.load("images/menu_images/globalbg_img.jpg").convert()
    globalbg_img = pygame.transform.scale(globalbg_img, (900, 500))
    
    back_btn = None  # Placeholder for back button if needed
    
    # Get user input from menu
    num_disks, origin, destination = recursion_menu(screen, clock, globalbg_img, back_btn)
    
    towers = {1: list(range(num_disks, 0, -1)) if origin == 1 else [],
              2: list(range(num_disks, 0, -1)) if origin == 2 else [],
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

    while True:
        screen.blit(globalbg_img, (0, 0))
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
