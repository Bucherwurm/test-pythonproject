floor_input = int(input("Enter the floor number (0-10): "))
if floor_input < 0 or floor_input > 10:
    print("Invalid floor number. Please enter a number between 0 and 10.")
else:
    total_weight = int(input("Enter the total weight of passengers in kg: "))
    if total_weight <=0:
        print("Invalid weight. Please enter a non-negative number.")
    elif total_weight > 500:
        print("Overweight! The elevator cannot move.")
    else:
        door_status = input("Is the door open or closed? (open/closed): ").lower()
        if door_status == "open":
            print("Please close the door before moving the elevator.")
        elif door_status == "closed":
            print(f"Elevator is moving to floor {floor_input}.")
        else:
            print("Invalid door status. Please enter 'open' or 'closed'.")
