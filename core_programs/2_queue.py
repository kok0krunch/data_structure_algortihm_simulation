#Queue Program Logic Python File
#Implement Table for license plate, number of arrival, number of departure, and who arrived and departed
#Implement a 4 Lane Parking Garage Simulation using Queue Data Structure
#Implement a Random License plate generator for cars arriving at the parking garage
import random
import string
import core_programs_module as cpm


class Queue:
    def __init__(self, lane_id, max_capacity=4):
        self.items = {}
        self.front = 0
        self.rear = 0
        self.lane_id = lane_id # Identity for this lane (e.g., 1, 2, 3, 4)
        self.arrival_count = 0  # Track total arrivals in this lane
        self.departure_count = 0  # Track total departures in this lane
        self.max_capacity = max_capacity  # Maximum cars allowed in this lane

    def isEmpty(self):
        return self.rear == self.front

    def size(self):
        return self.rear - self.front

    def isFull(self):
        return self.size() >= self.max_capacity

    def enqueue(self, item):
        if self.isFull():
            return False  # Failed to enqueue
        self.items[self.rear] = item
        self.rear += 1
        return True  # Successfully enqueued

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


def render_parking_grid(lanes, grid_rows=4, grid_cols=4):
    """Render a visual parking grid showing occupied and empty spots.
    
    Args:
        lanes: List of Queue objects representing parking lanes
        grid_rows: Number of rows in the parking grid
        grid_cols: Number of columns in the parking grid
    """
    # Create empty grid
    grid = [["[ ---- ]" for _ in range(grid_cols)] for _ in range(grid_rows)]
    
    # Fill grid with cars from each lane - each lane gets its own row
    for lane_idx, lane in enumerate(lanes):
        col_index = 0
        for position, (index, car_data) in enumerate(lane.items.items()):
            if lane_idx < grid_rows and col_index < grid_cols:
                # Display license plate or first part of it for brevity
                plate_display = car_data['plate'][:8] if len(car_data['plate']) > 8 else car_data['plate']
                grid[lane_idx][col_index] = f"[{plate_display:>6}]"
            col_index += 1
    
    # Render the grid
    print("\n" + "="*60)
    print("Parking Garage")
    print("="*60)
    print("EXIT " + " "*45 + "ENTRANCE")
    for row_idx, row in enumerate(grid):
        lane = lanes[row_idx]
        status_indicator = " [FULL]" if lane.isFull() else ""
        lane_label = f"Lane {row_idx + 1}{status_indicator}: "
        spots_display = " ".join(row)
        capacity_display = f"({lane.size()}/4)"
        # Right-align capacity to match ENTRANCE end position (around column 59)
        output = f"{lane_label}{spots_display}"
        # Pad to align capacity at the right edge, under ENTRANCE
        print(f"{output:<54}{capacity_display:>5}")
    print("="*60)
    
    # Display lane statistics
    print("\nLane Statistics:")
    for lane in lanes:
        print(f"  Lane {lane.lane_id}: Arrivals: {lane.arrival_count} | Departures: {lane.departure_count}")
    print("="*60 + "\n")


def print_menu():
    print("\n" + "="*50)
    print("Parking Garage Queue Management")
    print("="*50)
    print("1. Park Car (Enqueue)")
    print("2. Depart Car (Dequeue)")
    print("3. Exit Parking Garage")
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
    
    print("="*90)
    print("="*90)
    
    # Display lane statistics at the bottom
    print("\nLane Statistics:")
    for lane in lanes:
        print(f"  Lane {lane.lane_id}: Arrivals: {lane.arrival_count} | Departures: {lane.departure_count}")
    print("="*90 + "\n")


def main():
    # Initialize 4 parking lanes with lane-specific counters
    lanes = [Queue(i+1) for i in range(4)]
    
    # Store departed cars with their lane information
    display_parking_table.departed_cars = []
    
    while True:
        cpm.clear_console()
        render_parking_grid(lanes)
        print_menu()
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == '1':  # Park Car
            license_plate = generate_license_plate()
            
            # Show lane availability
            print("\nAvailable lanes:")
            for i in range(4):
                capacity_info = f"{lanes[i].size()}/4"
                status = "FULL" if lanes[i].isFull() else "Available"
                print(f"  Lane {i + 1}: {capacity_info} ({status})")
            
            # Ask user to choose a lane
            lane_choice = input("\nSelect a lane (1-4) or 0 to cancel: ").strip()
            
            try:
                lane_num = int(lane_choice)
                if lane_num == 0:
                    print("Cancelled.")
                    continue
                if lane_num < 1 or lane_num > 4:
                    print("Invalid lane number!")
                    continue
                
                lane_idx = lane_num - 1
                
                # Check if lane is full
                if lanes[lane_idx].isFull():
                    print(f"Lane {lane_num} is full! Cannot park.")
                    continue
                
                # Increment lane-specific arrival counter
                lanes[lane_idx].arrival_count += 1
                lane_arrival_num = lanes[lane_idx].arrival_count
                
                car_data = {
                    'plate': license_plate,
                    'arrival_num': lane_arrival_num,
                    'departure_num': None,
                    'lane_id': lane_num
                }
                
                lanes[lane_idx].enqueue(car_data)
                print(f"✓ Car {license_plate} parked successfully in Lane {lane_num}")
                print(f"  Lane Arrival #: {lane_arrival_num}")
            except ValueError:
                print("Invalid input!")
        
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
                    # Increment lane-specific departure counter
                    lanes[lane_idx].departure_count += 1
                    lane_departure_num = lanes[lane_idx].departure_count
                    
                    departed_car = lanes[lane_idx].dequeue()
                    departed_car['departure_num'] = lane_departure_num
                    
                    display_parking_table.departed_cars.append(departed_car)
                    
                    print(f"✓ Car {departed_car['plate']} departed from Lane {lane_num}")
                    print(f"  Lane Departure #: {lane_departure_num}")
            except ValueError:
                print("Invalid input!")
        
        elif choice == '3':  # Exit
            print("\nThank you for using the Parking Garage System!")
            break
        
        else:
            print("Invalid choice! Please enter 1-3.")

if __name__ == "__main__":
    main()
