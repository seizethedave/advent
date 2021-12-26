package main

import (
	"fmt"
	"io"
	"os"
)

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

		if !(x1 == x2 || y1 == y2) {
			continue
		}

		if x1 == x2 && y1 == y2 {
			// A single point.
			if seenAdd(x1, y1) {
				crossings++
			}
		} else if x1 != x2 {
			if x1 > x2 {
				x1, x2 = x2, x1
			}
			for x := x1; x <= x2; x++ {
				if seenAdd(x, y1) {
					crossings++
				}
			}
		} else if y1 != y2 {
			if y1 > y2 {
				y1, y2 = y2, y1
			}
			for y := y1; y <= y2; y++ {
				if seenAdd(x1, y) {
					crossings++
				}
			}
		}
	}
	fmt.Println(crossings)
}
