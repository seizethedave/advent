#include <fstream>
#include <iostream>
#include <string>
#include <cstdio>
#include <functional>
#include <map>
#include <sstream>

// To build:
// g++ 04a.cpp -std=c++11

const char* Filename = "advent04.txt";

class Passport {
public:
    std::map<std::string, std::string> data;

    void Assign(const std::string&& key, std::string&& value) {
        if (key == "byr" || key == "iyr" || key == "eyr" || key == "hgt"
            || key == "hcl" || key == "ecl" || key == "pid") {

            this->data[key] = value;
        }
    }

    void Clear() {
        this->data.clear();
    }

    bool Valid() {
        return this->data.size() >= 7;
    }
};

int main(int argc, char** argv) {
    std::ifstream input(Filename, std::ios::in);
    std::string line;

    int numValid = 0;
    bool needsNew = true;

    Passport p;

    while (std::getline(input, line)) {
        if (needsNew) {
            if (p.Valid()) {
                numValid++;
            }

            p.Clear();
            needsNew = false;
        }

        if (line == "") {
            needsNew = true;
        } else {
            // regular line with >=1 key:val pairs.
            std::istringstream str(line);
            std::string pair;
            char key[8];
            char val[128];
            while (str >> pair) {
                if (std::sscanf(pair.c_str(), "%3s:%s", key, val) == 2) {
                    p.Assign(std::string(key), std::string(val));
                }
            }
        }
    }

    if (p.Valid()) {
        numValid++;
    }

    std::cout << numValid << std::endl;

    return 0;
}