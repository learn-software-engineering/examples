def countdown(number):

    if number > 0:
        print(number)
        countdown(number - 1)
    else:
        print("Blastoff!")

countdown(5)
