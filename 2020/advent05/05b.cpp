#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

// To build:
// g++ 05b.cpp -std=c++11

const char* Filename = "advent05.txt";

uint8_t decode(const std::string& str, char signalChar) {
    uint8_t result = 0;
    uint8_t pow = 1 << (str.length() - 1);
    for (const char &c: str) {
        if (c == signalChar) {
            result |= pow;
        }
        pow >>= 1;
    }
    return result;
}

bool gapped(int i, int j) {
    return j == i + 2;
}

int main(int argc, char** argv) {
    std::ifstream input(Filename, std::ios::in);
    std::string line;
    std::vector<int> numbers;

    while (std::getline(input, line)) {
        std::string row(line, 0, 7);
        std::string col(line, 7, 3);
        int seatNumber = int(decode(row, 'B')) * 8 + int(decode(col, 'R'));
        numbers.push_back(seatNumber);
    }

    std::sort(numbers.begin(), numbers.end());
    auto it = std::adjacent_find(numbers.begin(), numbers.end(), gapped);
    std::cout << (*it + 1) << std::endl;
    return 0;
}