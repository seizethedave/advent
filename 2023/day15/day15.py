import sys

def do_hash(s):
    h = 0
    for c in s:
        h = ((h + ord(c)) * 17) % 256
    return h

if __name__ == "__main__":
    print(
        sum(do_hash(atom) for line in sys.stdin for atom in line.split(","))
    )