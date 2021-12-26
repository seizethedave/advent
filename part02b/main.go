package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	horizontal := 0
	depth := 0
	aim := 0

	s := bufio.NewScanner(os.Stdin)

	for s.Scan() {
		atoms := strings.Split(s.Text(), " ")
		dir := atoms[0]
		amt, err := strconv.Atoi(atoms[1])
		if err != nil {
			panic(err.Error())
		}

		switch dir {
		case "forward":
			horizontal += amt
			depth += (amt * aim)
		case "up":
			aim -= amt
		case "down":
			aim += amt
		}
	}
	fmt.Println(horizontal * depth)
}
