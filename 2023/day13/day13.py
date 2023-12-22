import sys

Ash = "."
Rock = "#"

def poly_list_push(listref: list, i: int, val: int):
    """
    Append to a base-2 polynomial. Assumes each push happens in order: A push
    for index 11 should be immediately followed by a push for index 12.
    """
    try:
        total = listref[i]
    except IndexError:
        listref.append(0)
        total = 0
    listref[i] = (total << 1) + val

def find_reflection(listref: list, delta_bits: int):
    """
    This is an O(N^2) list reflection scan. I believe there's another O(N)
    implementation of this that iteratively constructs unique polynomials, but I
    lost steam on that train of thought.

    Since each number in the list is a base-2 polynomial, we can use the bit
    count of the difference between two of them to determine how many original
    grid squares were different.
    (n bits different ==> n squares were different.)
    """
    for i in range(1, len(listref)):
        w = min(i, len(listref) - i)
        l = listref[i-w:i]
        r = listref[i:i+w]
        if sum(abs(a-b).bit_count() for a, b in zip(l, r[::-1])) == delta_bits:
            return i
    return 0

class Grid:
    def __init__(self):
        self.row_poly = []
        self.col_poly = []
    
    def reflect_score(self, delta_bits):
        return (
            find_reflection(self.row_poly, delta_bits) * 100 +
            find_reflection(self.col_poly, delta_bits)
        )
    
    def poly_push_row(self, i: int, val: int):
        poly_list_push(self.row_poly, i, val)

    def poly_push_col(self, i: int, val: int):
        poly_list_push(self.col_poly, i, val)

    def __repr__(self):
        return "{}, {}".format(self.row_poly, self.col_poly)

if __name__ == "__main__":
    g = Grid()
    grids = [g]
    gy = 0
    for y, row in enumerate(sys.stdin):
        row = row.rstrip()
        if not row:
            g = Grid()
            grids.append(g)
            gy = 0
            continue

        for x, c in enumerate(row.rstrip()):
            val = int(c == Rock)
            g.poly_push_row(gy, val)
            g.poly_push_col(x, val)

        gy += 1

    #for i, g in enumerate(grids):
    #    print(i, g.reflect_score(0), g.reflect_score(1))

    print("%%%%%%")
    print(sum(g.reflect_score(0) for g in grids))
    print(sum(g.reflect_score(1) for g in grids))
