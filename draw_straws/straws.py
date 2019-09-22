import math
import random

fam = ["Joe", "Bill", "Mike"]
room = ["First", "Second", "Last"]

for i in fam:
    x = random.randint(0,len(room)-1)
    print(i + " gets " + room[x])
    room.pop(x)

    
