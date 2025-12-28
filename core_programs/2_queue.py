#Queue Program Logic Python File
#Implement Table for license plate, number of arrival, number of departure, and who arrived and departed
#Implement a 4 Lane Parking Garage Simulation using Queue Data Structure
#Implement a Random License plate generator for cars arriving at the parking garage
import core_programs_module as cpm


def print_menu():
    print("\n" + "="*50)
    print("Parking Garage Queue Management")
    print("="*50)
    print("1. Park Car (Enqueue)")
    print("2. Depart Car (Dequeue)")
    print("3. Exit Parking Garage")
    print("="*50)


def main():
    # Initialize 4 parking lanes with lane-specific counters
    lanes = [cpm.Queue(i+1) for i in range(4)]
    
    while True:
        cpm.clear_console()
        cpm.render_parking_grid(lanes)
        print_menu()
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == '1':  # Park Car
            license_plate = cpm.generate_license_plate()
            
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
                    print(f"\n✗ ERROR: Lane {lane_num} is full. Cannot park.")
                    input("Press Enter to continue...")
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
                print(f"\n✓ SUCCESS: Car {license_plate} added to Lane {lane_num}")
                print(f"  Lane Arrival #: {lane_arrival_num}")
                print(f"  Current Lane Occupancy: {lanes[lane_idx].size()}/4")
                input("\nPress Enter to continue...")
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
                    print(f"\n✗ ERROR: Lane {lane_num} is empty. No car to remove.")
                    input("Press Enter to continue...")
                else:
                    # Increment lane-specific departure counter
                    lanes[lane_idx].departure_count += 1
                    lane_departure_num = lanes[lane_idx].departure_count
                    
                    departed_car = lanes[lane_idx].dequeue()
                    departed_car['departure_num'] = lane_departure_num
                    
                    print(f"\n✓ SUCCESS: Car {departed_car['plate']} removed from Lane {lane_num}")
                    print(f"  Lane Departure #: {lane_departure_num}")
                    print(f"  Current Lane Occupancy: {lanes[lane_idx].size()}/4")
                    input("\nPress Enter to continue...")
            except ValueError:
                print("Invalid input!")
        
        elif choice == '3':  # Exit
            print("\nThank you for using the Parking Garage System!")
            break
        
        else:
            print("Invalid choice! Please enter 1-3.")

if __name__ == "__main__":
    main()
