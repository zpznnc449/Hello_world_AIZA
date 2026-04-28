a = [1, 2, 3, 4, 5, 6, -7, 8]
n = len(a)

pos = 0

for i in range(n):
    if a[i] > 0:
        pos = pos + 1
        i = i + 1
    else: i = i + 1
print("Количество положительных элементов массива:", pos)
