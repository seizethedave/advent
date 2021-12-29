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

	rules := make(map[string]rune)

	for sc.Scan() {
		var left string
		var right rune
		n, err := fmt.Sscanf(sc.Text(), "%s -> %c", &left, &right)
		if err == io.EOF {
			break
		} else if err != nil {
			panic(err.Error())
		} else if n != 2 {
			panic("non-two sscanf")
		}
		rules[left] = right
	}

	for i := 0; i < 10; i++ {
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

func doStep(str *list.List, rules map[string]rune) {
	var prev rune
	for e := str.Front(); e != nil; e = e.Next() {
		if prev != 0 {
			pair := string([]rune{prev, e.Value.(rune)})
			if insertion, ok := rules[pair]; ok {
				str.InsertBefore(insertion, e)
			}
		}
		prev = e.Value.(rune)
	}
}
