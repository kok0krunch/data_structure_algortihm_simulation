# Tower of Hanoi

# Ask user how many disks
user_input = input("How many disks would you like? ")

# Calculate how many moves it takes to solve the puzzle
num_moves = int(user_input) ** 2 - 1
print(f' It takes {num_moves} to solve for the tower')