#include <iostream>
#include <algorithm>
#include <numeric>
#include <vector>

// To build:
//  g++ 10a.cpp -std=c++2a
//  cat input.txt | ./a.out

int main(int argc, char** argv) {
    std::vector<int> items {0};
    int value;
    int highest = 0;

    while (std::cin >> value) {
        items.push_back(value);
        highest = std::max(highest, value);
    }

    items.push_back(highest + 3);
    std::sort(items.begin(), items.end());
    std::adjacent_difference(items.begin(), items.end(), items.begin());
    int ones = std::count(items.begin(), items.end(), 1);
    int threes = std::count(items.begin(), items.end(), 3);

    std::cout << (ones * threes) << std::endl;
    return 0;
}