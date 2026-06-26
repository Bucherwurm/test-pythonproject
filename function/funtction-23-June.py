# r_balance = 400
# h_balance = 400
# def withdraw(balance, amount = 0 ):
#     amount = int(input("Enter the amount to withdraw: "))
#     if balance >= amount:
#         balance -= amount
#         print(f"Withdrawal Successful! Amount withdrawn: ${amount} New balance: ${balance}")
#     else:
#         print(f"Insufficient funds! Current balance: ${balance}")
#     return balance

# r_balance = withdraw(r_balance)
# print(r_balance)
# r_balance = withdraw(r_balance)

def account(balance):
    c_balance = balance
    def withdraw(amount):
        nonlocal balance
        if balance >=amount:
            balance -= amount
            return f"Withdrawal Successful! Amount withdrawn: ${amount} New balance: ${balance}"
        else:
            return f"Insufficient funds! Current balance: ${balance}"
    return withdraw
u_a = account(1000)
u_k = account(500)
print(u_k(20))
print(u_a(200))
print(u_a(20))
print(u_a.__closure__[0].cell_contents)
print(u_k.__closure__[0].cell_contents)

