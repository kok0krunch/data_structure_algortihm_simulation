# Tower of Hanoi

# Ask user how many disks
user_input = int(input("How many disks would you like? "))
choose_origin_tower = int(input("From which tower do you wish to start the puzzle?:(1, 2, 3) "))
choose_destination_tower = int(input("Where do you eish to put the disks?:(1, 2, 3) "))
if choose_origin_tower == choose_destination_tower:
    print('Invalid input')
# Calculate how many moves it takes to solve the puzzle
num_moves = 2 ** int(user_input) - 1
print(f"It takes {num_moves} to solve for the tower")

# Functions for solving Tower of Hanoi using recursion
def tower_one_to_tower_two(user_input, tower_1, tower_2, tower_3):
    if user_input == 0:
        return
    tower_one_to_tower_two(int(user_input) - 1, tower_1, tower_3, tower_2)
    print("Move disk", user_input, "from", tower_1, "to", tower_2)
    tower_one_to_tower_two(int(user_input) - 1, tower_3, tower_2, tower_1)

def tower_one_to_tower_three(user_input, tower_1, tower_2, tower_3):
    if user_input == 0:
        return
    
    tower_one_to_tower_three(int(user_input) - 1, tower_1, tower_3, tower_2)
    print('Move disk', user_input, 'from', tower_1, 'to', tower_3)
    tower_one_to_tower_three(int(user_input) - 1, tower_2, tower_1, tower_3)

def tower_two_to_tower_one(user_input, tower_2, tower_3, tower_1):
    if user_input == 0:
        return
    
    tower_two_to_tower_one(int(user_input) - 1, tower_2, tower_1, tower_3)
    print("Move disk", user_input, "from", tower_2, "to", tower_1)
    tower_two_to_tower_one(int(user_input) - 1, tower_3, tower_2, tower_1)

def tower_two_to_tower_three(user_input, tower_2, tower_1, tower_3):
    if user_input == 0:
        return
    tower_two_to_tower_three(int(user_input) - 1, tower_2, tower_3, tower_1)
    print("Move disk", user_input, "from", tower_2, "to", tower_3)
    tower_two_to_tower_three(int(user_input) - 1, tower_1, tower_2, tower_3)

def tower_three_to_tower_one(user_input, tower_3, tower_2, tower_1):
    if user_input == 0:
        return
    tower_three_to_tower_one(int(user_input) - 1, tower_3, tower_1, tower_2)
    print("Move disk", user_input, "from", tower_3, "to", tower_1)
    tower_three_to_tower_one(int(user_input) - 1, tower_2, tower_3, tower_1)

def tower_three_to_tower_two(user_input, tower_3, tower_1, tower_2):
    if user_input == 0:
        return
    tower_three_to_tower_two(int(user_input) - 1, tower_3, tower_2, tower_1)
    print("Move disk", user_input, "from", tower_3, "to", tower_2)
    tower_three_to_tower_two(int(user_input) - 1, tower_1, tower_3, tower_2)

def main_menu():
    if choose_origin_tower == 1 and choose_destination_tower == 2:
        tower_one_to_tower_two(user_input, 'tower_1', 'tower_2', 'tower_3')
    elif choose_origin_tower == 1 and choose_destination_tower == 3:
        tower_one_to_tower_three(user_input, 'tower_1', 'tower_2', 'tower_3') 
    elif choose_origin_tower == 2 and choose_destination_tower == 1:
        tower_two_to_tower_one(user_input, 'tower_2', 'tower_3', 'tower_1')
    elif choose_origin_tower == 2 and choose_destination_tower == 3:
        tower_two_to_tower_three(user_input, 'tower_2', 'tower_1', 'tower_3')
    elif choose_origin_tower == 3 and choose_destination_tower == 2:
        tower_three_to_tower_two(user_input, 'tower_3', 'tower_1', 'tower_2')
    elif choose_origin_tower == 3 and choose_destination_tower == 1:
        tower_three_to_tower_one(user_input, 'tower_3', 'tower_2', 'tower_1')





 
    


# Calls the functions
