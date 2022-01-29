package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
)

func str2bools(s string) []bool {
	bools := make([]bool, len(s))
	for i, c := range s {
		bools[i] = (c == '#')
	}
	return bools
}

type coord struct {
	y, x int
}

type image struct {
	img                    map[coord]struct{}
	minX, maxX, minY, maxY int
}

func newImage() *image {
	return &image{
		img:  make(map[coord]struct{}),
		minX: math.MaxInt,
		maxX: math.MinInt,
		minY: math.MaxInt,
		maxY: math.MinInt,
	}
}

func (img *image) set(y, x int) {
	img.img[coord{y, x}] = struct{}{}

	if x < img.minX {
		img.minX = x
	}
	if x > img.maxX {
		img.maxX = x
	}
	if y < img.minY {
		img.minY = y
	}
	if y > img.maxY {
		img.maxY = y
	}
}

func (img *image) print() {
	for y := img.minY; y <= img.maxY; y++ {
		for x := img.minX; x <= img.maxX; x++ {
			if _, ok := img.img[coord{y, x}]; ok {
				fmt.Print("#")
			} else {
				fmt.Print(".")
			}
		}
		fmt.Println()
	}
}

func render(algo []bool, img *image) *image {
	bitAt := func(y, x int) int {
		if _, ok := img.img[coord{y, x}]; ok {
			return 1
		}
		return 0
	}

	output := newImage()

	for y := img.minY - 2; y <= img.maxY+2; y++ {
		for x := img.minX - 2; x <= img.maxX+2; x++ {
			num := (bitAt(y-1, x-1) << 8) | (bitAt(y-1, x) << 7) | (bitAt(y-1, x+1) << 6) |
				(bitAt(y, x-1) << 5) | (bitAt(y, x) << 4) | (bitAt(y, x+1) << 3) |
				(bitAt(y+1, x-1) << 2) | (bitAt(y+1, x) << 1) | bitAt(y+1, x+1)
			if algo[num] {
				output.set(y, x)
			}
		}
	}

	return output
}

func main() {
	s := bufio.NewScanner(os.Stdin)
	s.Scan()
	algo := str2bools(s.Text())
	s.Scan()

	img := newImage()

	for y := 0; s.Scan(); y++ {
		line := s.Text()
		for x, c := range line {
			if c == '#' {
				img.set(y, x)
			}
		}
	}

	//img.print()
	fmt.Println(len(img.img))
	img = render(algo, img)
	//img.print()
	fmt.Println(len(img.img))
	img = render(algo, img)
	//img.print()
	fmt.Println(len(img.img))
}
