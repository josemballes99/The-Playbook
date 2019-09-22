import math
import random

fam = ["Joe", "Carl", "Mike"]
spot = ["First", "Second", "Last"]

for i in fam:
    x = random.randint(0,len(spot)-1)
    print(i + " gets " + spot[x])
    spot.pop(x)

    
