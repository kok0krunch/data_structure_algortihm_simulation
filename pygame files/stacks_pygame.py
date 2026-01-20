import pygame

class Stack:
    def __init__(self):
        self.items = [] # List to hold stack items
        
    def push(self, item):
        self.items.append(item) # Add item to the list 
        
    def pop(self): # Remove item from the top of the stack
        if not self.is_empty():
            return self.items.pop() 
        return None
        
    def is_empty(self): # Check if list is empty
        return len(self.items) == 0 
        
    def size(self): # Number of items in the stack
        return len(self.items) 
        
    def peek(self): # Return the top item without removing it
        if not self.is_empty():
            return self.items[-1]
        return None

class ParkingGarageVisualizer:
    def __init__(self, screen_width=1400, screen_height=1000):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.parking_stack = Stack()
        self.temp_stack = Stack()  # Temporary stack for displaced cars
        self.car_log = {}
        self.max_capacity = 10  # Fixed capacity
        
        # UI State
        self.input_plate = ""
        self.message = ""
        self.message_timer = 0
        
        # Fonts - Using bold system font with larger sizes
        self.font = pygame.font.SysFont("couriernew", 44)
        self.small_font = pygame.font.SysFont("couriernew", 28)
        self.large_font = pygame.font.SysFont("couriernew", 56)
        self.title_font = pygame.font.SysFont("couriernew", 64)
        self.table_font = pygame.font.SysFont("couriernew", 26)
        
        # Load car image
        img_path = pygame.image.load("images\stacks_images\cat_car_img.png").convert_alpha()
        self.car_img = pygame.transform.scale(img_path, (100, 70))
        
    
    def draw_car_with_label(self, screen, x, y, plate):
        """Draw car image with plate label on the right side"""
        if self.car_img:
            screen.blit(self.car_img, (x, y))
        
        # Draw plate label to the right of the car
        plate_label = pygame.font.SysFont("couriernew", 22, bold=True).render(plate, True, (0, 0, 0))
        label_x = x + 105  # Position to the right of the car image
        label_y = y + 12
        screen.blit(plate_label, (label_x, label_y))
    
    def draw_garage_left(self, screen):
        """Draw main parking lot stack"""
        # Main Stack (Left side) - Centered
        garage_x = 210
        garage_y = 145
        garage_width = 550
        garage_height = 630
        
        # Draw main garage frame
        pygame.draw.rect(screen, (240, 240, 240), (garage_x, garage_y, garage_width, garage_height))
        pygame.draw.rect(screen, (100, 100, 100), (garage_x, garage_y, garage_width, garage_height), 3)
# PURRKING LOT DETAILS       
        # Title (Centered)
        garage_title = pygame.font.SysFont("couriernew", 28, bold=True).render("PURR-KING LOT", True, (50, 50, 50))
        screen.blit(garage_title, (garage_x + garage_width // 2 - garage_title.get_width() // 2, garage_y + 8))
        
        # Capacity info
        capacity_text = pygame.font.SysFont("couriernew", 18).render(f"Capacity: {self.parking_stack.size()}/{self.max_capacity}", 
                                            True, (50, 50, 50))
        screen.blit(capacity_text, (garage_x + 15, garage_y + 32))
        
        # Draw parked cars (newest at top, oldest at bottom)
        slot_y = garage_y + 58
        slot_height = 45
        car_x = garage_x + (garage_width - 100) // 2  # Center the car horizontally
        
        if not self.parking_stack.is_empty():
            # Display in reverse order (newest first, at top)
            for i in range(len(self.parking_stack.items) - 1, -1, -1):
                plate = self.parking_stack.items[i]
                if slot_y + slot_height < garage_y + garage_height - 15:
                    # Draw car with label (centered)
                    self.draw_car_with_label(screen, car_x, slot_y + 3, plate)
                    
                    # Top label (only for newest car)
                    if i == len(self.parking_stack.items) - 1:
                        top_label = pygame.font.SysFont("couriernew", 18).render("(TOP)", True, (255, 0, 0))
                        screen.blit(top_label, (garage_x + garage_width - 55, slot_y + 12))
                    
                    slot_y += slot_height
        else:
            empty_text = pygame.font.SysFont("couriernew", 24, bold=True).render("No cars parked", True, (150, 150, 150))
            screen.blit(empty_text, (garage_x + garage_width // 2 - empty_text.get_width() // 2, garage_y + 300))
    
    def draw_controls_right(self, screen):
        """Draw input controls, buttons on the right side"""
        # Right panel - Centered next to parking garage
        right_x = 780
        right_y = 145
        panel_width = 410
        panel_height = 180
        
        # Panel background
        pygame.draw.rect(screen, (245, 245, 245), (right_x, right_y, panel_width, panel_height), 0)
        pygame.draw.rect(screen, (100, 100, 100), (right_x, right_y, panel_width, panel_height), 3)
# CAR OPERATIONS        
        # Title
        title = pygame.font.SysFont("couriernew", 26, bold=True).render("CAR OPERATIONS", True, (50, 50, 50))
        screen.blit(title, (right_x + 20, right_y + 10))
        
        # Plate input section
        plate_label = pygame.font.SysFont("couriernew", 22).render("Plate#:", True, (50, 50, 50))
        screen.blit(plate_label, (right_x + 20, right_y + 45))
        
        # Input box for plate
        plate_input_rect = pygame.Rect(right_x + 120, right_y + 42, 140, 32)
        pygame.draw.rect(screen, (255, 255, 255), plate_input_rect)
        pygame.draw.rect(screen, (0, 0, 0), plate_input_rect, 2)
        plate_input = pygame.font.SysFont("couriernew", 24, bold=True).render(self.input_plate.upper(), True, (0, 0, 0))
        screen.blit(plate_input, (right_x + 130, right_y + 47))
        
        # Buttons (horizontal row below input)
        button_width = 110
        button_height = 35
        button_y = right_y + 90
        button_spacing = 12
        
        # Arrive button
        arrive_rect = pygame.Rect(right_x + 20, button_y, button_width, button_height)
        pygame.draw.rect(screen, (100, 200, 100), arrive_rect)
        pygame.draw.rect(screen, (50, 150, 50), arrive_rect, 2)
        arrive_text = pygame.font.SysFont("couriernew", 20, bold=True).render("Arrive", True, (255, 255, 255))
        screen.blit(arrive_text, (arrive_rect.centerx - arrive_text.get_width() // 2,
                                 arrive_rect.centery - arrive_text.get_height() // 2))
        
        # Depart button
        depart_rect = pygame.Rect(right_x + 20 + button_width + button_spacing, button_y, button_width, button_height)
        pygame.draw.rect(screen, (200, 100, 100), depart_rect)
        pygame.draw.rect(screen, (150, 50, 50), depart_rect, 2)
        depart_text = pygame.font.SysFont("couriernew", 20, bold=True).render("Depart", True, (255, 255, 255))
        screen.blit(depart_text, (depart_rect.centerx - depart_text.get_width() // 2,
                                 depart_rect.centery - depart_text.get_height() // 2))
        
        # Clear button
        clear_rect = pygame.Rect(right_x + 20 + 2 * (button_width + button_spacing), button_y, button_width, button_height)
        pygame.draw.rect(screen, (150, 150, 150), clear_rect)
        pygame.draw.rect(screen, (100, 100, 100), clear_rect, 2)
        clear_text = pygame.font.SysFont("couriernew", 20, bold=True).render("Clear", True, (255, 255, 255))
        screen.blit(clear_text, (clear_rect.centerx - clear_text.get_width() // 2,
                                clear_rect.centery - clear_text.get_height() // 2))
        
        # Message display
        if self.message_timer > 0:
            msg = pygame.font.SysFont("couriernew", 22, bold=True).render(self.message, True, (0, 100, 0))
            screen.blit(msg, (right_x + 20, right_y + 145))
            self.message_timer -= 1
        
        return arrive_rect, depart_rect, clear_rect, plate_input_rect
    
    def draw_history_table(self, screen):
        """Draw the history table showing plate, arrive, depart counts below Car Operations"""
        table_x = 780
        table_y = 340
        table_width = 410
        table_height = 435
# CAR LOG TABLE       
        # Panel background
        pygame.draw.rect(screen, (245, 245, 245), (table_x, table_y, table_width, table_height), 0)
        pygame.draw.rect(screen, (100, 100, 100), (table_x, table_y, table_width, table_height), 2)
        
        # Title
        title = pygame.font.SysFont("couriernew", 20, bold=True).render("CAR LOG", True, (50, 50, 50))
        screen.blit(title, (table_x + table_width // 2 - title.get_width() // 2, table_y + 6))
        
        # Table headers
        header_y = table_y + 25
        col_x = [table_x + 12, table_x + 146, table_x + 278]
        col_width = [120, 120, 120]
        
        # Header boxes
        pygame.draw.rect(screen, (200, 200, 200), (col_x[0], header_y, col_width[0], 18))
        pygame.draw.rect(screen, (200, 200, 200), (col_x[1], header_y, col_width[1], 18))
        pygame.draw.rect(screen, (200, 200, 200), (col_x[2], header_y, col_width[2], 18))
        
        # Header text
        plate_header = pygame.font.SysFont("couriernew", 18).render("Plate", True, (0, 0, 0))
        arrive_header = pygame.font.SysFont("couriernew", 18).render("Arrive", True, (0, 0, 0))
        depart_header = pygame.font.SysFont("couriernew", 18).render("Depart", True, (0, 0, 0))

        screen.blit(plate_header, (col_x[0] + 35, header_y + 1))
        screen.blit(arrive_header, (col_x[1] + 27, header_y + 1))
        screen.blit(depart_header, (col_x[2] + 27, header_y + 1))
        
        # Table rows
        row_y = header_y + 20
        row_height = 20
        max_rows = 20
        
        for i, (plate, [arrivals, departures]) in enumerate(self.car_log.items()):
            if i >= max_rows:
                break
            
            # Alternating row colors
            if i % 2 == 0:
                pygame.draw.rect(screen, (255, 255, 255), (table_x + 12, row_y, table_width - 24, row_height))
            else:
                pygame.draw.rect(screen, (240, 240, 240), (table_x + 12, row_y, table_width - 24, row_height))
            
            # Row data (smaller font)
            plate_text = pygame.font.SysFont("couriernew", 20).render(plate, True, (0, 0, 0))
            arrive_text = pygame.font.SysFont("couriernew", 20).render(str(arrivals), True, (100, 150, 100))
            depart_text = pygame.font.SysFont("couriernew", 20).render(str(departures), True, (200, 100, 100))
            
            screen.blit(plate_text, (col_x[0] + 12, row_y))
            screen.blit(arrive_text, (col_x[1] + 40, row_y))
            screen.blit(depart_text, (col_x[2] + 45, row_y))
            
            row_y += row_height
        
        # Border
        pygame.draw.rect(screen, (100, 100, 100), (table_x + 12, header_y + 18, table_width - 24, max_rows * row_height), 2)
    
    def arrive(self, plate):
        """Add a car to the garage"""
        if not plate:
            self.message = "Please enter a license plate"
            self.message_timer = 60
            return
        
        if self.parking_stack.size() >= self.max_capacity:
            self.message = f"Garage is FULL! {self.parking_stack.size()}/{self.max_capacity}"
            self.message_timer = 80
            return
        
        plate = plate.upper()
        self.parking_stack.push(plate)
        
        if plate not in self.car_log:
            self.car_log[plate] = [0, 0]
        self.car_log[plate][0] += 1
        
        self.message = f"Car {plate} arrived!"
        self.message_timer = 80
        self.input_plate = ""
    
    def depart(self, plate):
        """Remove a car from the garage"""
        if not plate:
            self.message = "Please enter a license plate"
            self.message_timer = 60
            return
        
        if self.parking_stack.is_empty():
            self.message = "Garage is empty!"
            self.message_timer = 80
            return
        
        plate = plate.upper()
        found = False
        temp_cars = []
        
        # Search for the car and move cars above it temporarily
        while not self.parking_stack.is_empty():
            current_car = self.parking_stack.pop()
            if current_car == plate:
                # Car found and removed
                if plate not in self.car_log:
                    self.car_log[plate] = [0, 0]
                self.car_log[plate][1] += 1
                
                # Remove from car log if depart count equals arrival count
                if self.car_log[plate][1] >= self.car_log[plate][0]:
                    del self.car_log[plate]
                
                self.message = f"Car {plate} departed!"
                found = True
                
                # Log temporary cars as departed, then arrived again
                for car in temp_cars:
                    if car not in self.car_log:
                        self.car_log[car] = [0, 0]
                    self.car_log[car][1] += 1  # Log as departed
                
                # Put remaining cars back and log as arrived again
                for car in reversed(temp_cars):
                    self.parking_stack.push(car)
                    if car not in self.car_log:
                        self.car_log[car] = [0, 0]
                    self.car_log[car][0] += 1  # Log as arrived again
                
                break
            else:
                # Store cars above the target
                temp_cars.append(current_car)
        
        if not found:
            # Car not found, restore all cars
            for car in reversed(temp_cars):
                self.parking_stack.push(car)
            self.message = f"Car {plate} not found!"
        
        self.message_timer = 80
        self.input_plate = ""
    
    def handle_event(self, event, arrive_rect=None, depart_rect=None, clear_rect=None, plate_input_rect=None):
        """Handle keyboard and mouse input"""
        if event.type == pygame.KEYDOWN:
            # Handle keyboard input for plate number
            if event.key == pygame.K_BACKSPACE:
                # Delete last character
                self.input_plate = self.input_plate[:-1]
            elif event.key == pygame.K_RETURN:
                # Press Enter to arrive (if plate is entered)
                if self.input_plate and arrive_rect:
                    self.arrive(self.input_plate)
            else:
                # Add character (letters and numbers only, max 10 chars)
                if len(self.input_plate) < 10:
                    if event.unicode.isalnum():
                        self.input_plate += event.unicode.upper()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Click on input box to focus it
            if plate_input_rect and plate_input_rect.collidepoint(event.pos):
                pass  # Input box is now focused, keyboard will work
            elif arrive_rect and arrive_rect.collidepoint(event.pos):
                if self.input_plate:
                    self.arrive(self.input_plate)
            elif depart_rect and depart_rect.collidepoint(event.pos):
                if self.input_plate:
                    self.depart(self.input_plate)
            elif clear_rect and clear_rect.collidepoint(event.pos):
                self.parking_stack = Stack()
                self.car_log = {}
                self.message = "Garage cleared!"
                self.message_timer = 60
                self.input_plate = ""

def stacks_menu(screen, clock, globalbg_img, back_btn):
    """Stacks menu function - Parking Garage Simulation"""
    running = True
    visualizer = ParkingGarageVisualizer(screen.get_width(), 1000)  # Fixed height to 1000
    
    while running:
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            # Garage operation screen
            visualizer.draw_garage_left(screen)
            arrive_rect, depart_rect, clear_rect, plate_input_rect = visualizer.draw_controls_right(screen)
            visualizer.draw_history_table(screen)
            visualizer.handle_event(event, arrive_rect, depart_rect, clear_rect, plate_input_rect)

        # Show background
        screen.blit(globalbg_img, (0, 0))

# PURRKING GARAGE VISUALIZER
        # Draw main title at the top
        title_font = pygame.font.SysFont("couriernew", 60, bold=True)
        main_title = title_font.render("The Purr-king Garage (Stacks)", True, (50, 50, 50))
        screen.blit(main_title, (visualizer.screen_width // 2 - main_title.get_width() // 2, 30))

        # Draw parking garage
        visualizer.draw_garage_left(screen)
        arrive_rect, depart_rect, clear_rect, plate_input_rect = visualizer.draw_controls_right(screen)
        visualizer.draw_history_table(screen)

        # Draw back button
        if back_btn.draw():
            running = False

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    return True
