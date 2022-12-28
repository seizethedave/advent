#include <iostream>
#include <cstdio>
#include <cmath>

// To build:
//  g++ 12a.cpp -std=c++2a
//  cat input.txt | ./a.out

inline double deg2rad(int deg) {
    return deg * M_PI / 180.0;
}

class Navigator {
public:
    void Navigate(char action, int number) {
        switch (action) {
        case 'L':
            this->direction = (this->direction + number) % 360;
            break;
        case 'R':
            this->direction = (this->direction - number) % 360;
            break;
        case 'F':
            this->x += std::round(std::cos(deg2rad(this->direction)) * number);
            this->y += std::round(std::sin(deg2rad(this->direction)) * number);
            break;
        case 'N':
            this->y += number;
            break;
        case 'E':
            this->x += number;
            break;
        case 'S':
            this->y -= number;
            break;
        case 'W':
            this->x -= number;
            break;
        }
    }

    int Distance() const {
        return std::abs(this->x) + std::abs(this->y);
    }
private:
    int x = 0;
    int y = 0;
    int direction = 0;
};

int main(int argc, char** argv) {
    Navigator n;
    char action;
    int number;

    while (std::scanf("%c%i\n", &action, &number) == 2) {
        n.Navigate(action, number);
    }

    std::cout << n.Distance() << std::endl;
    return 0;
}