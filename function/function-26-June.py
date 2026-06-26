# from tkinter import *
# root = Tk()
# root.geometry("1000x1000")
# def login(num):
#     print(f"{num}")
# btn = Button(root, text="1", font=("Arial", 20), bg="red", fg="white", command=lambda : login(1))
# btn.pack()
# btn = Button(root, text="2", font=("Arial", 20), bg="red", fg="white", command=lambda : login(2))
# btn.pack()
# btn = Button(root, text="3", font=("Arial", 20), bg="red", fg="white", command=lambda : login(3))
# btn.pack()
# btn = Button(root, text="4", font=("Arial", 20), bg="red", fg="white", command=lambda : login(4))
# btn.pack()
# btn = Button(root, text="5", font=("Arial", 20), bg="red", fg="white", command=lambda : login(5))
# btn.pack()
# btn = Button(root, text="6", font=("Arial", 20), bg="red", fg="white", command=lambda : login(6))
# btn.pack()
# btn = Button(root, text="7", font=("Arial", 20), bg="red", fg="white", command=lambda : login(7))
# btn.pack()
# btn = Button(root, text="8", font=("Arial", 20), bg="red", fg="white", command=lambda : login(8))
# btn.pack()
# btn = Button(root, text="9", font=("Arial", 20), bg="red", fg="white", command=lambda : login(9))
# btn.pack()
# btn = Button(root, text="0", font=("Arial", 20), bg="red", fg="white", command=lambda : login(0))
# btn.pack()
# mainloop()

# x = y = 20
# result = lambda x,y : x+y
# print(result(x,y))

# l = [1,2,3,4,5,6,7,8,9]
# s_l = list(map(lambda x: x**2,l))
# print(s_l)

# a_h = ["alice", "bob", "charlie", "david", "eve","frank", "grace", "heidi", "ivan", "judy"]
# h = list(filter(lambda x: x.startswith('a') or x.startswith('e'), a_h))
# print(h)
# c_h = list(filter(lambda x: len(x)>3, a_h))
# print(c_h)
# uax_h = list()
# for i in a_h:
#     uax_h.append(i.upper())
# print(uax_h)
# ua_h = list(map(lambda x:x.title(),a_h))
# print(ua_h)

# email = ['alice @ gmail.com','   bob.   @gmail.com']
# remail = list(map(lambda x: x.replace(" ",""), email))
# print(remail)

# number = [1,2,3,4,5,6,7,8,9]
# fumber = list(filter(lambda x: x%2==0,number))
# print(fumber)
# xnumber = list()
# for i in number:
#     if i%2 != 0:
#         xnumber.append(i)
# print(xnumber)
# t = 0
# for i in number:
#     t += i
# print(t)
# from functools import reduce
# T = reduce((lambda x,y: x+y), number)
# print(T)

# items = ['sql','123','python']
# print(items)
# elist = list(filter(lambda x: x.isalpha(), items))
# print(elist)

from functools import reduce
n = [1,2,3,4,5,6,7,8,9,10]
n1 = list(filter(lambda x: x%2==0, n))
n2 = list(map(lambda x: x*2, n1))
n2 = reduce((lambda x,y: x+y), n2)
print(n2)