package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	s := bufio.NewScanner(os.Stdin)

	score := 0
	for s.Scan() {
		line := s.Text()
		score += scoreLine(line)
	}

	fmt.Println(score)
}

func scoreLine(line string) int {
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
				return scores[c]
			}
		}
	}

	return 0
}
