

with open("input.txt", "r") as f:
    lines = f.read().splitlines()


c = 0
for line in lines:
    elf1, elf2 = line.split(",")
    elf1_lo, elf1_hi = map(int, elf1.split("-"))
    elf2_lo, elf2_hi = map(int, elf2.split("-"))
    if elf1_lo <= elf2_lo and elf2_hi <= elf1_hi:
        c += 1
    elif elf2_lo <= elf1_lo and elf1_hi <= elf2_hi:
        c += 1
    elif elf1_lo <= elf2_lo <= elf1_hi <= elf2_hi:
        c += 1
    elif elf2_lo <= elf1_lo <= elf2_hi <= elf1_hi:
        c += 1


print(c)
