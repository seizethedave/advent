import itertools
import re
import sys

I = lambda x, y, z: (x, y, z)
X = lambda x, y, z: (x, -z, y)
Y = lambda x, y, z: (z, y, -x)

"""
A tree of +90 deg rotate operations about X or Y axis. (e.g. XXY = Z and facing downward.)
Evaluating all paths from root to leaves = all 24 orientations.
"""
xforms = [
    (I, [
        (X, [
            (X, [
                (X, [
                    (Y, [
                        (X, []),
                    ])
                ]),
                (Y, [
                    (X, []),
                    (Y, [])
                ])
            ]),
            (Y, [
                (X, [
                    (X, [
                        (X, [])
                    ]),
                ]),
                (Y, [
                    (Y, [
                        (X, []),
                    ])
                ])
            ])
        ]),
        (Y, [
            (X, [
                (X, [
                    (X, [])
                ])
            ]),
            (Y, [
                (X, []),
                (Y, [
                    (X, []),
                ])
            ])
        ])
    ])
]

def translate(pt, skew):
    return (pt[0] + skew[0], pt[1] + skew[1], pt[2] + skew[2])

class Scanner(object):
    def __init__(self, num):
        self.num = num
        self.pos = None
        self.points = []

    def all_rotations(self):
        stack = [(self.points, xforms)]
        while stack:
            (pts, others) = stack.pop()
            for xf, next_xfs in others:
                changed_points = [xf(*p) for p in pts]
                yield changed_points
                stack.append((changed_points, next_xfs))

    def translated_points(self):
        return [translate(pt, self.pos) for pt in self.points]

    def match_with(self, other):
        my_points = sorted(self.points)
        s1 = set(my_points)

        for root1 in my_points:
            for other_points in other.all_rotations():
                other_points.sort()

                for root2 in other_points:
                    offset = (root1[0] - root2[0], root1[1] - root2[1], root1[2] - root2[2])
                    s2 = set(translate(pt, offset) for pt in other_points)
                    overlap = s1 & s2
                    if len(overlap) >= 12:
                        if self.pos is not None:
                            other.pos = translate(self.pos, offset)
                            print(f"{other.num}.pos <- {other.pos}")
                        else:
                            print(f"{self.num}.pos was None")
                        return True
        return False


def part1():
    scanners = []

    for line in sys.stdin:
        if line.startswith("---"):
            num = int(re.search(r"(\d+)", line).group(0))
            scanner = Scanner(num)
            scanners.append(scanner)
            continue

        try:
            a, b, c = line.split(",")
        except ValueError:
            continue
        scanner.points.append((int(a), int(b), int(c)))

    scanners[0].pos = (0, 0, 0)
    unmatched = set(scanners)
    unmatched.discard(scanners[0])
    matched = [scanners[0]]

    while matched:
        root = matched.pop()
        for other in list(unmatched):
            if root.match_with(other):
                unmatched.discard(root)
                unmatched.discard(other)
                matched.append(other)
                print(f"Match {root.num}, {other.num}")

    print(f"done matching. {len(unmatched)} / {len(scanners)}")

if __name__ == "__main__":
    part1()
