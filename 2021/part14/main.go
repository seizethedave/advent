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
	pattern := sc.Text()
	str := list.New()
	for _, c := range pattern {
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
		doStep(str, rules)
	}

	// compute counts for each rune, then min/max.
	counts := make(map[rune]int)
	for e := str.Front(); e != nil; e = e.Next() {
		counts[e.Value.(rune)]++
	}

	{
		min, max := minmax(counts)
		fmt.Println(max - min)
	}

	{
		min, max := minmax(countChars(pattern, rules))
		fmt.Println(max - min + 1)
	}
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

type cacheKey struct {
	pair  [2]rune
	depth int
}

type cacheResult map[rune]int

func countChars(pattern string, rules map[[2]rune]rune) map[rune]int {
	cache := make(map[cacheKey]cacheResult)

	var visit func([2]rune, int) map[rune]int
	visit = func(pair [2]rune, depth int) map[rune]int {
		key := cacheKey{pair, depth}
		if res, ok := cache[key]; ok {
			return res
		}

		var result cacheResult

		if depth == 0 {
			result = make(cacheResult)
			result[pair[0]]++
			result[pair[1]]++
		} else if insertion, ok := rules[pair]; ok {
			result = make(cacheResult)
			// combine left & right in new result.
			for k, v := range visit([2]rune{pair[0], insertion}, depth-1) {
				result[k] = v
			}
			for k, v := range visit([2]rune{insertion, pair[1]}, depth-1) {
				result[k] += v
			}
			result[insertion]-- // don't double-count
		}

		if result != nil {
			cache[key] = result
		}
		return result
	}

	counts := make(map[rune]int)
	for i := 0; i < (len(pattern) - 1); i++ {
		pair := [2]rune{rune(pattern[i]), rune(pattern[i+1])}
		for k, v := range visit(pair, 40) {
			counts[k] += v
		}
	}
	return counts
}

func minmax(counts map[rune]int) (int, int) {
	min := math.MaxInt
	max := 0

	for _, ct := range counts {
		if ct > max {
			max = ct
		}
		if ct < min {
			min = ct
		}
	}
	return min, max
}
