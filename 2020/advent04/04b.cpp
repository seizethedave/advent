#include <fstream>
#include <iostream>
#include <string>
#include <unordered_map>
#include <sstream>
#include <regex>
#include <cstring>

// To build:
// g++ 04b.cpp -std=c++11

const char* Filename = "advent04.txt";

class Passport {
public:
    std::string birthYear;
    std::string issueYear;
    std::string expYear;
    std::string height;
    std::string hairColor;
    std::string eyeColor;
    std::string passportID;
    std::string countryID;

    void Assign(const std::string&& key, std::string&& value) {
        std::unordered_map<std::string, std::string*> keyMap = {
            {"byr", &this->birthYear},
            {"iyr", &this->issueYear},
            {"eyr", &this->expYear},
            {"hgt", &this->height},
            {"hcl", &this->hairColor},
            {"ecl", &this->eyeColor},
            {"pid", &this->passportID},
            {"cid", &this->countryID},
        };

        auto match = keyMap.find(key);
        if (match == keyMap.end()) {
            return;
        }
        auto fieldPtr = match->second;
        fieldPtr->assign(value);
    }

    void Clear() {
        this->birthYear.clear();
        this->issueYear.clear();
        this->expYear.clear();
        this->height.clear();
        this->hairColor.clear();
        this->eyeColor.clear();
        this->passportID.clear();
        this->countryID.clear();
    }

    bool Valid() {
        // Wrong language for this one.

        bool valid = true;
        try {
            int birth = std::stoi(this->birthYear);
            valid = 1920 <= birth && birth <= 2002;
        }
        catch (const std::invalid_argument& e) {
            valid = false;
        }
        if (!valid) {
            return false;
        }

        try {
            int issue = std::stoi(this->issueYear);
            valid = 2010 <= issue && issue <= 2020;
        }
        catch (const std::invalid_argument& e) {
            valid = false;
        }
        if (!valid) {
            return false;
        }

        try {
            int exp = std::stoi(this->expYear);
            valid = 2020 <= exp && exp <= 2030;
        }
        catch (const std::invalid_argument& e) {
            valid = false;
        }
        if (!valid) {
            return false;
        }

        int h;
        char type[8];
        if (std::sscanf(this->height.c_str(), "%i%s", &h, type) == 2) {
            if (std::strcmp(type, "cm") == 0) {
                valid = 150 <= h && h <= 193;
            } else if (std::strcmp(type, "in") == 0) {
                valid = 59 <= h && h <= 76;
            } else {
                valid = false;
            }
        } else {
            valid = false;
        }
        if (!valid) {
            return false;
        }

        std::regex hairExpr("#[0-9a-f]{6}");
        if (!std::regex_match(this->hairColor, hairExpr)) {
            return false;
        }

        valid = this->eyeColor == "amb" || this->eyeColor == "blu"
            || this->eyeColor == "brn" || this->eyeColor == "gry"
            || this->eyeColor == "grn" || this->eyeColor == "hzl"
            || this->eyeColor == "oth";
        if (!valid) {
            return false;
        }

        std::regex passportExpr("[0-9]{9}");
        if (!std::regex_match(this->passportID, passportExpr)) {
            return false;
        }

        return true;
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
                    p.Assign(
                        std::move(std::string(key)),
                        std::move(std::string(val))
                    );
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