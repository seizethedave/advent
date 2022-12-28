#include <iostream>
#include <iterator>
#include <string>
#include <unordered_map>
#include <set>

// To build:
// g++ 07a.cpp -std=c++2a
// cat input.txt | ./a.out

class Deps {
public:
    std::unordered_map<std::string, std::set<std::string>> deps;

    void LoadStringReverseDeps(std::string& str) {
        
        auto bags = str.find(" bags");
        std::string containerBag(str.begin(), str.begin() + bags);
        str.erase(0, bags + 14);

        // Now str is of form
        //     "1 bright magenta bag, 1 posh lavender bag, 2 dark gray bags, 1 wavy lime bag."
        // or
        //     "no other bags."
    
        if (str.starts_with("no")) {
            return;
        }
        do {
            str.erase(0, 2);
            bags = str.find(" bag");
            std::string contained(str.begin(), str.begin() + bags);
            this->deps[containerBag].insert(contained);
            str.erase(0, bags + 4);
            str.erase(
                0,
                str.starts_with("s") ? 3 : 2
            );
        } while (str.length() > 0);
    }

    bool ItemCanContain(const std::string& item, const std::string& target) {
        // DFS to see if item contains target, directly or indirectly.
        auto res = this->deps.find(item);
        if (res == this->deps.end()) {
            return false;
        }
        auto items = res->second;
        if (items.contains(target)) {
            return true;
        }
        for (auto const& s : items) {
            if (this->ItemCanContain(s, target)) {
                return true;
            }
        }
        return false;
    }

    int CountItemsTargeting(const std::string& target) {
        int count = 0;
        for (auto const& [k, v] : this->deps) {
            if (k != target && this->ItemCanContain(k, target)) {
                count++;
            }
        }
        return count;
    }

    void PrintDeps() const {
        for (auto const& [k, v] : this->deps) {
            std::cout << k << std::endl;
            for (auto const& s : v) {
                std::cout << "   " << s << std::endl;
            }
        }
    }
};

int main(int argc, char** argv) {
    Deps deps;
    std::string line;

    while (std::getline(std::cin, line)) {
        deps.LoadStringReverseDeps(line);
    }

    std::cout << deps.CountItemsTargeting("shiny gold") << std::endl;
    return 0;
}