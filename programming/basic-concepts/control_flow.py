####
# If
####
print("### Example showing use fo the `if` structure")

age = 15
if age >= 18:
    print("   You are an adult")

#########
# If-Else
#########
print("### Example showing use fo the `if-else` structure")

age = 21
if age >= 18:
    print("   You are an adult")
else:
    print("   You are a minor")

##############
# If-Elif-Else
##############
print("### Example showing use fo the `if-elif-else` structure")

age = 5
if age <= 13:
    print("   You are a child")
elif age > 13 and age < 18:
    print("   You are a teenager")
else:
    print("   You are an adult")

#######
# While
#######
i = 1
while i <= 5:
    print(i)
    i = i + 1

#####
# For
#####
print("### Example showing use fo the `for` structure")

names = ["Maria", "Florencia", "Julian"]
for name in names:
    print(f"   Hello {name}")

################
# break sentence
################
print("### Example showing use of the `break` sentence")

i = 0
while i < 10:
    print(i)
    if i == 5:
        break
    i += 1

###################
# continue sentence
###################
print("### Example showing use of the `continue` sentence")

i = 0
while i < 10:
    i += 1
    if i % 2 == 0:
        continue
    print(i)

#################################
# Nesting flow control structures
#################################
print("### Example showing nested structures")

for i in range(5):
    for j in range(10):
        if (i % 2 == 0 and j % 3 == 0):
            print(f"i = {i}, j = {j}")

# Prints:
# i = 0, j = 0
# i = 0, j = 3
# i = 0, j = 6
# i = 0, j = 9
# i = 2, j = 0
# i = 2, j = 3
# i = 2, j = 6
# i = 2, j = 9
# i = 4, j = 0
# i = 4, j = 3
# i = 4, j = 6
# i = 4, j = 9

#############################
# Common use patterns: search
#############################
print("### Example of the use of the search pattern")

fruits = ["apple", "orange"]

searching = "orange"
found = False

for fruit in fruits:
    if fruit == searching:
        found = True
        break

if found:
    print("Fruit found!")

###################################
# Common use patterns: accumulation
###################################
print("### Example of using accumulation pattern")

total = 0

for i in range(10):
    total += i

print(total)  # Sum from 0..9 = 45
