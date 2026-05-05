first_name = input("Enter is your first name: ")
last_name = input("Enter is your last name: ")
email = input("Enter your email: ")
re_email = input("Re-enter your email: ")
password = input("Enter your password: ")
if not (first_name and last_name and email and re_email and password):
    print("All fields are required.")
    is_valid = False
elif not (first_name.isalpha() and last_name.isalpha()):
    print("First name and last name must contain only letters.")
    is_valid = False
elif '@' not in email or '.' not in email:
    print("Email must contain '@' and '.'.")
    is_valid = False
elif re_email != email:
    print("Re-entered email does not match.")
    is_valid = False
elif len(password) <= 6:
    print("Password must be at least 6 characters long.")
    is_valid = False
else:
    print("All inputs are valid.")
    is_valid = True

if is_valid:
    print("Registration successful!")
else:
    print("Registration failed. Please correct the errors and try again.")