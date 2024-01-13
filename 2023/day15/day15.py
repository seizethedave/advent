import sys

def do_hash(s):
    h = 0
    for c in s:
        h = ((h + ord(c)) * 17) % 256
    return h

if __name__ == "__main__":
    total = 0
    for line in sys.stdin:
        line = line.rstrip()
        for atom in line.split(","):
            total += do_hash(atom)
    print(total)
            