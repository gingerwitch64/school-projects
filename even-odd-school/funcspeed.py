import time

myls = [70, 40, 32, 65, 78, 100, 1542, 42, 16, 2006, 2008, 72, 78, 100, 1542, 42, 16, 2006, 2008, 72, 78, 100, 1542, 42, 16, 2006, 2008, 72]

def findOut(x):
    if x[0]%2 + x[1]%2 + x[2]%2 >= 2:
        modifier = 0
    else:
        modifier = 1
    for items in x:
        if items%2 == modifier:
            return items

def oddoneout(list):
    even = 0
    odd = 0
    for i in list:
        if i % 2 == 0:
            even += 1
        else:
            odd += 1
    if even > odd and odd != 0:
        for i in list:
            if i % 2 != 0:
                return i
    else:
        for i in list:
            if i % 2 == 0:
                return i

st1 = time.process_time()
findOut(myls)
et1 = time.process_time()

st2 = time.process_time()
oddoneout(myls)
et2 = time.process_time()

print(f"""
Mr. Long's function returns  {findOut(myls)}
Nola's function returns      {oddoneout(myls)}\
""")

el1 = et1 - st1
el2 = et2 - st2

print(f"""
Mr. Long's function finished in {el1:10f} seconds.
Nola's function finished in     {el2:10f} seconds.
""")
