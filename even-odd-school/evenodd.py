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
