import sys

"""
To run:
    cat input.txt | python3 06b.py
"""

vote_count = 0
group_votes = set()

for line in sys.stdin:
    line = line.strip()
    if not line:
        vote_count += len(group_votes)
        group_votes = set()
    else:
        group_votes.update(line)

vote_count += len(group_votes)
print(vote_count)