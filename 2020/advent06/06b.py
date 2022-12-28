import sys
from collections import Counter

"""
To run:
    cat input.txt | python3 06b.py
"""

group_size = 0
all_present_count = 0
group_votes = Counter()

for line in sys.stdin:
    line = line.strip()
    if not line:
        all_present_count += len([
            v for v in group_votes.values() if v == group_size
        ])
        group_size = 0
        group_votes.clear()
    else:
        group_size += 1
        group_votes.update(line)

all_present_count += len([
    v for v in group_votes.values() if v == group_size
])
print(all_present_count)