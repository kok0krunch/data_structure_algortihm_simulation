#Queue Program Logic Python File
#Implement Table for license plate, number of arrival, number of departure, and who arrived and departed
#Implement a 4 Lane Parking Garage Simulation using Queue Data Structure

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


def print_menu():
    print("\n" + "="*50)
    print("Parking Garage Queue Management")
    print("="*50)
    print("1. Park Car (Enqueue)")
    print("2. Depart Car (Dequeue)")
    print("3. View Parking Garage")
    print("4. Exit Parking Garage")
    print("="*50)


def main():


if __name__ == "__main__":
    main()
