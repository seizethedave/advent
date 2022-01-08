package main

import (
	"bufio"
	"encoding/hex"
	"fmt"
	"io"
	"os"

	"github.com/pkg/errors"
)

const (
	TypeLiteral int = 4
)

type bitReader struct {
	io.ByteReader
	buf     byte
	balance int
	offset  int
}

func (r *bitReader) readBits(bits int) (int, error) {
	var ret int

	for bits > 0 {
		if r.balance == 0 {
			buf, err := r.ReadByte()
			if err != nil {
				return 0, err
			}
			r.buf = buf
			r.balance = 8
		}

		ret <<= 1
		if (r.buf & (1 << (r.balance - 1))) != 0 {
			ret |= 1
		}

		r.balance--
		bits--
		r.offset++
	}

	return ret, nil
}

func main() {
	bufreader := bufio.NewReader(hex.NewDecoder(os.Stdin))
	bitreader := &bitReader{bufreader, 0, 0, 0}

	sum, err := readPacket(bitreader)
	if err != nil {
		panic(err.Error())
	}
	fmt.Println(sum)
}

func readLiteral(r *bitReader) (int, error) {
	val := 0
	cont := true

	for cont {
		word, err := r.readBits(5)
		if err != nil {
			return 0, err
		}
		cont = (word & 0b10000) != 0
		val = (val << 4) | (word & 0b01111)
	}

	return val, nil
}

func readPacket(r *bitReader) (int, error) {
	versum := 0

	packetVers, err := r.readBits(3)
	if err != nil {
		return 0, err
	}

	versum += int(packetVers)

	packetType, err := r.readBits(3)
	if err != nil {
		return 0, err
	}

	if packetType == TypeLiteral {
		_, err := readLiteral(r)
		if err != nil {
			return 0, errors.Wrap(err, "reading literal")
		}
	} else {
		// an operator.
		lengthFlag, err := r.readBits(1)
		if err != nil {
			return 0, err
		}
		switch lengthFlag {
		case 1:
			subpackets, err := r.readBits(11)
			if err != nil {
				return 0, err
			}

			for i := 0; i < subpackets; i++ {
				vers, err := readPacket(r)
				if err != nil {
					return 0, errors.Wrap(err, "read subpacket")
				}
				versum += vers
			}
		case 0:
			length, err := r.readBits(15)
			if err != nil {
				return 0, err
			}

			for begin := r.offset; r.offset < begin+length; {
				vers, err := readPacket(r)
				if err != nil {
					return 0, errors.Wrap(err, "read subpacket")
				}
				versum += vers
			}
		}
	}

	return versum, nil
}
