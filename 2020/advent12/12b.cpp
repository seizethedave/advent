#include <iostream>
#include <cstdio>
#include <cmath>

// To build:
//  g++ 12b.cpp -std=c++2a
//  cat input.txt | ./a.out

inline double deg2rad(double deg) {
    return deg * M_PI / 180.0;
}

class Navigator {
public:
    void Navigate(char action, int number) {
        switch (action) {
        case 'L':
            this->Rotate(+number);
            break;
        case 'R':
            this->Rotate(-number);
            break;
        case 'F':
            this->shipX += this->waypointX * number;
            this->shipY += this->waypointY * number;
            break;
        case 'N':
            this->waypointY += number;
            break;
        case 'E':
            this->waypointX += number;
            break;
        case 'S':
            this->waypointY -= number;
            break;
        case 'W':
            this->waypointX -= number;
            break;
        }
    }

    void PrintLoc() const {
        std::cerr << this->shipX << ", " << this->shipY
            << " W: " << this->waypointX << ", " << this->waypointY
            << std::endl;
    }

    int Distance() const {
        return std::abs(this->shipX) + std::abs(this->shipY);
    }
private:
    int waypointX = 10;
    int waypointY = 1;
    int shipX = 0;
    int shipY = 0;

    void Rotate(int degrees) {
        double theta = deg2rad(degrees);
        double c = std::cos(theta);
        double s = std::sin(theta);
        int x2 = std::round(this->waypointX * c - this->waypointY * s);
        int y2 = std::round(this->waypointX * s + this->waypointY * c);
        this->waypointX = x2;
        this->waypointY = y2;
    }
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