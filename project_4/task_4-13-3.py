N = int(input("Введите число N: "))

factor = 1 

for i in range(1, N+1):
    factor = factor * i

print("Факториал N:",factor)
