class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class Queue:
    def __init__(self):
        self.front = None
        self.end = None
        self.size = 0

    def enqueue(self, value):
        new_node = Node(value)
        if self.end is None:
            self.end = new_node
            self.front = new_node
            return
        self.end.next = new_node
        self.end = new_node
        self.size += 1

    def dequeue(self):
        if self.is_empty():
            return None
        value = self.front.value
        self.front = self.front.next
        if self.front is None:
            self.end = None
        self.size -= 1
        return value

    def peek(self):
        if self.is_empty():
            return None
        return self.front.value

    def is_empty(self):
        return self.front is None  # Returns true if front is None

    def __len__(self):
        return self.size

    def __str__(self):
        values = []
        current = self.front
        while current:
            values.append(str(current.value))
            current = current.next
        return "\n".join(values)


print("Creating a new queue")
queue = Queue()

print("==========")
print("Check if queue is empty")
print(f"Is queue empty? {queue.is_empty()}")


print("==========")
print("Enqueue three elements")
queue.enqueue("ABC")
queue.enqueue("DEF")
queue.enqueue("GHI")

print("==========")
print("Print queue after enqueuing elements:")
print(queue)

print("==========")
print("Get front element using dequeue")
print(f"queue.dequeue() => {queue.dequeue()}")

print("==========")
print("Print queue after dequeue element:")
print(queue)

print("==========")
print("Print front element using peek")
print(f"queue.peek() => {queue.peek()}")

print("==========")
print("Print queue after peek:")
print(queue)

print("==========")
print("Get front element using dequeue")
print(f"queue.dequeue() => {queue.dequeue()}")

print("==========")
print("Print queue after dequeue element:")
print(queue)

print("==========")
print("Check if queue is empty")
print(f"Is queue empty? {queue.is_empty()}")

print("==========")
print("Get front element using dequeue")
print(f"queue.dequeue() => {queue.dequeue()}")

print("==========")
print("Print queue after dequeue element:")
print(queue)

print("==========")
print("Check if queue is empty")
print(f"Is queue empty? {queue.is_empty()}")
