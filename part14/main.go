package main

import (
	"bufio"
	"container/list"
	"fmt"
	"io"
	"math"
	"os"
)

func main() {
	sc := bufio.NewScanner(os.Stdin)

	sc.Scan()
	str := list.New()
	for _, c := range sc.Text() {
		str.PushBack(c)
	}
	sc.Scan()

	rules := make(map[[2]rune]rune)

	for sc.Scan() {
		var left1, left2, right rune
		n, err := fmt.Sscanf(sc.Text(), "%c%c -> %c", &left1, &left2, &right)
		if err == io.EOF {
			break
		} else if err != nil {
			panic(err.Error())
		} else if n != 3 {
			panic("non-3 sscanf")
		}
		rules[[2]rune{left1, left2}] = right
	}

	for i := 0; i < 10; i++ {
		fmt.Println(i)
		doStep(str, rules)
	}

	// compute counts for each rune, then min/max.
	counts := make(map[rune]int)
	for e := str.Front(); e != nil; e = e.Next() {
		counts[e.Value.(rune)]++
	}

	min := math.MaxInt32
	max := 0

	for _, ct := range counts {
		if ct > max {
			max = ct
		}
		if ct < min {
			min = ct
		}
	}

	fmt.Println(max - min)
}

func doStep(str *list.List, rules map[[2]rune]rune) {
	var prev rune
	for e := str.Front(); e != nil; e = e.Next() {
		if prev != 0 {
			pair := [2]rune{prev, e.Value.(rune)}
			if insertion, ok := rules[pair]; ok {
				str.InsertBefore(insertion, e)
			}
		}
		prev = e.Value.(rune)
	}
}
