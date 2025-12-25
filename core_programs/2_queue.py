#Queue Data Structure Core Program
#Queue Logic Python File
#Implement Enqqueue(), Dequeue(), Peek(), isEmpty(), and size operations as Python Functions

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


    