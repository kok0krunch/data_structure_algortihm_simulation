#Queue Data Structure Core Program
#Queue Logic Python File
#Implement Enqqueue(), Dequeue(), Peek(), isEmpty(), and size operations as Python Functions
#Implement Table for license plate, number of arrival, number of departure, and who arrived and departed

class Queue:
    def __init__(self):
        self.items = {}
        self.front = 0
        self.rear = 0

    def isEmpty(self):
        return self.size() == 0

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

    def display(self):
        if self.isEmpty():
            return "Queue is empty"
        items = [self.items[i] for i in range(self.front, self.rear)]
        items.reverse()
        return " -> ".join(map(str, items))


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
    queue = Queue()
    
    while True:
        print_menu()
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1':
            try:
                element = input("Enter element to enqueue: ").strip()
                if element:
                    queue.enqueue(element)
                    print(f"✓ '{element}' added to queue")
                    print(f"Current Queue: {queue.display()}")
                else:
                    print("✗ Invalid input. Please enter a non-empty element.")
            except Exception as e:
                print(f"✗ Error: {e}")
        
        elif choice == '2':
            try:
                removed = queue.dequeue()
                print(f"✓ Dequeued: '{removed}'")
                print(f"Current Queue: {queue.display()}")
            except IndexError as e:
                print(f"✗ Error: {e}")
        
        elif choice == '3':
            try:
                front = queue.peek()
                print(f"✓ Front element: '{front}'")
                print(f"Current Queue: {queue.display()}")
            except IndexError as e:
                print(f"✗ Error: {e}")
        
        elif choice == '4':
            if queue.isEmpty():
                print("✓ Queue is EMPTY")
            else:
                print("✓ Queue is NOT empty")
            print(f"Current Queue: {queue.display()}")
        
        elif choice == '5':
            size = queue.size()
            print(f"✓ Queue size: {size}")
            print(f"Current Queue: {queue.display()}")
        
        elif choice == '6':
            display = queue.display()
            print(f"Queue contents: {display}")
        
        elif choice == '7':
            print("\n✓ Exiting... Goodbye!")
            break
        
        else:
            print("✗ Invalid choice. Please select 1-7.")



if __name__ == "__main__":
    main()
