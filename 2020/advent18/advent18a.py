import sys
import operator

def eval_expr(expr):
    return eval_expr_iter(iter(expr))

def eval_expr_iter(it):
    operands = []
    op = None

    for c in it:
        if c.isspace():
            continue
        elif c.isdecimal():
            operands.append(int(c))
        elif c == '+':
            op = operator.add
        elif c == '*':
            op = operator.mul
        elif c == '(':
            operands.append(eval_expr_iter(it))

        if len(operands) == 2:
            # result becomes operand[0]
            operands = [op(*operands)]

        if c == ')':
            break
    return operands[0]

if __name__ == "__main__":
    total = 0
    for line in sys.stdin:
        total += eval_expr(line.rstrip())
    print(total)