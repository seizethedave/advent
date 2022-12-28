#include <iostream>
#include <list>
#include <algorithm>

// To build:
// g++ 09b.cpp -std=c++2a
// cat input.txt | ./a.out

class SumWindow {
public:
    std::list<int64_t> items;
    int64_t sum;
    int64_t target;

    SumWindow(const int64_t target)
     : items(), sum(0), target(target) { }

    /**
     * Adds the value to the sliding window, reducing the window if it flows over.
     * Returns whether the window sums to the target.
     */
    bool Add(int64_t value) {
        this->items.push_front(value);
        this->sum += value;

        while (this->sum > this->target) {
            this->sum -= this->items.back();
            this->items.pop_back();
        }
        return this->sum == this->target;
    }

    int64_t Min() const {
        return *std::min_element(this->items.begin(), this->items.end());
    }
    int64_t Max() const {
        return *std::max_element(this->items.begin(), this->items.end());
    }
};

int main(int argc, char** argv) {
    SumWindow window(3199139634);
    int64_t value;
    while (std::cin >> value) {
        if (window.Add(value)) {
            std::cout << (window.Min() + window.Max()) << std::endl;
            break;
        }
    }
    return 0;
}