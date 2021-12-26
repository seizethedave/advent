package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
)

const BoardSize = 5

type board [BoardSize][BoardSize]int

func main() {
	r := bufio.NewReader(os.Stdin)
	header, err := r.ReadString('\n')
	if err != nil {
		panic(err.Error())
	}

	header = strings.TrimRight(header, "\n")
	discarded, err := r.Discard(1)
	if err != nil {
		panic(err.Error())
	}
	if discarded != 1 {
		panic(fmt.Sprintf("discarded %d, not 1", discarded))
	}

	var boards []board

	for {
		b, err := readBoard(r)
		if err != nil {
			if err != io.EOF {
				fmt.Println(err.Error())
			}
			break
		}

		discarded, err := r.Discard(1)
		if err != nil {
			panic(err.Error())
		}
		if discarded != 1 {
			panic(fmt.Sprintf("discarded %d, not 1", discarded))
		}

		boards = append(boards, b)
	}

	/*
		// part 4a:
		for _, atom := range strings.Split(header, ",") {
			num, err := strconv.Atoi(atom)
			if err != nil {
				panic(err.Error())
			}

			for i := range boards {
				b := &boards[i]
				if b.mark(num) {
					fmt.Println(b.score() * num)
					return
				}
			}
		}
	*/

	// part 4b:
	lastScore := 0
	winners := make(map[int]struct{})
	for _, atom := range strings.Split(header, ",") {
		num, err := strconv.Atoi(atom)
		if err != nil {
			panic(err.Error())
		}
		for i := range boards {
			if _, ok := winners[i]; ok {
				// Skip boards that have won.
				continue
			}
			b := &boards[i]
			if b.mark(num) {
				lastScore = b.score() * num
				winners[i] = struct{}{}
			}
		}
	}
	fmt.Println(lastScore)
}

func readBoard(r *bufio.Reader) (board, error) {
	var brd board
	for i := 0; i < BoardSize; i++ {
		line, err := r.ReadString('\n')
		if err != nil {
			return board{}, err
		}

		for j, a := range strings.Fields(line) {
			num, err := strconv.Atoi(a)
			if err != nil {
				return board{}, err
			}
			brd[i][j] = num
		}
	}
	return brd, nil
}

// mark scans the board, marking a cell if its value is `num`, and returns
// whether that mark produced a winning board.
func (b *board) mark(num int) bool {
	for i := range b {
		for j := range b[i] {
			if b[i][j] == num {
				b[i][j] = 0
				return b.wins(i, j)
			}
		}
	}

	return false
}

// wins takes the (i, j) coordinate of a cell that was just marked, and returns
// whether that mark produced a winning board.
func (b *board) wins(i, j int) bool {
	allWin := true
	for col := range b[0] {
		if b[i][col] != 0 {
			allWin = false
			break
		}
	}

	if allWin {
		return true
	}

	allWin = true

	for row := range b {
		if b[row][j] != 0 {
			allWin = false
			break
		}
	}

	return allWin
}

func (b *board) score() int {
	score := 0
	for i := range b {
		for _, val := range b[i] {
			score += val
		}
	}
	return score
}
