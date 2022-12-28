#include <iostream>
#include <iterator>
#include <string>
#include <unordered_map>
#include <unordered_set>

// To build:
// g++ 07b.cpp -std=c++2a
// cat input.txt | ./a.out

struct Target {
    std::string target;
    int bagCount;

    Target(const std::string&& t, int&& ct) :
        target(t), bagCount(ct)
    {}
};

bool operator==(const Target& a, const Target& b) {
    return a.target == b.target && a.bagCount == b.bagCount;
}

namespace std
{
    template<> struct hash<Target>
    {
        std::size_t operator()(Target const& t) const noexcept
        {
            std::size_t h1 = std::hash<std::string>{}(t.target);
            std::size_t h2 = std::hash<int>{}(t.bagCount);
            return h1 ^ (h2 << 1);
        }
    };
}

class Deps {
public:
    std::unordered_map<std::string, std::unordered_set<Target>> deps;

    void LoadLine(std::string& str) {
        
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
            int qty = std::stoi(
                std::string(str.begin(), str.begin() + 1)
            );

            str.erase(0, 2);
            bags = str.find(" bag");
            std::string contained(str.begin(), str.begin() + bags);

            this->deps[containerBag].emplace(
                std::move(contained),
                std::move(qty)
            );

            str.erase(0, bags + 4);
            str.erase(
                0,
                str.starts_with("s") ? 3 : 2
            );
        } while (str.length() > 0);
    }

    int CountBagsRequired(const std::string& bag) {
        std::unordered_set<Target> s; 
        try {
            s = this->deps.at(bag);
        } catch (const std::out_of_range& e) {
            // Leaf bags are not added to the map.
            return 1;
        }

        int count = 1;
        for (auto const& t : s) {
            count += t.bagCount * this->CountBagsRequired(t.target);
        }
        return count;
    }

    void PrintDeps() const {
        for (auto const& [k, v] : this->deps) {
            std::cout << k << std::endl;
            for (auto const& s : v) {
                std::cout << "   " << s.target << " (" << s.bagCount << ")" << std::endl;
            }
        }
    }
};

int main(int argc, char** argv) {
    Deps deps;
    std::string line;

    while (std::getline(std::cin, line)) {
        deps.LoadLine(line);
    }

    // don't need to count the outer bag.
    int required = deps.CountBagsRequired("shiny gold") - 1;
    std::cout << required << std::endl;
    return 0;
}