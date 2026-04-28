a = float(input("Введите число A: "))
b = float(input("Введите число B: "))
c = float(input("Введите число C: "))
d = float(input("Введите число D: "))

if a < b:
    if a < c:
        if a < d:
            min = a
        else: min = d
    else: 
        if c < d:
            min = c
        else: min = d
else:
    if b < c:
        if b < d:
            min = b
        else: min = d
    else: 
        if c < d:
            min = c
        else: min = d

print("Минимальное число:", min)