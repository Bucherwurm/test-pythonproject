"""
choice1 =input("Player 1, enter your choice (rock, paper, scissors): ").lower()
choice2 =input("Player 2, enter your choice (rock, paper, scissors): ").lower()
if choice1 == choice2:
    print("It's a tie.")    
elif (choice1 == "rock" and choice2 == "scissors") or (choice1 == "paper" and choice2 == "rock") or (choice1 == "scissors" and choice2 == "paper"):
    print("Player 1 WINS!")
elif (choice2 == "rock" and choice1 == "scissors") or (choice2 == "paper" and choice1 == "rock") or (choice2 == "scissors" and choice1 == "paper"):
    print("Player 2 WINS!")
else:
    print("Invalid input. Please enter rock, paper, or scissors.") 
"""

import random
choices = ["rock", "paper", "scissors"]
player_choice = input("Enter your choice (rock, paper, scissors): ").lower()
computer_choice = random.choice(choices)
print(f"Computer chose: {computer_choice}")
if player_choice == computer_choice:
    print("It's a tie.")
elif (player_choice == "rock" and computer_choice == "scissors") or (player_choice == "paper" and computer_choice == "rock") or (player_choice == "scissors" and computer_choice == "paper"):
    print("You WIN!")
elif (computer_choice == "rock" and player_choice == "scissors") or (computer_choice == "paper" and player_choice == "rock") or (computer_choice == "scissors" and player_choice == "paper"):
    print("Computer WINS!")
else:
    print("Invalid input. Please enter rock, paper, or scissors.")  