import time

myls = [70, 40, 32, 65, 78, 100, 1542, 42, 16, 2006, 2008, 72, 78, 100, 1542, 42, 16, 2006, 2008, 72, 78, 100, 1542, 42, 16, 2006, 2008, 72]

def findOut(x):
    odds = []
    evens = []
    for items in x:
        if items%2:
            odds.append(items)
        else:
            evens.append(items)
    if len(odds) == 1:
        print(odds[0])
    else:
        print(evens[0])

def oddoneout(list):
    even = 0
    odd = 0
    for i in list:
        if i % 2 == 0:
            even += 1
        elif i % 2 != 0:
            odd += 1
        else:
            print(f"Invalid list item {i} at index {list.index(i)}. Terminating.")
            return None
    if even > odd and odd != 0:
        for i in list:
            if i % 2 != 0:
                return i
    elif odd > even and even != 0:
        for i in list:
            if i % 2 == 0:
                return i
    elif odd == 0 or even == 0:
        print("There are no \"odd one out\" numbers in this list. Terminating.")
        return None
    elif odd == even:
        print("There are no \"odd one out\" numbers in this list, as the number of even numbers to the number of odd numbers is equal. Terminating.")
        return None
    else:
        print("Unknown error. Terminating.")
        return None

st1 = time.time()
findOut(myls)
et1 = time.time()

st2 = time.time()
oddoneout(myls)
et2 = time.time()

el1 = et1 - st1
el2 = et2 - st2

print(f"""
Mr. Long's function finished in {el1:10f} seconds.
Nola's function finished in {el2:10f} seconds.
""")
