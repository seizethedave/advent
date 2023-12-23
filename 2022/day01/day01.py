import sys

best_count = 0
elf_count = 0

for line in sys.stdin:
    line = line.strip()

    if line == "":
        best_count = max(best_count, elf_count)
        elf_count = 0
    else:
        elf_count += int(line)
else:
    best_count = max(best_count, elf_count)

print(best_count)