package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
)

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

	score := 0
	lows := lowPoints(grid)
	for _, l := range lows {
		score += 1 + l
	}
	fmt.Println(score)
}

func lowPoints(grid [][]int) []int {
	type xy struct {
		y, x int
	}
	var lows []int

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
				lows = append(lows, c)
			}
		}
	}

	return lows
}
