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

def display_log():
    print("\n" + "=" * 40)
    print(f"{'LICENSE PLATE':<15} {'ARRIVALS':<10} {'DEPARTURES':<10}")
    print("=" * 40)
    for car, [arrivals, departures] in car_log.items():
        print(f"{car:<15} {arrivals:<10} {departures:<10}")
    print("=" * 40)
    
def display_menu():
    print("\n========= PARKING GARAGE SYSTEM =========")
    print("1. Arrive")
    print("2. Depart")
    print("3. View garage")
    print("4. Exit")
    
while True:
    display_menu()
    try:
        choice = input("\nChoose an option (1-4): ").strip()
    except ValueError:
        print("Invalid input. Please enter a number from 1 to 4.")
        continue