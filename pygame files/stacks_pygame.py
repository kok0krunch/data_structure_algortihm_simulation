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
    
def stacks_menu(screen, clock, globalbg_img, back_btn):
    """Stacks menu function"""
    running = True
    while running:
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        # show global background image
        screen.blit(globalbg_img, (0, 0))

        # RENDER YOUR STACKS CONTENT HERE

        # Draw back button
        if back_btn.draw():
            running = False

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    return True
