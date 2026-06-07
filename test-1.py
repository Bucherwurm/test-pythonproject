quiz_data = {
    'qno1':{
        'question':'Which Python library is used for building Desktop GUI ?',
        'options':['NumPy','Pandas','Tkinter','Flask'],
        'answer':'Tkinter'
    },
    'qno2':{
        'question':'What is the result of 4 == 7 in Python ?',
        'options':['True','False','Error','None'], 
        'answer':'False' 
        },
    'qno3':{
        'question':'Which set method is used to check if two sets have no common elements ?',
        'options':['issubset()','intersection()','isdisjoint()','difference()'], 
        'answer':'isdisjoint()'
    }
    
}
count = 0
for i,j in quiz_data.items():
    print(i,' : ',j['question'])
    print()
    for k in j['options']:
        print(k)
    print()
    ans = input("Enter Answer : ")
    if ans == j['answer']:
        count += 1
print()
print(f"You got {count} questions correct ")
