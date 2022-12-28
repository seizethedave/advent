#include <fstream>
#include <iostream>
#include <string>

// To build:
// g++ 05a.cpp -std=c++11

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

int main(int argc, char** argv) {
    std::ifstream input(Filename, std::ios::in);
    std::string line;
    int highest = 0;

    while (std::getline(input, line)) {
        std::string row(line, 0, 7);
        std::string col(line, 7, 3);

        int seatNumber = int(decode(row, 'B')) * 8 + int(decode(col, 'R'));
        highest = std::max(highest, seatNumber);
    }

    std::cout << "highest = " << highest << std::endl;

    return 0;
}