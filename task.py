number=int(input("Enter a number between 1 and 4: "))
if number ==1:
    print("Spring")
elif number ==2:
    print("Summer")
elif number ==3:
    print("Autumn")
elif number ==4:
    print("Winter")
else:  
    print("Invalid number. Please enter a number between 1 and 4.")

number=int(input("Enter a number between 1 and 4: "))
match number:
    case 1:        print("Spring")
    case 2:        print("Summer")
    case 3:        print("Autumn")
    case 4:        print("Winter")
    case _:        print("Invalid number. Please enter a number between 1 and 4.")
    