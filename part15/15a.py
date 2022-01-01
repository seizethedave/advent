import heapq
import sys

def neighbors(grid, pos):
	for dy, dx in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
		y = pos[0] + dy
		x = pos[1] + dx
		if 0 <= y < len(grid) and 0 <= x < len(grid[0]):
			yield (y, x)

def scan(grid):
	q = [(0, (0, 0))]
	destination = (len(grid) - 1, len(grid[0]) - 1)
	seen = set()

	while q:
		dist, pos = heapq.heappop(q)

		if pos == destination:
			return dist
		elif pos in seen:
			continue

		seen.add(pos)

		for n in neighbors(grid, pos):
			if n not in seen:
				(ny, nx) = n
				heapq.heappush(q, (dist + grid[ny][nx], n))

if __name__ == "__main__":
	grid = []
	for line in sys.stdin.readlines():
		grid.append([int(j) for j in line.rstrip()])
	print(scan(grid))