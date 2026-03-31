medium_name = input("Введите название питательной среды: ")
agar_concentration = input("Введите концентрацию агара (%): ")
sterilization_temp = input("Введите температуру стерилизации (°C): ")
with open("recipe.txt", "w", encoding="utf-8") as file:
    file.write(f"{medium_name}\n")
    file.write("Параметры:\n")
    file.write(f"  - Концентрация агара: {agar_concentration}%\n")
    file.write(f"  - Температура стерилизации: {sterilization_temp}°C\n")
print("\nФайл 'recipe.txt' успешно сформирован!")