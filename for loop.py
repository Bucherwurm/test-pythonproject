# cart = {'Rice': (2, 140), 'Milk': (3, 50), 'Bread': (4, 35), 'Apple':(2,145)}
# print(f"Item\tQuantity\tPrice\tTotal\n")
# total_cost = 0
# for item, (qty, price) in cart.items():
#     total = qty * price
#     print(f'{item}\t{qty}\t\t{price}\t{total}')
#     total_cost += total
# print(f'\nTotal Cost :\t\t\t{total_cost}')

# file_name = ['loop.py', 'photo.jpg', 'xyz.exe', 'abc.exe']
# file1_name = list()
# for i in file_name:
#     if not i.endswith('.exe'):
#         file1_name.append(i)
# print(file1_name)

# items = [1,2,3,11.2,22.1,2+4j,'milk','apple']
# integer_l = list()
# float_l = list()
# complex_l = list()
# string_l = list()
# for i in items:
#     if type(i) == int:
#         integer_l.append(i)
#     elif type(i) == float:
#         float_l.append(i)
#     elif type(i) == complex:
#         complex_l.append(i)
#     elif type(i) == str:
#         string_l.append(i)
# print(integer_l)
# print(float_l)
# print(complex_l)
# print(string_l)

# cart = ['milk','milk','apple','orange','orange']
# d = dict()
# for i in cart:
#     d[i] = d.get(i,0)+1
# print(d)

# cart = ['milk', 'milk', 'apple', 'orange', 'orange']
# d = dict()

# for i in cart:
#     if i in d:  
#         d[i] = d[i] + 1
#     else:
#         d[i] = 1

# print(d)

# cart = ['milk', 'milk', 'apple', 'orange', 'orange']
# d = {}

# for i in cart:
#     if i in d:
#         d[i] = d.get(i) + 1  
#     else:
#         d[i] = 1

# print(d)

n = [1,2,3,-11,13,14,-20]
negative = list()
even = list()
odd = list()
for i in n:
    if i < 0:
        negative.append(i)
    elif i%2 == 0:
        even.append(i)
    else:
        odd.append(i)
print(negative)
print(even)
print(odd)