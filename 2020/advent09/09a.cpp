#include <iostream>
#include <list>

// To build:
// g++ 09a.cpp -std=c++2a
// cat input.txt | ./a.out

class Cipher {
public:
    std::list<int64_t> window;
    size_t size = 0;

    bool Add(int64_t value) {
        const int windowSize = 25;
        if (this->size < windowSize) {
            this->window.push_front(value);
            this->size++;
            return true;
        }

        if (!this->IsValid(value)) {
            return false;
        }

        this->window.pop_back();
        this->window.push_front(value);
        return true;
    }

    bool IsValid(int64_t value) {
        for (auto i = this->window.begin(); i != this->window.end(); ++i) {
            auto j = i;
            for (++j; j != this->window.end(); ++j) {
                if (*i != *j && *i + *j == value) {
                    return true;
                }
            }
        }
        return false;
    }
};

int main(int argc, char** argv) {
    Cipher cipher;
    int64_t value;
    while (std::cin >> value) {
        if (!cipher.Add(value)) {
            std::cout << value << std::endl;
            break;
        }
    }
    return 0;
}