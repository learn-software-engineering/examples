######################
# Fibonacci calculator
######################
def fibonacci(n, a=0, b=1):
    if n == 0:
        return a
    return fibonacci(n-1, b, a+b)


############
# User input
############
print("Welcome to Fibonacci calculator, press Control+C to exit")

while True:
    position = int(input("Position of the Fibonacci numbers would you like to calculate: "))
    print(f"The Fibonacci number in position {position} is {fibonacci(position)}")
