# Stack implementation
# Implement push, pop, is_empty, size, and peek methods

class Stack:
    def __init__(self):
        self.items = []
        
    def push(self, item):
        self.items.append(item)
        
    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None
        
    def is_empty(self):
        return len(self.items) == 0
        
    def size(self):
        return len(self.items)
        
    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None

# Parking garage program
print("Welcome to the Parking Garage System!")
while True:
    max_capacity = int(input("Enter parking capacity (minimum of 5): "))
    if max_capacity >= 5:
        break
    print("Capacity must be at least 5!")
    
parking = Stack()
car_log = {}