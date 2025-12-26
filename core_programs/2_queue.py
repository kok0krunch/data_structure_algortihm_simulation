#Queue Program Logic Python File
#Implement Table for license plate, number of arrival, number of departure, and who arrived and departed
#Implement a 4 Lane Parking Garage Simulation using Queue Data Structure
#Implement a Random License plate generator for cars arriving at the parking garage
import random
import string


class Queue:
    def __init__(self, lane_id):
        self.items = {}
        self.front = 0
        self.rear = 0
        self.lane_id = lane_id # Identity for this lane (e.g., 1, 2, 3, 4)

    def isEmpty(self):
        return self.rear == self.front

    def size(self):
        return self.rear - self.front

    def enqueue(self, item):
        self.items[self.rear] = item
        self.rear += 1

    def dequeue(self):
        if self.isEmpty():
            raise IndexError("Dequeue from empty queue")
        item = self.items[self.front]
        del self.items[self.front]
        self.front += 1
        return item

    def peek(self):
        if self.isEmpty():
            raise IndexError("Peek from empty queue")
        return self.items[self.front]


def generate_license_plate():
    """Generate a random license plate in format ABC-123"""
    letters = ''.join(random.choices(string.ascii_uppercase, k=3))
    numbers = ''.join(random.choices(string.digits, k=3))
    return f"{letters}-{numbers}"


def print_menu():
    print("\n" + "="*50)
    print("Parking Garage Queue Management")
    print("="*50)
    print("1. Park Car (Enqueue)")
    print("2. Depart Car (Dequeue)")
    print("3. View Parking Garage")
    print("4. Exit Parking Garage")
    print("="*50)


def display_parking_table(lanes):
    """Display formatted table with parking information"""
    print("\n" + "="*90)
    print(f"{'License Plate':<15} {'Arrival #':<12} {'Departure #':<15} {'Status':<45}")
    print("="*90)
    
    # Collect all cars from all lanes
    all_cars = []
    for lane_id, lane in enumerate(lanes, 1):
        for position, (index, car_data) in enumerate(lane.items.items()):
            status = f"Lane {lane_id} - {'Front' if position == 0 else f'Position {position}'}"
            all_cars.append({
                'plate': car_data['plate'],
                'arrival': car_data['arrival_num'],
                'departure': car_data.get('departure_num', '-'),
                'status': status
            })
    
    # Display departed cars first
    if hasattr(display_parking_table, 'departed_cars'):
        for car in display_parking_table.departed_cars:
            departure_str = str(car['departure_num']) if car['departure_num'] else '-'
            print(f"{car['plate']:<15} {car['arrival_num']:<12} {departure_str:<15} {'Departed':<45}")
    
    # Display parked cars
    for car in all_cars:
        departure_str = str(car['departure']) if car['departure'] != '-' else '-'
        print(f"{car['plate']:<15} {car['arrival']:<12} {departure_str:<15} {car['status']:<45}")
    
    print("="*90 + "\n")


def main():
    # Global counters
    arrival_counter = [0]  # Using list to allow modification in nested scope
    departure_counter = [0]
    
    # Initialize 4 parking lanes
    lanes = [Queue(i+1) for i in range(4)]
    
    # Store departed cars
    display_parking_table.departed_cars = []
    
    while True:
        print_menu()
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1':  # Park Car
            arrival_counter[0] += 1
            license_plate = generate_license_plate()
            
            # Find the lane with the most space
            best_lane = min(range(4), key=lambda i: lanes[i].size())
            
            car_data = {
                'plate': license_plate,
                'arrival_num': arrival_counter[0],
                'departure_num': None
            }
            
            lanes[best_lane].enqueue(car_data)
            print(f"\n✓ Car {license_plate} parked successfully in Lane {best_lane + 1}")
            print(f"  Arrival #: {arrival_counter[0]}")
        
        elif choice == '2':  # Depart Car
            print("\nSelect a lane to depart from (1-4) or 0 to cancel:")
            lane_choice = input("Enter lane number: ").strip()
            
            try:
                lane_num = int(lane_choice)
                if lane_num == 0:
                    print("Cancelled.")
                    continue
                if lane_num < 1 or lane_num > 4:
                    print("Invalid lane number!")
                    continue
                
                lane_idx = lane_num - 1
                if lanes[lane_idx].isEmpty():
                    print(f"Lane {lane_num} is empty!")
                else:
                    departure_counter[0] += 1
                    departed_car = lanes[lane_idx].dequeue()
                    departed_car['departure_num'] = departure_counter[0]
                    
                    display_parking_table.departed_cars.append(departed_car)
                    
                    print(f"\n✓ Car {departed_car['plate']} departed from Lane {lane_num}")
                    print(f"  Departure #: {departure_counter[0]}")
            except ValueError:
                print("Invalid input!")
        
        elif choice == '3':  # View Parking Garage
            display_parking_table(lanes)
        
        elif choice == '4':  # Exit
            print("\nThank you for using the Parking Garage System!")
            break
        
        else:
            print("Invalid choice! Please enter 1-4.")

if __name__ == "__main__":
    main()
