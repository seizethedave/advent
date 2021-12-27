package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
)

func main() {
	s := bufio.NewScanner(os.Stdin)

	part1score := 0

	var part2scores []int
	termScores := map[rune]int{')': 1, ']': 2, '}': 3, '>': 4}

	for s.Scan() {
		s, expected := scoreLine(s.Text())
		part1score += s

		if s == 0 && len(expected) > 0 {
			expScore := 0
			for i := range expected {
				expScore = expScore*5 + termScores[expected[len(expected)-1-i]]
			}
			part2scores = append(part2scores, expScore)
		}
	}

	fmt.Println(part1score)

	sort.Ints(part2scores)
	fmt.Println(part2scores[len(part2scores)/2])
}

func scoreLine(line string) (int, []rune) {
	entries := map[rune]rune{'[': ']', '<': '>', '{': '}', '(': ')'}
	scores := map[rune]int{')': 3, ']': 57, '}': 1197, '>': 25137}
	var expect []rune // A stack of closing runes to expect.

	for _, c := range line {
		if closer, ok := entries[c]; ok {
			expect = append(expect, closer)
		} else {
			if c == expect[len(expect)-1] {
				expect = expect[:len(expect)-1]
			} else {
				return scores[c], expect
			}
		}
	}

	return 0, expect
}
