import pygame
import sys
import time 

pygame.init()

screen = pygame.display.set_mode((800,400))
clock = pygame.time.Clock()

menu_bg = pygame.image.load("images\menu_images\globalbg_img.jpg").convert()
menu_bg = pygame.transform.scale(menu_bg, (900, 500))
base_width = 100
width_step = 40
peg_height = 280
disk_height = 35
move_delay = 0.6
rainbow_colors = [(255, 102, 102), (255, 178, 102), (255, 255, 153), (153, 255, 153),
                  (153, 204, 255), (178, 102, 255), (255, 153, 255)]

screen_width = 1370
screen_height = 810
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
            center_x = x + width // 2
            center_y = y + disk_height // 2
            
            # Body of the Cat
            pygame.draw.rect(screen, color, (x, y, width, disk_height))
            
            # Cat Ears (Triangles)
            ear_size = 18
            pygame.draw.polygon(screen, color, [(x, y), (x + ear_size, y), (x + ear_size // 2, y - ear_size)])
            pygame.draw.polygon(screen, color, [(x + width - ear_size, y), (x + width, y), (x + width - ear_size // 2, y - ear_size)])

            # Cat Eyes
            eye_offset_x = width // 4
            eye_radius = 5
            for side in [-1, 1]: # Left and Right eyes
                eye_x = center_x + (side * eye_offset_x)
                pygame.draw.circle(screen, (40, 40, 40), (eye_x, center_y - 2), eye_radius) # Black part
                pygame.draw.circle(screen, (255, 255, 255), (eye_x + 2, center_y - 4), 2) # White reflection

            # Whiskers
            whisker_color = (100, 100, 100)
            whisker_len = 15
            for side in [-1, 1]: 
                start_x = center_x + (side * 8)
                for angle in [-3, 0, 3]: # Three whiskers at different tilts
                    pygame.draw.line(screen, whisker_color, 
                                     (start_x, center_y), 
                                     (start_x + (side * whisker_len), center_y + angle), 1)

            # Small Pink Nose
            pygame.draw.circle(screen, (255, 200, 200), (center_x, center_y + 2), 3)

def recursion_menu(screen, clock, globalbg_img, back_btn):
    """Menu function for Tower of Hanoi recursion simulation - Integrated Construction"""
    font = pygame.font.SysFont("couriernew", 32, bold=True)
    title_font = pygame.font.SysFont("couriernew", 60, bold=True)
    
    num_disks = 0
    origin = 0
    destination = 0
    stage = 0
    user_input = ""
    
    text_x = 1370 // 2
    text_y = 810 // 2
    
    hanoi = TowerOfHanoi()
    
    # USER INPUT LOOP
    while stage < 3:
        screen.blit(globalbg_img, (0, 0))
        draw_game_background(screen)
        
        title = title_font.render("Tower of Catnoi", True, (50, 50, 50))
        screen.blit(title, (1370 // 2 - title.get_width() // 2, 80))

        if back_btn.draw():
            return None # Go back to activity menu
        
        if stage == 0:
            text = "Enter number of disks (1-7): "
        elif stage == 1:
            text = "Enter origin tower (1,2,3): "
        else:
            text = "Enter destination tower (1,2,3): "

        text_surface = font.render(text + user_input, True, (0, 0, 0)) # using black
        text_rect = text_surface.get_rect(center=(text_x, text_y))
        screen.blit(text_surface, text_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_input:
                        val = int(user_input)
                        if stage == 0 and 1 <= val <= 7:
                            num_disks = val
                            stage += 1
                        elif stage == 1 and 1 <= val <= 3:
                            origin = val
                            stage += 1
                        elif stage == 2 and 1 <= val <= 3 and val != origin:
                            destination = val
                            stage += 1
                        user_input = ""
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.unicode.isdigit() and len(user_input) < 1:
                    user_input += event.unicode

        pygame.display.flip()
        clock.tick(60)

    # INITIALIZE SIMULATION DATA BASED ON USER INPUT
    towers = {1: list(range(num_disks, 0, -1)) if origin == 1 else [],
              2: list(range(num_disks, 0, -1)) if origin == 2 else [],
              3: list(range(num_disks, 0, -1)) if origin == 3 else []}

    # Solve recursion based on origin/destination logic
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

    # ANIMATION LOOP
    while True:
        screen.blit(globalbg_img, (0, 0))
        draw_game_background(screen)
        
        title = title_font.render("Tower of Catnoi", True, (50, 50, 50))
        screen.blit(title, (1370 // 2 - title.get_width() // 2, 80))
        
        draw_pegs(screen)
        draw_disks(screen, towers)
        
        if back_btn.draw():
            return True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        # Animation logic
        if move_index < len(hanoi.moves):
            if time.time() - last_move > move_delay:
                src, dst = hanoi.moves[move_index]
                disk = towers[src].pop()
                towers[dst].append(disk)
                move_index += 1
                last_move = time.time()
        else:
            success_msg = "All kittens are moved!"
            text_color = (255, 50, 50) 

            msg_y = 210  
            msg_x = 1370 // 2 - font.size(success_msg)[0] // 2

            success_text = font.render(success_msg, True, text_color)
            screen.blit(success_text, (msg_x, msg_y))

        pygame.display.flip()
        clock.tick(60)