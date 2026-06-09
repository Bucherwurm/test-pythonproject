for r in range(7):
    for c in range(35):  
        # Letter 1: A 
        if (c == 0 or c == 4) and (r != 0):
            print("*", end=" ")
        elif (c == 1 or c == 2 or c == 3) and (r == 0 or r == 3):
            print("*", end=" ")
        # Letter 2: R 
        elif (c == 6) and (r != 0):                    
            print("*", end=" ")
        elif (c == 7 or c == 8 or c == 9) and (r == 0 or r == 3):  
            print("*", end=" ")
        elif (c == 10) and (r == 1 or r == 2):        
            print("*", end=" ")
        elif (c == 9) and (r == 6):                    
            print("*", end=" ")
        elif (c == 8) and (r == 5):                    
            print("*", end=" ")
        elif (c == 7) and (r == 4):                    
            print("*", end=" ")
        # Letter 3: Y
        elif (c == 12 or c == 16) and (r == 0):
            print("*", end=" ")
        elif (c == 13 or c == 15) and (r == 1):
            print("*", end=" ")
        elif (c == 14) and (r >= 2):
            print("*", end=" ")
        # Letter 4: A
        elif (c == 18 or c == 22) and (r != 0):
            print("*", end=" ")
        elif (c == 19 or c == 20 or c == 21) and (r == 0 or r == 3):
            print("*", end=" ")
        # Letter 5: N
        elif (c == 24 or c == 30):
            print("*", end=" ")
        elif (c == 25 and r == 1):
            print("*", end=" ")
        elif (c == 26 and r == 2):
            print("*", end=" ")
        elif (c == 27 and r == 3):
            print("*", end=" ")
        elif (c == 28 and r == 4):
            print("*", end=" ")
        elif (c == 29 and r == 5):
            print("*", end=" ")
        else:
            print(end="  ")
    print()