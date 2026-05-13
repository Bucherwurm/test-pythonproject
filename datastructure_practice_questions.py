#1.
items = [3,5,7,9,11,13]
item = items.pop(4)
items. insert(2, item)
items.append(item)
print(items)

#2.
first_set = {23, 42, 65, 57, 78, 83, 29}
second_set = {57, 83, 29, 67, 73, 43, 48}
if first_set.isdisjoint(second_set):
    print("The sets have no elements in common.")   
else:
    intersection = first_set.intersection(second_set)
    print("The sets have the following elements in common:", intersection) 
    first_set = first_set - intersection
    print("The first set after removing the common elements:", first_set)

#3.
set1 = {27,43,34}
set2 = {34,93,22,27,43,53,48}
if set1.issubset(set2):
    print("Set1 is a subset of Set2")
    set1.clear()
elif set1.issuperset(set2):
    print("Set1 is a superset of Set2")
    set2.clear()
else:
    print("Set1 and Set2 are not subsets of each other")

#4.
month = {'jan': 47 , 'feb': 52 , 'march': 47 , 'April': 44 , 'May': 52 ,  'June': 53 , 'july': 54 , 'Aug': 44 , 'Sept': 54 }
values = month.values()
UniqueValues = list(set(values))
print(UniqueValues)

#5.
sample_list = [87, 45, 41, 65, 94, 41, 99, 94]
unique_tuple = tuple(set(sample_list))
print("result after removing duplicates and creating tuple:", unique_tuple)
print("maximum number: ", max(unique_tuple))
print("minimum number: ", min(unique_tuple))

#6.
club_A = {"ram" , "hari" , "shyam"}
club_B = {"ram" , "gita" , "hari"}
if club_A.isdisjoint(club_B):
    print("no overlapping members found between groups")
else:
    print("the following members exist in both groups", club_A.intersection(club_B))

#7.
required_tasks = {'Email', 'Report', 'Meeting'}
completed_tasks = {'Email', 'Report'}
if required_tasks.issubset(completed_tasks):
    print("all tasks done")
else:
    print(required_tasks - completed_tasks , "yet to be completed")
