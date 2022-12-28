#include <fstream>
#include <iostream>
#include <string>

// To build:
// g++ 03a.cpp -std=c++11

const char Tree = '#';
const int NewlineLength = 1;
const char* Filename = "advent03.txt";

int main(int argc, char** argv) {
    std::ifstream input(Filename, std::ios::in);

    // Sniff map width:
    std::string line;
    std::getline(input, line);
    int width = line.length();

    int x = 0;
    int y = 0;
    int trees = 0;

    while (true) {
        int pos = (y * (width + NewlineLength)) + (x % width);
        input.seekg(pos);
        char ch = input.get();
        if (ch == EOF) {
            break;
        }
        if (ch == Tree) {
            trees++;
        }
        x += 3;
        y += 1;
    }

    std::cout << trees << std::endl;
    return 0;
}