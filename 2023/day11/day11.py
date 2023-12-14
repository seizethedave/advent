import sys
import itertools

if __name__ == "__main__":
    galaxies = []
    width = 0
    blankrows = set()
    blankcols = None
    for y, line in enumerate(sys.stdin):
        l = line.strip()

        if blankcols is None:
            blankcols = set(range(len(l)))

        blankrow = True
        for x, char in enumerate(l):
            if char != ".":
                blankrow = False
                blankcols.discard(x)
                galaxies.append((y, x))

        if blankrow:
            blankrows.add(y)

    def dist(src, dest, boost_size):
        sy, sx = src
        dy, dx = dest
        rawdistY = abs(dy - sy)
        for r in blankrows:
            if sy < r < dy or dy < r < sy:
                rawdistY += boost_size
        rawdistX = abs(dx - sx)
        for c in blankcols:
            if sx < c < dx or dx < c < sx:
                rawdistX += boost_size
        return rawdistY + rawdistX

    print(
        sum(
            dist(src, dest, boost_size=1) for src, dest in itertools.combinations(galaxies, 2)
        )
    )

    print(
        sum(
            dist(src, dest, boost_size=999_999) for src, dest in itertools.combinations(galaxies, 2)
        )
    )
