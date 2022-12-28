#include <iostream>
#include <cstdio>
#include <cinttypes>
#include <array>
#include <unordered_map>

/* NOTE:
    This was a good try but as C++ has no BigInt, it cannot sum
    all of the values in memory without overflowing. So I rewrote in in Python.
*/

// To build:
//  g++ 14a.cpp -std=c++2a -o 14a
//  cat input.txt | ./14a

using Addr = uint64_t;
using Value = uint64_t;

class Machine {
public:
    void SetMask(const std::string& mask) {
        Value m = 0;
        Value b = 0;
        size_t i = 0;

        for (auto it = mask.crbegin(); it != mask.crend(); ++it) {
            if (*it != 'X') {
                m |= (1 << i);
                if (*it == '1') {
                    b |= (1 << i);
                }
            }

            ++i;
        }

        this->maskMask = m;
        this->maskBits = b;
    }

    void SetMem(Addr addr, Value value) {
       Value newValue = this->maskBits | (value & ~this->maskMask);
       this->memory[addr] = newValue;
    }

    Value SumValues() const {
        Value sum = 0;
        for (auto const& [addr, val] : this->memory) {
            sum += val;
        }
        return sum;
    }
private:
    std::unordered_map<Addr, Value> memory;
    Value maskMask = 0;
    Value maskBits = 0;
};

int main(int argc, char** argv) {
    Machine m;
    std::string line;

    while (std::getline(std::cin, line)) {
        Addr addr;
        Value value;
        std::array<char, 40> mask;

        if (std::sscanf(line.c_str(), "mask = %s", mask.data()) == 1) {
            m.SetMask(mask.data());
        }
        else if (std::sscanf(line.c_str(), "mem[%" SCNu64 "] = %" SCNu64, &addr, &value) == 2) {
            m.SetMem(addr, value);
        }
    }

    std::cout << m.SumValues() << std::endl;

    return 0;
}