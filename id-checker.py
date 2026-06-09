id = [{'username': 'admin', 'password': 'pass123'}, {'username': 'user', 'password': 'user123'}]
for i in range(3):
    username = input("Enter username: ")
    password = input("Enter password: ")
    for j in range(len(id)):
        if username == id[j]['username'] and password == id[j]['password']:
            print("Access Granted")
            break
    else:
        print("Access Denied")
        remaining = 2 - i
        if remaining > 0:
            print(f"Try again ({remaining} attempts left)")
        else:
            print("Account locked!")
        continue 
    break  