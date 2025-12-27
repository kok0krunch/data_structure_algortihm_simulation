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

def TowerOneToTowerThree(user_input, tower_1, tower_2, tower_3):
    if user_input == 0:
        return
    
    TowerOneToTowerThree(int(user_input) - 1, tower_1, tower_3, tower_2)
    print('Move disk', user_input, 'from', tower_1, 'to', tower_3)
    TowerOneToTowerThree(int(user_input) - 1, tower_2, tower_1, tower_3)
TowerOneToTowerThree(user_input, 'tower_1', 'tower_2', 'tower_3') 

def TowerOneToTowerTwo(user_input, tower_1, tower_2, tower_3):
    if user_input == 0:
        return
    
    TowerOneToTowerTwo(int(user_input) - 1, tower_1, tower_3, tower_2)
    print("Move disk", user_input, "from", tower_1, "to", tower_2)
    TowerOneToTowerTwo(int(user_input) - 1, tower_3, tower_2, tower_1)
TowerOneToTowerTwo(user_input, 'tower_1', 'tower_2', 'tower_3')

def TowerTwoToTowerOne(user_input, tower_2, tower_3, tower_1):
    if user_input == 0:
        return
    
    TowerTwoToTowerOne(int(user_input) - 1, tower_2, tower_1, tower_3)
    print("Move disk", user_input, "from", tower_2, "to", tower_1)
    TowerTwoToTowerOne(int(user_input) - 1, tower_3, tower_2, tower_1)

TowerTwoToTowerOne(user_input, 'tower_2', 'tower_3', 'tower_1')

def TowerTwoToTowerThree(user_input, tower_2, tower_1, tower_3):
    if user_input == 0:
        return
    TowerTwoToTowerThree(int(user_input) - 1, tower_2, tower_3, tower_1)
    print("Move disk", user_input, "from", tower_2, "to", tower_3)
    TowerTwoToTowerThree(int(user_input) - 1, tower_1, tower_2, tower_3)

TowerTwoToTowerThree(user_input, 'tower_2', 'tower_1', 'tower_3')

def TowerThreeToTowerOne(user_input, tower_3, tower_2, tower_1):
    if user_input == 0:
        return
    TowerThreeToTowerOne(int(user_input) - 1, tower_3, tower_1, tower_2)
    print("Move disk", user_input, "from", tower_3, "to", tower_1)
    TowerThreeToTowerOne(int(user_input) - 1, tower_2, tower_3, tower_1)

TowerThreeToTowerOne(user_input, 'tower_3', 'tower_2', 'tower_1')