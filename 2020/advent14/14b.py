import sys
import re
import itertools

class Machine:
    def __init__(self):
        self.memory = {}
        self.mask_x_positions = []
        self.mask_bits = 0

    def set_mask(self, mask):
        self.mask_x_positions = []
        self.mask_bits = 0
        for i, ch in enumerate(reversed(mask)):
            if ch == "X":
                self.mask_x_positions.append(i)
            elif ch == "1":
                self.mask_bits |= 1 << i

    def set_value(self, addr, val):
        for seq in itertools.product((0, 1), repeat=len(self.mask_x_positions)):
            # seq will take on ALL k-bit tuples (0, 0, 0), (0, 0, 1), ..., (1, 1, 1).
            mask = 0
            realmask = 0
            for i, bit in enumerate(seq):
                mask |= bit << self.mask_x_positions[i]
                realmask |= 1 << self.mask_x_positions[i]
            new_addr = ((addr | self.mask_bits) & ~realmask) | mask
            self.memory[new_addr] = val

    def sum_values(self):
        return sum(self.memory.values())

machine = Machine()

for line in sys.stdin:
    if line.startswith("mem"):
        addr, val = re.findall(r"mem\[(\d+)\] = (\d+)", line)[0]
        machine.set_value(int(addr), int(val))
    elif line.startswith("mask"):
        mask = line.split()[-1]
        machine.set_mask(mask)

print(machine.sum_values())