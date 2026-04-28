a = [1, 5, 8, 4, 6, 14, 5, 22, 9]
n = len(a)

summ = 0
for i in range(n):
    if a[i] % 2 == 1:
        summ = summ + a[i]
        i = i + 1
    else: i = i + 1
print("Сумма нечетных элементов массива:", summ)
