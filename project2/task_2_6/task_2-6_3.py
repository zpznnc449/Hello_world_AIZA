phenotype = input("Введите фенотип группы крови (I, II, III, IV): ").strip().upper()
if phenotype == "I":
    print("Группа крови: 0 (I)")
elif phenotype == "II":
    print("Группа крови: A (II)")
elif phenotype == "III":
    print("Группа крови: B (III)")
elif phenotype == "IV":
    print("Группа крови: AB (IV)")
else:
    print("Такой группы крови не существует")