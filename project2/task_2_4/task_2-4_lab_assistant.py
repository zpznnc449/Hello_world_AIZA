volume = float(input("Введите нужный объём раствора (мл): "))
salt_mass = volume * 0.009
water_volume = volume - salt_mass
with open("recipe.txt", "w", encoding="utf-8") as file:
    file.write("ОТЧЕТ ПО ПРИГОТОВЛЕНИЮ:\n")
    file.write("-" * 23 + "\n")
    file.write(f"Общий объем: {volume:.2f} мл\n")
    file.write(f"Масса соли: {salt_mass:.2f} г\n")
    file.write(f"Объем воды: {water_volume:.2f} мл\n")
print("Рецепт сохранён в файл recipe.txt")