'''
price = 111.33
num = 3
stotal = price * num
print(stotal)
discountamt = 10/100 * stotal
print(f"{discountamt:.2f}")
total = stotal - discountamt
print(f"{total:.2f}")
'''

'''
ppn = 1200.88
ns = 7
ntotal = ppn * ns
print(ntotal)
discountamt = 18/100 * ntotal   
print(f"{discountamt:.2f}")
total2 = ntotal - discountamt
print(f"{total2:.2f}")  
'''
'''
a = int(input("Enter a number: "))
b = int(input("Enter another number: "))
sum = a + b
print("The sum is: ", sum)
sub = a - b 
print("The difference is: ", sub)
mul = a * b
print("The product is: ", mul)
div = a / b
print("The quotient is: ", div) 
expo = a ** b
print("The exponentiation is: ", expo)
rem = a % b
print("The remainder is: ", rem)
ddiv = a // b
print("The floor division is: ", ddiv)

'''
year = 2026
month = 12
day = 25
print(year, month, day, sep="-")
print(f'{year}-{month}-{day}')
print('/' .join((year,month,day)))
print('/' .join([year,month,day]))

name = 'rahUL DahaL'
print(name.title())