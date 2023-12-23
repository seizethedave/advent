#include <iostream>
#include <vector>

// Build: g++ day14.cpp -std=c++20

enum Item {
    Empty,
    Rock,
    Cube,
};

class grid {
public:
    std::vector<Item> items;
    size_t width;

    void reserve(size_t s) {
        this->items.reserve(s);
        while (s > this->items.size()) {
            this->items.emplace_back(Empty);
        }
    }

    void set(int y, int x, Item item) {
        this->items[y * this->width + x] = item;
    }

    Item& get(int y, int x) {
        return this->items.at(y * this->width + x);
    }

    int findMoveRow(int y, int x) {
        int best = y;
        for (int yy = y - 1; yy >= 0; yy--) {
            Item val = this->get(yy, x);
            if (val == Empty) {
                best = yy;
            } else {
                break;
            }
        }
        return best;
    }

    void dragRocks() {
        int y = 0;
        int x = 0;
        int rows = this->items.size() / this->width;

        for (auto& val : this->items) {
            if (x == this->width) {
                y++;
                x = 0;
            }
            if (val == Rock) {
                int moveRow = this->findMoveRow(y, x);
                if (moveRow != y) {
                    std::swap(this->get(y, x), this->get(moveRow, x));
                }
            }
            x++;
        }
    }

    int score() const {
        int total = 0;
        int y = 0;
        int x = 0;
        int rows = this->items.size() / this->width;

        for (auto& val : this->items) {
            if (x == this->width) {
                y++;
                x = 0;
            }
            if (val == Rock) {
                total += rows - y;
            }
            x++;
        }

        return total;
    }
};

int main() {
    std::vector<std::string> lines;
    std::string line;
    grid g;

    // Pre-read to learn width.

    while (std::getline(std::cin, line)) {
        g.width = line.size();
        lines.push_back(line);
    }

    g.reserve(g.width * lines[0].size());
    int y = 0;

    for (std::string& l : lines) {
        int x = 0;

        for (char& c : l) {
            Item val;
            switch (c) {
            case '.':
                val = Empty;
                break;
            case 'O':
                val = Rock;
                break;
            case '#':
                val = Cube;
                break;
            }

            g.set(y, x, val);
            x++;
        }

        y++;
    }

    g.dragRocks();

    std::cout << g.score() << std::endl;
}