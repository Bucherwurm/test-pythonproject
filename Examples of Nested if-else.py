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

#5
age=int(input("Enter your age: "))
monthly_income=int(input("Enter your monthly income: "))
credit_score=int(input("Enter your credit score: "))
if age < 21 or age > 60:
    print("Age must be between 21 and 60.")
elif monthly_income < 30000:
    print("Monthly income must be at least 30,000.")
elif credit_score < 700:
    print("Credit score must be at least 700.")
else:
    print("You are eligible for the loan.")

#6
age=int(input("Enter your age: "))
member_status=input("Are you a member? (yes/no): ").lower()
if age < 12:
    print('The ticket is free for children under 12.')
elif age >= 12 and age <= 60:
    if member_status == 'yes':
        print('The ticket price is Rs.150 for members.')
    else:
        print('The ticket price is Rs.200 for non-members.')
elif age > 60:
    print('The ticket price is Rs.100 for senior citizens.')

#7
salary=int(input("Enter your salary: "))
service_year=int(input("Enter your years of service: "))
if service_year >5:
    bonus=salary*0.05
    netbonus=salary+bonus
    print(f"Your net salary is Rs.{netbonus}.")
else:
    print("You are not eligible for a bonus.")

#8
radius=float(input("Enter the radius of the circle (in cm): "))
area=3.14*radius**2
print(f"The area of the circle is: {area} cm²")

#9
age=int(input("Enter your age: "))
gender=input("Enter your gender (M/F): ").upper()
number_of_days=int(input("Enter the number of days you have worked: "))
if age >= 18 and age < 30:
    if gender == 'M':
        wages=number_of_days*700
    elif gender == 'F':
        wages=number_of_days*750
elif age >= 30 and age <= 40:
    if gender == 'M':
        wages=number_of_days*800
    elif gender == 'F':
        wages=number_of_days*850
else:
    print("Invalid age. Age must be between 18 and 40.")
print(f"Your wages are Rs.{wages}.")

#10
number=int(input("Enter a number: "))
if number % 3 == 0 and number % 5 == 0:
    print("Fizz Buzz")
elif number % 3 == 0:
    print("Fizz")   
elif number % 5 == 0:
    print("Buzz")
else:
    print(number)