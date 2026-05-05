#1
age=int(input("Enter your age: "))
height=float(input("Enter your height in cm: "))
if age >= 12 and height >= 140: 
    print("You are eligible to ride the roller coaster.")
else:
    print("You are not eligible to ride the roller coaster.")

#2
traffic_light=input("Enter the traffic light color (red, yellow, green): ").lower()
match traffic_light:
    case "red":        print("Stop")
    case "yellow":     print("Get ready to Stop")
    case "green":      print("Go")
    case _:            print("Invalid traffic light color. Please enter red, yellow, or green.")

#3
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

#4
username = input("Enter your username: ")
password = input("Enter your password: ")
if username == "admin":
    if password == "pass123":
        print("Valid Login")
    else:
        print("Incorrect password.")
else:
    print("Invalid username.")

