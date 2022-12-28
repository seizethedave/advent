package main

import (
	"fmt"
	"io"
	"os"
)

// To run:
// cat ../advent02.txt | go run main.go

func main() {
	var low, hi int
	var c rune
	var password string

	numValid := 0

	for {
		n, err := fmt.Fscanf(os.Stdin, "%d-%d %c: %s\n", &low, &hi, &c, &password)
		if err != nil {
			if err == io.EOF {
				break
			}
			panic(err)
		}
		if n != 4 {
			panic("bad line format")
		}

		if validPassword(password, c, low, hi) {
			numValid++
		}
	}

	println(numValid)
}

func validPassword(password string, char rune, low, hi int) bool {
	ct := 0
	for _, c := range password {
		if c == char {
			ct++
		}
	}
	return low <= ct && ct <= hi
}