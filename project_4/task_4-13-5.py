n = int(input("Количество чисел: "))
max_value = float(input("Число 1: "))
i = 2
while i <= n:
    x = float(input(f"Введите число {i}: "))
    if x > max_value:
        max_value = x
    i = i + 1
print("Максимальное число:", max_value)