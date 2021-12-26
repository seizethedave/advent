package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

func main() {
	s := bufio.NewScanner(os.Stdin)
	lines := 0
	inset := make(map[int]string)
	var length int

	for s.Scan() {
		inset[lines] = s.Text()
		lines++
		if length == 0 {
			length = len(s.Text())
		}
	}

	oxygen := filter(inset, length, true)
	co2 := filter(inset, length, false)

	fmt.Println(oxygen * co2)
}

func filter(items map[int]string, length int, lt bool) int {
	for index := 0; index < length; index++ {
		zeroes := make(map[int]string)
		ones := make(map[int]string)

		for i, s := range items {
			if s[index] == '1' {
				ones[i] = s
			} else {
				zeroes[i] = s
			}
		}

		if (len(ones)*2 < len(items)) == lt {
			items = ones
		} else {
			items = zeroes
		}

		if len(items) == 1 {
			for _, s := range items {
				if val, err := strconv.ParseInt(s, 2, 32); err != nil {
					panic(err.Error())
				} else {
					return int(val)
				}
			}
		}
	}

	panic("failed to find the magic item")
}
