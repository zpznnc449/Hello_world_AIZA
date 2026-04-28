a = [1, 2, 3, 4, 5, 6, 7, 8]
n = len(a)

avg = 0

for i in range(n):
    avg = avg + a[i]
avg = avg/n
print("Среднее арифметическое элементов массива:", avg)
