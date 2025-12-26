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

    if choice == '1':
            if parking.size() < max_capacity:
                car = input("Enter car license plate: ").strip().upper()
                parking.push(car)
                car_log[car] = car_log.get(car, [0, 0])
                car_log[car][0] += 1
                print(f"✅ Car {car} arrived!")
                display_log()
            else:
                print("❌ Parking garage is full!")
    
    elif choice == '2':
        if not parking.is_empty():
            car = input("Enter car license plate to depart: ").strip().upper()
            temp_cars = []
            found = False
            while not parking.is_empty():
                current_car = parking.pop()
                if current_car == car:
                    car_log[car][1] += 1
                    print(f"✓ Car {car} departed!")
                    found = True
                    break
                temp_cars.append(current_car)
            if found:
                for temp_car in reversed(temp_cars):
                    car_log[temp_car][0] += 1
                    parking.push(temp_car)
            else:
                for temp_car in temp_cars:
                    parking.push(temp_car)
                print(f"✗ Car {car} not found in garage!")
            display_log()
        else:
            print("❌ Garage is empty!")
            
    elif choice == '3':
        print("\n" + "=" * 40)
        print("CARS IN GARAGE:")
        print("=" * 40)
        if parking.is_empty():
            print("(Empty)")
        else:
            for i, car in enumerate(reversed(parking.items), 1):
                print(f"{car}")
        print(f"\nCapacity: {parking.size()}/{max_capacity}")
        print("=" * 40)
    
    elif choice == '4':
        print("Goodbye!")
        break
    
    else:
        print("Invalid choice. Please enter 1-4.")