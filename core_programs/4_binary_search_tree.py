inputs=0

#Binary Search Tree
print("BINARY SEARCH TREE: Input a number and we will make a binary search tree for you.")
first_num=int(input("Input your number:"))#Ask user to input number
print (first_num)#First number is directly outputted
inputs+=1
print(f"inputs:{inputs}") #REMOVE THIS IN FINAL (FOR CHECKING ONLY)
while True: #Program will ask for user input until user types 'Done' or they have reached the maximum inputs (100 inputs)
    try:
        while inputs!=100:
            ...
    except ValueError:
        print("You have typed in 'DONE'. Creating your tree...")
#Suceeding numbers will be identified whether greater or smaller than the first number and preceeding numbers.
#Smaller numbers go the left, larger numbers go to the right