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
		seen := make(map[xy]struct{})
		sizes = append(sizes, basinSize(grid, pt, seen))
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

			for _, dydx := range []xy{{-1, 0}, {0, 1}, {1, 0}, {0, -1}} {
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

func basinSize(grid [][]int, lowPoint xy, seen map[xy]struct{}) int {
	val := grid[lowPoint.y][lowPoint.x]

	for _, dydx := range []xy{{-1, 0}, {0, 1}, {1, 0}, {0, -1}} {
		y := lowPoint.y + dydx.y
		x := lowPoint.x + dydx.x
		if y >= 0 && y < len(grid) && x >= 0 && x < len(grid[0]) {
			pt := xy{y, x}
			if _, ok := seen[pt]; !ok {
				if grid[y][x] < 9 && grid[y][x] > val {
					seen[pt] = struct{}{}
					basinSize(grid, pt, seen)
				}
			}
		}
	}

	return len(seen) + 1
}
