#include <iostream>
#include <vector>
#include <cstdio>
#include <cstring>

// To build:
// g++ 08b.cpp -std=c++2a
// cat input.txt | ./a.out

enum InstructionCode {
    NoOp,
    Jump,
    Accumulate,
};

struct Instruction {
    InstructionCode code;
    int number;
    Instruction(const InstructionCode&& c, const int&& n)
        : code(c), number(n)
        {}
};

bool interpret(const std::vector<Instruction>& program) {
    size_t p = 0;
    int value = 0;

    // A "have we visited this instruction yet" counter.
    std::vector<bool> seen(program.size(), false);

    while (true) {
        if (p + 1 > program.size()) {
            // exited normally.
            std::cout << value << std::endl;
            return true;
        } else if (seen[p]) {
            // infinite loop.
            return false;
        }

        auto instruction = program.at(p);
        seen[p] = true;

        switch (instruction.code) {
        case NoOp:
            p++;
            break;
        case Jump:
            p += instruction.number;
            break;
        case Accumulate:
            value += instruction.number;
            p++;
            break;
        }
    }
}

void trials(std::vector<Instruction>& program) {
    // For every instruction:
    //     Swap jump/noop ops, try the program, restore op.
    for (Instruction& i : program) {
        InstructionCode previous = i.code;

        if (i.code == NoOp) {
            i.code = Jump;
        } else if (i.code == Jump) {
            i.code = NoOp;
        } else {
            continue;
        }

        bool completed = interpret(program);
        if (completed) {
            break;
        }

        i.code = previous;
    }
}

int main(int argc, char** argv) {
    std::vector<Instruction> instructions;

    char icode[8];
    int num;

    while (std::scanf("%3s %d\n", icode, &num) == 2) {
        if (0 == std::strcmp("nop", icode)) {
            instructions.emplace_back(std::move(NoOp), std::move(num));
        } else if (0 == std::strcmp("acc", icode)) {
            instructions.emplace_back(std::move(Accumulate), std::move(num));
        } else if (0 == std::strcmp("jmp", icode)) {
            instructions.emplace_back(std::move(Jump), std::move(num));
        } else {
            std::cerr << "unexpected instruction code " << icode << std::endl;
        }
    }
    
    trials(instructions);
    return 0;
}