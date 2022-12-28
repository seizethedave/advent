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
	var values []int

	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		val, err := strconv.Atoi(scanner.Text())
		if err != nil {
			panic(err)
		}
		values = append(values, val)
	}

	for i, val1 := range values {
		for j, val2 := range values[i:] {
			for _, val3 := range values[j:] {
				if val1 + val2 + val3 == target {
					fmt.Println(val1 * val2 * val3)
					return
				}
			}
		}
	}
}
