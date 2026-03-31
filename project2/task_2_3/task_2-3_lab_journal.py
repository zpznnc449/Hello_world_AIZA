fio = input("ФИО: ")
date = input("Дата: ")
exp = input("Эксперимент: ")
print("Вывод (пустая строка - конец):")
lines = []
while line := input():
    lines.append(line)
w = 41
with open("journal.txt", "w", encoding="utf-8") as f:
    f.write("+" + "-" * w + "+\n")
    f.write(f"| Электронный лабораторный журнал{' ' * (w - 32)}|\n")
    f.write("+" + "-" * w + "+\n")
    f.write(f"| ФИО исследователя : {fio:<{w - 21}}|\n")
    f.write(f"| Дата              : {date:<{w - 21}}|\n")
    f.write(f"| Эксперимент       : {exp:<{w - 21}}|\n")
    f.write("+" + "-" * w + "+\n")
    f.write(f"| Вывод:{' ' * (w - 7)}|\n")
    for line in lines:
        while len(line) > w - 2:
            f.write(f"| {line[:w - 4]:<{w - 2}} |\n")
            line = line[w - 4:]
        f.write(f"| {line:<{w - 2}} |\n")
    f.write("+" + "-" * w + "+\n")