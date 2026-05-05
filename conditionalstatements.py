first_name = input("Enter is your first name: ")
last_name = input("Enter is your last name: ")
email = input("Enter your email: ")
re_email = input("Re-enter your email: ")
password = input("Enter your password: ")
if first_name == '':
    print("First name cannot be empty.")
    isfirst_name_valid = False
elif not first_name.isalpha():
    print("First name must contain only letters.")
    isfirst_name_valid = False
else:
    print("First name is valid.")
    isfirst_name_valid = True
if last_name == '':
    print("Last name cannot be empty.")
    islast_name_valid = False
elif not last_name.isalpha():
    print("Last name must contain only letters.")
    islast_name_valid = False
else:
    print("Last name is valid.")
    islast_name_valid = True
if email == '':
    print("Email cannot be empty.")
    isemail_valid = False
elif '@' not in email or '.' not in email:
    print("Email must contain '@' and '.'.")
    isemail_valid = False
else:
    print("Email is valid.")
    isemail_valid = True
if re_email == '':
    print("Re-entered email cannot be empty.")
    isre_email_valid = False
elif re_email != email:
    print("Re-entered email does not match.")
    isre_email_valid = False
else:    
    print("Re-entered email is valid.")
    isre_email_valid = True
if password == '':
    print("Password cannot be empty.")
    ispassword_valid = False
elif len(password) <= 6:
    print("Password must be at least 6 characters long.")
    ispassword_valid = False
else:
    print("Password is valid.")
    ispassword_valid = True
if isfirst_name_valid and islast_name_valid and isemail_valid and isre_email_valid and ispassword_valid:
     print("Registration successful!")
else:
    print("Registration failed. Please correct the errors and try again.")