package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strings"
)

type Grid [][]int

func main() {
	var grid Grid
	var line []int
	reader := bufio.NewReader(os.Stdin)

	for {
		if r, _, err := reader.ReadRune(); err != nil {
			if err == io.EOF {
				if len(line) > 0 {
					grid = append(grid, line)
				}
				break
			}
			panic(err.Error())
		} else if r == '\n' {
			grid = append(grid, line)
			line = make([]int, 0)
		} else {
			line = append(line, int(r-'0'))
		}
	}

	flashes := 0
	firstAllFlash := 0

	for i := 0; firstAllFlash == 0; i++ {
		flashCount := grid.doStep()
		if i < 100 {
			flashes += flashCount
		}
		if flashCount == (len(grid) * len(grid[0])) {
			firstAllFlash = i + 1
		}
	}

	// part 1:
	fmt.Println(flashes)

	// part 2:
	fmt.Println(firstAllFlash)
}

func (grid Grid) String() string {
	var s strings.Builder
	for _, line := range grid {
		fmt.Fprintln(&s, line)
	}
	return s.String()
}

func (grid Grid) flash(y, x int) {
	type coord struct{ y, x int }
	grid[y][x] = -1

	for _, d := range [...]coord{{-1, 0}, {-1, 1}, {0, 1}, {1, 1}, {1, 0}, {1, -1}, {0, -1}, {-1, -1}} {
		yy := y + d.y
		xx := x + d.x
		if yy >= 0 && yy < len(grid) && xx >= 0 && xx < len(grid[0]) && grid[yy][xx] != -1 {
			grid[yy][xx]++
			if grid[yy][xx] > 9 {
				grid.flash(yy, xx)
			}
		}
	}
}

func (grid Grid) doStep() int {
	for r, line := range grid {
		for c := range line {
			grid[r][c]++
		}
	}

	for r, line := range grid {
		for c, num := range line {
			if num > 9 {
				grid.flash(r, c)
			}
		}
	}

	flashes := 0

	for r, line := range grid {
		for c, num := range line {
			if num == -1 {
				flashes++
				grid[r][c] = 0
			}
		}
	}

	return flashes
}
