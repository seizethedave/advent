package main

import (
	"os"
	"bufio"
	"fmt"
	"strconv"
)

const target = 2020

// To run:
// cat ../advent01.txt | go run main.go

func main() {
	items := make(map[int]struct{})
	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		val, err := strconv.Atoi(scanner.Text())
		if err != nil {
			panic(err)
		}
		items[val] = struct{}{}
		other := target - val
		if _, ok := items[other]; ok {
			fmt.Println(val * other)
		}
	}
}
