# while True:
#     u = int(input("Enter your age: "))
    
#     if u < 18: 
#         print("You are a minor.")
#     elif u >= 18 and u <= 60:
#         print("You are an adult.")
#     else:
#         print("You are a senior citizen.")
    
#     c = input("Do you want to continue (Y/N)? ")
#     if c.upper() == "N":
#         break

#2
# while(v := input("Enter the name of a vehicle : ").lower()) != "bus":
#     print("Waiting....")
# else:
#     print("Finally the wait is over.")

#3
# ratings = ['4+','9+','12+','17+','4+','12+','4+','9+','17+','12+','4+','17+']
# current_ratings = dict()
# i = 0
# while i < len(ratings):
#     current_ratings[ratings[i]] = current_ratings.get(ratings[i],0)+1
#     i += 1
# print(current_ratings) 

#4
# import random
# x = random.randint(1,10)
# count = 0
# while (u := int(input("Guess the number betn 1 and 10 : "))) != x:
#     count += 1
#     if u < x:
#         print("Guess Higher")
#     elif u > x:
#         print("Guess Lower")
# else:
#     count += 1
#     print(f"Congratulations! You guessed correctly. Number : {x}  Attempts : {count}")

#5
# username = "admin"
# password = "1234"
# attempt = 0 
# while attempt < 3:
#     attempt += 1
#     uin = input("Username : ")
#     pin = input("Password : ")
#     if uin == username and pin == password:
#         print("Login Successful")
#         break
#     else:
#         print("Invalid Credentials, try again")
# else:
#     print("Too many failed attempts")

#7
count = 0
while True:
    uin = input("Enter name  : ")
    if uin == "good luck":
        count += 1
        if count < 3:
            print(f"You entered good luck {count} times")
        elif count == 3:
            print("You entered good luck three times")
            break
    
