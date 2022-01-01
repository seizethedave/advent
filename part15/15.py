import heapq
import sys

def neighbors(height, width, pos):
	for dy, dx in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
		y = pos[0] + dy
		x = pos[1] + dx
		if 0 <= y < height and 0 <= x < width:
			yield (y, x)

def cost1(grid, pos):
	return grid[pos[0]][pos[1]]

def cost2(grid, pos):
	y, yr = divmod(pos[0], len(grid))
	x, xr = divmod(pos[1], len(grid[0]))
	val = grid[yr][xr] + y + x
	return ((val-1)%9) + 1

def scan(grid, height, width, cost_func):
	q = [(0, (0, 0))]
	seen = set()
	target = (height - 1, width - 1)

	while q:
		dist, pos = heapq.heappop(q)

		if pos == target:
			return dist
		elif pos in seen:
			continue

		seen.add(pos)

		for n in neighbors(height, width, pos):
			if n not in seen:
				cost = dist + cost_func(grid, n)
				heapq.heappush(q, (cost, n))

if __name__ == "__main__":
	grid = []
	for line in sys.stdin:
		grid.append([int(j) for j in line.rstrip()])

	print(scan(grid, len(grid), len(grid[0]), cost1))
	print(scan(grid, len(grid) * 5, len(grid[0]) * 5, cost2))