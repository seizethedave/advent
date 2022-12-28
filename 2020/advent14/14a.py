import sys
import re

class Machine:
    def __init__(self):
        self.memory = {}
        self.mask_mask = 0
        self.mask_bits = 0

    def set_mask(self, mask):
        self.mask_mask = 0
        self.mask_bits = 0
        for i, ch in enumerate(reversed(mask)):
            if ch != "X":
                self.mask_mask |= 1 << i
                if ch == "1":
                    self.mask_bits |= 1 << i

    def set_value(self, addr, val):
        self.memory[addr] = (val & ~self.mask_mask) | self.mask_bits

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