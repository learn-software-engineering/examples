######################
# Factorial calculator
######################
def factorial(n):
    if n == 1:
        return 1       # Base case
    return n * factorial(n-1) # Recursive case


############
# User input
############
print("Welcome to Factorial calculator, press Control+C to exit")

while True:
    number = int(input("For what number do you want to obtain the factorial?: "))
    print(f"{number}! = {factorial(number)}")
