# Tower of Hanoi

# Ask user how many disks
user_input = input("How many disks would you like? ")

# Calculate how many moves it takes to solve the puzzle
num_moves = int(user_input) ** 2 - 1
print(f"It takes {num_moves} to solve for the tower")

def TowerOfHanoi(user_input, tower_1, tower_2, tower_3):
    if user_input == 0:
        return
    
    TowerOfHanoi(int(user_input) - 1, tower_1, tower_2, tower_3)
    print('Move disk', user_input, 'from', tower_1, 'to', tower_3)
    TowerOfHanoi(int(user_input) - 1, tower_1, tower_2, tower_3)
    print('Move disk', user_input, 'from', tower_1, 'to', tower_2)

TowerOfHanoi(user_input, 'tower_1', 'tower_2', 'tower_3') 



#note: possible na i ask pano sya ilagay sa tower 2 or maybe yung placement ng disks ay nasa tower 3