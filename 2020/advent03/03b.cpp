#include <fstream>
#include <iostream>
#include <string>

// To build:
// g++ 03b.cpp -std=c++11

const char Tree = '#';
const int NewlineLength = 1;
const char* Filename = "advent03.txt";

int64_t countTrees(std::ifstream& input, int width, int dx, int dy) {
    int x = 0;
    int y = 0;
    int64_t trees = 0;
    // Clear prior EOF/fail state.
    input.clear();

    while (true) {
        int pos = (y * (width + NewlineLength)) + (x % width);
        input.seekg(pos);
        char ch = input.get();
        if (ch == EOF) {
            break;
        } else if (ch == Tree) {
            trees++;
        }
        x += dx;
        y += dy;
    }
    return trees;
}

int main(int argc, char** argv) {
    std::ifstream input(Filename, std::ios::in);

    // Sniff map width:
    std::string line;
    std::getline(input, line);
    int width = line.length();

    int64_t trees = countTrees(input, width, 1, 1)
        * countTrees(input, width, 3, 1)
        * countTrees(input, width, 5, 1)
        * countTrees(input, width, 7, 1)
        * countTrees(input, width, 1, 2);

    std::cout << trees << std::endl;
    return 0;
}