package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
)

type coordinate struct {
	x, y int
}

type image struct {
	coordinates   map[coordinate]struct{}
	width, height int
}

func newImage() *image {
	return &image{
		coordinates: make(map[coordinate]struct{}),
	}
}

func (im *image) add(x, y int) {
	im.coordinates[coordinate{x, y}] = struct{}{}
	if x > im.width {
		im.width = x
	}
	if y > im.height {
		im.height = y
	}
}

func (im *image) foldUp(row int) {
	im.height = row - 1
	for i := 0; i <= im.width; i++ {
		for j := 0; j <= im.height; j++ {
			destJ := 2*row - j
			if _, ok := im.coordinates[coordinate{i, destJ}]; ok {
				im.coordinates[coordinate{i, j}] = struct{}{}
			}
		}
	}
}

func (im *image) foldLeft(col int) {
	im.width = col - 1
	for i := 0; i <= im.width; i++ {
		destI := 2*col - i
		for j := 0; j <= im.height; j++ {
			if _, ok := im.coordinates[coordinate{destI, j}]; ok {
				im.coordinates[coordinate{i, j}] = struct{}{}
			}
		}
	}
}

func (im *image) dots() int {
	num := 0
	for r := 0; r <= im.height; r++ {
		for c := 0; c <= im.width; c++ {
			if _, ok := im.coordinates[coordinate{c, r}]; ok {
				num++
			}
		}
	}
	return num
}

func (im *image) String() string {
	var b strings.Builder

	for r := 0; r <= im.height; r++ {
		for c := 0; c <= im.width; c++ {
			if _, ok := im.coordinates[coordinate{c, r}]; ok {
				b.WriteByte('X')
			} else {
				b.WriteByte(' ')
			}
		}
		b.WriteByte('\n')
	}

	return b.String()
}

func main() {
	img := newImage()

	s := bufio.NewScanner(os.Stdin)
	for s.Scan() {
		if s.Text() == "" {
			break
		}
		coords := strings.Split(s.Text(), ",")
		x, err := strconv.Atoi(coords[0])
		if err != nil {
			panic(err.Error())
		}
		y, err := strconv.Atoi(coords[1])
		if err != nil {
			panic(err.Error())
		}
		img.add(x, y)
	}

	// process folds
	firstFold := true

	for s.Scan() {
		var dir rune
		var loc int
		n, err := fmt.Sscanf(s.Text(), "fold along %c=%d", &dir, &loc)
		if err == io.EOF {
			break
		} else if err != nil {
			panic(err.Error())
		}
		if n != 2 {
			panic("non-two scanf")
		}

		switch dir {
		case 'x':
			img.foldLeft(loc)
		case 'y':
			img.foldUp(loc)
		}

		if firstFold {
			fmt.Println("dots after first fold:", img.dots())
			firstFold = false
		}
	}

	fmt.Println(img)
}
