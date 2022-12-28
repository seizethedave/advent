import sys
import operator

# cat input.txt | python3.9 advent18b.py

def eval_expr(expr):
    return eval_expr_iter(iter(expr))

operators = {'*': operator.mul, '+': operator.add}
precedence = {operator.mul: 1, operator.add: 2}

def eval_expr_iter(it):
    operands = []
    opstack = []

    for c in it:
        if c.isspace():
            continue
        elif c.isdecimal():
            operands.append(int(c))
        elif op := operators.get(c):
            try:
                lastop = opstack[-1]
            except IndexError:
                pass
            else:
                if precedence[lastop] >= precedence[op]:
                    # Go ahead and eval lastop in place.
                    opstack.pop()
                    operands.append(lastop(operands.pop(), operands.pop()))
            opstack.append(op)
        elif c == '(':
            operands.append(eval_expr_iter(it))
        elif c == ')':
            break

    while opstack:
        op = opstack.pop()
        operands.append(op(operands.pop(), operands.pop()))

    return operands[0]

if __name__ == "__main__":
    print(sum(eval_expr(line.rstrip()) for line in sys.stdin))
