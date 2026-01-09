from 5_recursion.py improt TowerOfHanoi

        # Ask user how many disks
user_input = int(input("How many disks would you like? "))
choose_origin_tower = int(input("From which tower do you wish to start the puzzle?:(1, 2, 3) "))
choose_destination_tower = int(input("Where do you eish to put the disks?:(1, 2, 3) "))
if choose_origin_tower == choose_destination_tower:
    print('Invalid input')
    # Calculate how many moves it takes to solve the puzzle
    num_moves = 2 ** int(user_input) - 1
    print(f"It takes {num_moves} to solve for the tower")



if choose_origin_tower == 1 and choose_origin_tower == 2:
    tower_hanoi.tower_one_to_tower_two()
elif choose_origin_tower == 1 and choose_origin_tower == 3:
    tower_hanoi.tower_one_to_tower_three()
elif choose_origin_tower == 2 and choose_origin_tower == 1:
    tower_hanoi.tower_two_to_tower_one()
elif choose_origin_tower == 2 and choose_origin_tower == 3:
    tower_hanoi.tower_two_to_tower_three
elif choose_origin_tower == 3 and choose_origin_tower == 2:
    tower_hanoi.tower_three_to_tower_one()
elif choose_origin_tower == 3 and choose_origin_tower == 1:
    tower_hanoi.tower_three_to_tower_two()
