#include <iostream>
#include <vector>
#include <unordered_map>
#include <string>

// Build: g++ day14.cpp -std=c++20

enum Item {
    Empty,
    Rock,
    Cube,
};

enum Dir {
    North,
    West,
    South,
    East,
};

class grid {
public:
    std::vector<Item> items;
    size_t width;
    Dir dir = North;

    void rotate() {
        switch (this->dir) {
            case North:
            this->dir = West;
            break;
            case West:
            this->dir = South;
            break;
            case South:
            this->dir = East;
            break;
            case East:
            this->dir = North;
            break;
        }
    }

    size_t height() const {
        return this->items.size() / this->width;
    }

    void reserve(size_t s) {
        this->items.reserve(s);
        while (s > this->items.size()) {
            this->items.emplace_back(Empty);
        }
    }

    Item& get(int y, int x) {
        int h = this->height();
        int w = this->width;

        switch (this->dir) {
            case North:
            break;
            case East:
            std::swap(y, x);
            x = w - x - 1;
            break;
            case South:
            y = h - y - 1;
            x = w - x - 1;
            break;
            case West:
            std::swap(y, x);
            y = h - y - 1;
            break;
        }

        return this->items.at(y * w + x);
    }

    void set(int y, int x, Item item) {
        this->items[y * this->width + x] = item;
    }

    void print() {
        // Always print pointing north.
        Dir tmp = this->dir;
        this->dir = North;

        std::cout << "D: " << this->dir << std::endl;
        for (int y = 0; y < this->height(); y++) {
            for (int x = 0; x < this->width; x++) {
                Item val = this->get(y, x);
                if (val == Rock) {
                    std::cout << "O";
                } else if (val == Empty) {
                    std::cout << ".";
                } else if (val == Cube) {
                    std::cout << "#";
                }
            }
            std::cout << std::endl;
        }
        std::cout << std::endl;

        this->dir = tmp;
    }

    int findMoveRow(int y, int x) {
        int best = y;
        for (int yy = y - 1; yy >= 0; yy--) {
            if (this->get(yy, x) == Empty) {
                best = yy;
            } else {
                break;
            }
        }
        return best;
    }

    void dragRocks() {
        for (int y = 0; y < this->height(); y++) {
            for (int x = 0; x < this->width; x++) {
                if (this->get(y, x) == Rock) {
                    int moveRow = this->findMoveRow(y, x);
                    if (moveRow != y) {
                        std::swap(this->get(y, x), this->get(moveRow, x));
                    }
                }
            }
        }
    }

    void cycle() {
        for (int i = 0; i < 4; i++) {
            this->dragRocks();
            this->rotate();
        }
    }

    int load() {
        // Always calculate pointing north.
        Dir tmp = this->dir;
        this->dir = North;

        int score = 0;
        int y = 0;
        int x = 0;
        int rows = this->height();

        for (int y = 0; y < rows; y++) {
            for (int x = 0; x < this->width; x++) {
                if (this->get(y, x) == Rock) {
                    score += rows - y;
                }
            }
        }

        this->dir = tmp;
        return score;
    }

    std::string fingerprint() const {
        std::string val(this->items.size(), '0');
        size_t i = 0;
        for (auto c : this->items) {
            if (c == Rock) {
                val[i] = '1';
            }
            i++;
        }
        return val;
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

        for (char c : l) {
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

    // g.dragRocks();
    // std::cout << "Part 1: " << g.load() << std::endl;
    // return 0;

    const int64_t lim = 1000000000;

    std::vector<int64_t> history;
    std::unordered_map<std::string, size_t> seen;

    for (int64_t i = 0; i < lim; i++) {
        g.cycle();
        int val = g.load();
        auto print = g.fingerprint();
        auto found = seen.find(print);
        if (found != seen.end()) {
            // Found a cycle.
            int64_t cycleLen = i - found->second;
            size_t cycleBegin = found->second;
            int64_t ultimateValue = history[cycleBegin + ((lim - cycleBegin) % cycleLen) - 1];

            std::cout << "Part 2: " << ultimateValue << std::endl;
            break;
        }

        history.push_back(val);
        seen[print] = i;
    }
}
