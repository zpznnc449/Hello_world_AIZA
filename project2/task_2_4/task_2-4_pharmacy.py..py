total = int(input("Введите общее количество произведенных капсул: "))
pack_size = int(input("Введите количество капсул в одной упаковке: "))
full_packs = total // pack_size
remainder = total % pack_size
print("\n--- Отчет фасовочного цеха ---")
print(f"Полных упаковок: {full_packs}")
print(f"Остаток капсул: {remainder}")