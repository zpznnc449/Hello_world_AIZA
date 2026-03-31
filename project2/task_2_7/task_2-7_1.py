date = "2025-02-24"
print(f"Дата: {date}\n")
files = ["seq1", "seq2.fasta", "seq3.fa", "seq4"]
for name in files:
    if name.endswith((".fasta", ".fa")):
        print(f"{name} - уже есть")
    else:
        print(f"{name + '.fasta'} - добавлено")
print("\n" + "="*30 + "\n")
seq = "ATATACGCGTA"
print(f"ДНК: {seq}")
for letter in seq:
    print(letter, end=" ")