package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	s := bufio.NewScanner(os.Stdin)
	lines := 0
	var arr []int

	for s.Scan() {
		str := s.Text()
		if lines == 0 {
			length := len(str)
			arr = make([]int, length)
		}

		lines++

		for i, c := range str {
			if c == '1' {
				arr[i] += 1
			}
		}
	}

	gamma := 0

	for _, ct := range arr {
		gamma <<= 1
		if ct > lines-ct {
			gamma |= 1
		}
	}

	epsilon := ^gamma & (1<<len(arr) - 1)
	fmt.Println(gamma * epsilon)
}
