array = [11, 3, 2, 4, 6, 76, 23]
s = 0

for i in range(len(array)):
    if i % 2 != 0:
        s = s + array[i]

print("Сумма элементов с нечетными индексами:", s)