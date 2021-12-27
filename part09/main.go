package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"sort"
)

type xy struct {
	y, x int
}

var Cardinals = [...]xy{{-1, 0}, {0, 1}, {1, 0}, {0, -1}}

func main() {
	reader := bufio.NewReader(os.Stdin)
	var grid [][]int
	var line []int

	for {
		r, _, err := reader.ReadRune()
		if err != nil {
			if err == io.EOF {
				if len(line) > 0 {
					grid = append(grid, line)
				}
				break
			}
			panic(err.Error())
		}
		if r == '\n' {
			grid = append(grid, line)
			line = make([]int, 0)
		} else {
			line = append(line, int(r-'0'))
		}
	}

	// Part 1:

	score := 0
	pts := lowPoints(grid)
	for _, pt := range pts {
		score += 1 + grid[pt.y][pt.x]
	}
	fmt.Println(score)

	// Part 2:

	var sizes []int
	for _, pt := range pts {
		sizes = append(sizes, basinSize(grid, pt))
	}
	sort.Ints(sizes)
	l := len(sizes)
	fmt.Println(sizes[l-1] * sizes[l-2] * sizes[l-3])
}

func lowPoints(grid [][]int) []xy {
	var lowPts []xy

	for j, line := range grid {
		for i, c := range line {
			best := true

			for _, dydx := range Cardinals {
				y := j + dydx.y
				x := i + dydx.x
				if y >= 0 && y < len(grid) && x >= 0 && x < len(line) {
					if grid[y][x] <= c {
						best = false
						break
					}
				}
			}

			if best {
				lowPts = append(lowPts, xy{j, i})
			}
		}
	}

	return lowPts
}

func basinSize(grid [][]int, lowPoint xy) int {
	seen := make(map[xy]struct{})
	var scan func(xy)

	scan = func(pt xy) {
		val := grid[pt.y][pt.x]
		for _, dir := range Cardinals {
			y := pt.y + dir.y
			x := pt.x + dir.x
			if y >= 0 && y < len(grid) && x >= 0 && x < len(grid[0]) {
				neighbor := xy{y, x}
				if _, ok := seen[neighbor]; !ok {
					if grid[y][x] < 9 && grid[y][x] > val {
						seen[neighbor] = struct{}{}
						scan(neighbor)
					}
				}
			}
		}
	}

	scan(lowPoint)
	return len(seen) + 1
}
