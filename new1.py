'''
header = "STUDENT ID CARD"
st_N = input("Enter Student Name: ")
st_a = input("Enter Student Age: ")
st_c = input("Enter Student Class: ")
st_co = input("Enter Student College: ")
st_bg = input("Enter Student Blood Group: ")
print(header.center(30))
print("FullName"+" "*5 +": ", st_N)
print("Age"+" "*10 +": ", st_a)
print("Class"+" "*8 +": ", st_c)
print("College"+" "*6 +": ", st_co)
print("Blood Group"+" "*2 +": ", st_bg)
'''

userinput = input("Enter something: ")
if userinput.isspace():
    print("Blank field")
else:
    print("Valid")