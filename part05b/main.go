package main

import (
	"fmt"
	"io"
	"os"
)

func slope(a, b int) int {
	switch {
	case a < b:
		return 1
	case a > b:
		return -1
	}
	return 0
}

func main() {
	seen := make(map[string]int)
	seenAdd := func(x, y int) bool {
		coord := fmt.Sprintf("%d,%d", x, y)
		seen[coord]++
		return seen[coord] == 2
	}

	crossings := 0

	for {
		var x1, y1, x2, y2 int
		_, err := fmt.Fscanf(os.Stdin, "%d,%d -> %d,%d\n", &x1, &y1, &x2, &y2)
		if err != nil {
			if err == io.EOF {
				break
			}
			panic(err.Error())
		}

		dx := slope(x1, x2)
		dy := slope(y1, y2)
		x := x1
		y := y1

		for {
			if seenAdd(x, y) {
				crossings++
			}

			x += dx
			y += dy

			if x == x2 && y == y2 {
				// process terminal point.
				if seenAdd(x, y) {
					crossings++
				}
				break
			}
		}
	}

	fmt.Println(crossings)
}
