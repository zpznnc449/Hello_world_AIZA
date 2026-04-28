array = list(map(int, input('Введите ваши числа: ').split()))

res = 0
summa = 0
count = 0

for i in range(len(array)):
    if i % 2 == 0:
        summa += array[i]
        count += 1 

res = summa / count

print(res)
