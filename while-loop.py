# 1
# t = 0
# while (n := int(input("Enter a number: "))) != 0:
#     t += n
#     print(f"Total sum of all entered numbers: {t}")

# 2
# n = int(input("Enter a number: "))
# while n != 1:
#     print(n)
#     n -=1
# else:
#     print("Lower threshold reached")

# 3
# import random
# n = random.randint(1,100)
# count = 0
# while (guess := int(input("Enter a num 1-100: "))) != n:
#     count += 1
#     if guess < n :
#         print("Too low")
#     elif guess > n:
#         print("Too high")
# else:
#     print(f"Congratulations! You guessed the number {n} in {count} attempts.")

# 4
# while len((password := input("Enter a passowrd : "))) < 8:
#     print('Password must be 8+ characters')

# 5
# total = 0
# counter = 1
# while counter <= 50:
#     total += counter
#     counter += 1
# print(f"The sum of all numbers from 1 to 50 is {total}")

# 6
# n = int(input("Enter a number : "))
# i = 1
# while i in range(1,11):
#     print(f'{i} * {n} = {i*n}')
#     i += 1

# 7
# ratings = ['4+','9+','12+','17+','4+','12+','4+','9+','17+','12+','4+','17+']
# current_ratings = dict()
# i = 0
# while i < len(ratings):
#     current_ratings[ratings[i]] = current_ratings.get(ratings[i],0)+1
#     i += 1
# print(current_ratings) 

#8
# import random
# n = random.randint(1,50)
# i = 7
# attempts = 0
# while (guess := int(input("Enter a num between 1 and 50 : "))) != n:
#     i -= 1
#     print(f"{i} attempts remaining.")
#     attempts += 1
#     if i == 0:
#         print("Game Over!")
#         print(F"Number was {n}")
#         break
# else:
#     print(f'You guessed correctly in {attempts} attempts.')



#9

