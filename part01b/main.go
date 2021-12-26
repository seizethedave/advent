package main

import (
	"bufio"
	"container/list"
	"fmt"
	"os"
	"strconv"
)

func main() {
	s := bufio.NewScanner(os.Stdin)
	inc := 0
	sum := 0
	prevSum := -1
	hist := list.New()

	for s.Scan() {
		val, err := strconv.Atoi(s.Text())
		if err != nil {
			panic(err.Error())
		}

		_ = hist.PushBack(val)
		sum += val

		if hist.Len() >= 3 {
			if prevSum > -1 && sum > prevSum {
				inc++
			}

			prevSum = sum
			front := hist.Front()
			_ = hist.Remove(front)
			sum -= front.Value.(int)
		}
	}

	fmt.Println(inc)
}
