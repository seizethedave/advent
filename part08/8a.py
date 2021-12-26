import sys

counts = 0
for line in sys.stdin:
	_, right = line.split("|")
	for a in right.strip().split(" "):
		if len(a) in [2, 3, 4, 7]:
			counts += 1
print(counts)
