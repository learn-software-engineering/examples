class Node:
    def __init__(self, value):
        self.value = value
        self.previous = None


class Stack:
    def __init__(self):
        self.top = None
        self.size = 0

    def push(self, value):
        new_node = Node(value)
        if self.top is None:
            self.top = new_node
        else:
            new_node.previous = self.top
            self.top = new_node
        self.size += 1

    def pop(self):
        if self.top is None:
            return None
        top_node = self.top
        self.top = self.top.previous
        self.size -= 1
        return top_node.value

    def peek(self):
        if self.top is None:
            return None
        return self.top.value

    def is_empty(self):
        return self.top is None  # Returns true if top is None

    def __len__(self):
        return self.size

    def __str__(self):
        values = []
        current = self.top
        while current:
            values.append(str(current.value))
            current = current.previous
        return "\n".join(values)


print("Creating a new stack")
stack = Stack()

print("==========")
print("Check if stack is empty")
print(f"Is stack empty? {stack.is_empty()}")

print("==========")
print("Push first element")
print("   stack.push(\"First\")")
stack.push("First")

print("==========")
print("Print stack:")
print(stack)

print("==========")
print("Print top element using peek")
print(f"stack.peek() => {stack.peek()}")

print("Add two more elements: stack.push(\"\"):")
print("   stack.push(\"Second\")")
print("   stack.push(\"Third\")")
stack.push("Second")
stack.push("Third")

print("==========")
print("Print stack:")
print(stack)

print("==========")
print("Print top element using peek")
print(f"stack.peek() => {stack.peek()}")

print("==========")
print("Check if stack is empty")
print(f"Is stack empty? {stack.is_empty()}")

print("==========")
print("Get top element using pop")
print(f"stack.pop() => {stack.pop()}")

print("==========")
print("Print top element using peek")
print(f"stack.peek() => {stack.peek()}")

print("==========")
print("Get top element using pop")
print(f"stack.pop() => {stack.pop()}")

print("==========")
print("Get top element using pop")
print(f"stack.pop() => {stack.pop()}")

print("==========")
print("Check if stack is empty")
print(f"Is stack empty? {stack.is_empty()}")
