#1
records = {'alice':'AliceLight@gmail.com', 'bob':'BobDylan@gmail.com', 'charlie':'CharlieSheen@gmail.com', 'dobby':'Dobbytheelf@gmail.com', 'eliza':'ElizaH@gmail.com'}
userin_name = input("Enter a name : ")
if userin_name in records:
    print(f'Email of {userin_name} : {records[userin_name]} ')
else:
    print("Contact Not Found")

#1 Using get() method
records = {'alice':'AliceLight@gmail.com', 'bob':'BobDylan@gmail.com', 'charlie':'CharlieSheen@gmail.com', 'dobby':'Dobbytheelf@gmail.com', 'eliza':'ElizaHolmes@gmail.com'}
userin_name = input("Enter a name : ").lower()
email = records.get(userin_name)
if email:
    print(f'Email of {userin_name} : {email}')
else:
    print("Contact Not Found")

#2
shopping_list = {'Milk', 'Bread', 'Eggs'}
bought = {'Bread', 'Eggs'}
unbought = shopping_list.difference(bought) 
if unbought:
    print("Unbought Items : ", unbought)
else:
    print("Shopping Complete")

#3
classlist = ['ram','sita','laxman']
new_student = input('Enter student to be added : ').lower()
if new_student in classlist :
    print("Student is already present.")
else:
    classlist  = classlist.append(new_student)
    print("Student added to the list.")

#4
votes = ['Blue','Red','Blue','Green','Blue']
a = votes.count('Blue')
if a >= 3:
  print('Blue Wins!!!')
else:
  print("Blue doesn't win.")

#5
grades = {'Ram': 92, "Sita": 88}
st_n_in = input("Enter students name : ")
check = st_n_in in grades
if check :
    print(grades.get(st_n_in))
else:
    print('Grade not available.')

#6
applicant = { 'name': 'Priya' , "skills" : ['Java','Sql'], 'experience_years' : 1 }
required_skills = {'Python', 'Java'}
if not (required_skills.isdisjoint(applicant['skills'])) and applicant['experience_years'] >=2:
  print('Priya Qualifies')
else:
  print("Priya does not qualify")

#7