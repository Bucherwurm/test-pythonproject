# def bank_transfer(sender, receiver, amount):
#     print(f'Transfering ${amount} from {sender} to {receiver}')
# bank_transfer('Alice','Charlie',500)

# def book_flight(from_city,to_city):
#     print(f'Booking a flight from {from_city} to {to_city}')
# book_flight(to_city='Nice',from_city='Dublin')

def c_g(score):
    if score < 0 or score > 100:
        return "invalid score"
    
    if score >= 90:
        return'A+'
    elif score >= 80:
        return 'A'
    elif score >= 70:
        return 'B'
    elif score >= 60:
        return 'C'
    elif score >= 50:
        return 'D'
    else:
        return 'F'
    
print(c_g(95))
print(c_g(75))
print(c_g(45))
print(c_g(105))
    