package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

func main() {
	s := bufio.NewScanner(os.Stdin)
	var prevVal int
	first := true
	inc := 0
	for s.Scan() {
		val, err := strconv.Atoi(s.Text())
		if err != nil {
			panic(err.Error())
		}

		if !first && val > prevVal {
			inc++
		}

		first = false
		prevVal = val
	}

	fmt.Println(inc)
}
