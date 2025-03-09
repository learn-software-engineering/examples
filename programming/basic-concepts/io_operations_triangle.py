############
# User input
############
side1 = float(input("Enter the length of the first side: "))
side2 = float(input("Enter the length of the second side: "))
side3 = float(input("Enter the length of the third side: "))

#######################
# Perimeter calculation
#######################
perimeter = side1 + side2 + side3
print(f"The triangle's perimeter is: {perimeter}")

########################################
# Area calculation using Heron's formula
########################################
s = perimeter / 2
area = (s*(s-side1)*(s-side2)*(s-side3)) ** 0.5
print(f"The triangle's area is: {area:.2f}")
