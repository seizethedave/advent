#include <iostream>
#include <list>
#include <vector>
#include <unordered_map>
#include <string>
#include <numeric>

constexpr int BOXCOUNT = 256;

int boxhash(const std::string& s) {
    int h = 0;
    for (char c : s) {
        h = ((h + (int)c) * 17) % BOXCOUNT;
    }
    return h;
}

class Box {
public:
    int boxNum = 0;
    std::list<int> lenses;
    std::unordered_map<std::string, std::list<int>::iterator> labelIndex;

    void remove(const std::string& label) {
        auto it = this->labelIndex.find(label);
        if (it != this->labelIndex.end()) {
            this->lenses.erase(it->second);
            this->labelIndex.erase(it);
        }
    }

    void put(const std::string& label, int focalLength) {
        auto it = this->labelIndex.find(label);
        if (it != this->labelIndex.end()) {
            // Replace in same position.
            auto lensIt = it->second;
            *lensIt = focalLength;
        } else {
            // Just add to front.
            this->lenses.push_front(focalLength);
            this->labelIndex.insert(std::make_pair(label, this->lenses.begin()));
        }
    }

    long score() const {
        int boxPower = 1 + this->boxNum;
        int slot = 1;
        int sum = 0;

        for (auto it = this->lenses.crbegin(); it != this->lenses.crend(); ++it) {
            auto v = *it;
            sum += boxPower * slot * v;
            slot++;
        }

        return sum;
    }
};

int main() {
    std::string item;

    Box boxes[BOXCOUNT];
    int boxNum = 0;
    for (Box &b : boxes) {
        b.boxNum = boxNum++;
    }

    while (std::getline(std::cin, item, ',')) {
        size_t pos;

        if ((pos = item.find("=")) != std::string::npos) {
            std::string label = item.substr(0, pos);
            int focalLength = item[pos+1] - '0';
            int hash = boxhash(label);
            boxes[hash].put(label, focalLength);
        } else {
            item.resize(item.length() - 1);
            int hash = boxhash(item);
            boxes[hash].remove(item);
        }
    }

    long s = 0;

    for (Box &b : boxes) {
        s += b.score();
    }

    std::cout << s << std::endl;

    return 0;
}
