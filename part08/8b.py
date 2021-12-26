import sys
from collections import defaultdict
from itertools import permutations

layouts = [
	[0, 1, 2, 4, 5, 6],    # 0
	[2, 5],                # 1
	[0, 2, 3, 4, 6],       # 2
	[0, 2, 3, 5, 6],       # 3
	[1, 2, 3, 5],          # 4
	[0, 1, 3, 5, 6],       # 5
	[0, 1, 3, 4, 5, 6],    # 6
	[0, 2, 5],             # 7
	[0, 1, 2, 3, 4, 5, 6], # 8
	[0, 1, 2, 3, 5, 6],    # 9
]

layout_lookup = {frozenset(digits): i for i, digits in enumerate(layouts)}

layouts_by_length = defaultdict(list)
for lay in layouts:
	layouts_by_length[len(lay)].append(lay)

def word_valid(word, assignment):
	return any(
		all(assignment[i] in word for i in layout)
		for layout in layouts_by_length[len(word)]
	)

def get_assignment(dictionary):
	for assignment in permutations('abcdefg'):
		if all(word_valid(word, assignment) for word in dictionary):
			return assignment
	return None

def get_value(patterns, values):
	corpus = patterns + values
	dictionary = set("".join(sorted(w)) for w in corpus)
	assignment = get_assignment(dictionary)
	c2i = {c: i for i, c in enumerate(assignment)}

	tally = 0
	for v in values:
		tally = tally * 10 + layout_lookup[frozenset(c2i[c] for c in v)]
	return tally

total = 0

for line in sys.stdin:
	if not line:
		break
	left, right = line.split("|")
	patterns = left.strip().split(" ")
	values = right.strip().split(" ")
	total += get_value(patterns, values)

print(total)
