import math
import operator
import sys
from typing import Any, Callable, Dict, List, NamedTuple
import unittest

OP_LT = "<"
OP_GT = ">"
OPS = {OP_LT: operator.lt, OP_GT: operator.gt}
START_WORKFLOW = "in"
ACCEPT = "A"
REJECT = "R"

class Rule(NamedTuple):
    lhs_field: str
    op_char: str
    op: Callable[[Any, Any], bool]
    rhs_val: int
    action: str

class Workflow(NamedTuple):
    name: str
    rules: List[Rule]

class Rating(NamedTuple):
    vals: Dict[str, int]

def read_workflow(s: str) -> Workflow:
    rules_begin = s.index("{")
    name = s[:rules_begin]
    rules_str = s[rules_begin+1:-1]
    rules = []
    for r in rules_str.split(","):
        if ":" in r:
            pred, action = r.split(":")
            lhs = pred[0]
            op = pred[1]
            rhs = pred[2:]
            rules.append(Rule(lhs, op, OPS[op], int(rhs), action))
        else:
            # Unpredicated rule - a bare A, R or the name of another workflow to
            # jump to.
            rules.append(Rule(None, None, None, None, r))

    return Workflow(name, rules)

def read_rating(s: str) -> Rating:
    vals = {}
    for item in s.strip("{}").split(","):
        k, v = item.split("=")
        vals[k] = int(v)
    return Rating(vals)

def eval_rating(r: Rating, workflows: Dict[str, Workflow]) -> bool:
    w = workflows[START_WORKFLOW]
    while True:
        # Find the action for the first matching rule in this workflow.
        for rule in w.rules:
            if rule.lhs_field is not None:
                if rule.op(r.vals[rule.lhs_field], rule.rhs_val):
                    action = rule.action
                    break
            else:
                action = rule.action
                break
        else:
            assert False, "couldn't find an action."

        if action == ACCEPT:
            return True
        elif action == REJECT:
            return False
        else:
            w = workflows[action]

VAL_LOWERBOUND = 1
VAL_UPPERBOUND = 4001
CATEGORIES = ['x', 'm', 'a', 's']

class Constraint:
    def __init__(self, op, val):
        self.op = op
        self.val = val

    def negate(self):
        # <1000 negates to >999
        if self.op == OP_LT:
            return Constraint(OP_GT, self.val - 1)
        else:
            return Constraint(OP_LT, self.val + 1)

class CriteriaSet:
    def __init__(self, copyFrom: 'CriteriaSet'=None):
        if copyFrom is not None:
            self.vars = copyFrom.vars.copy()
        else:
            self.vars = {c: (VAL_LOWERBOUND, VAL_UPPERBOUND) for c in CATEGORIES}

    def apply(self, var: str, constraint: Constraint):
        l, h = self.vars[var]
        if constraint.op == OP_LT:
            # r = (10, 20)
            # op = <15 ==> r' = (10, 15)
            # op = <10 ==> r' = (10, 10)
            # op = <7 ==> r' = (10, 7)
            # op = <37 ==> r' = (10, 20)
            self.vars[var] = (l, min(constraint.val, h))
        else:
            # Convert strictly-greater-than to our closed interval lower bound.
            # (>n ==> [n+1, y))
            self.vars[var] = (max(l, constraint.val + 1), h)

    def combinations(self) -> int:
        return math.prod(max(0, hi - lo) for lo, hi in self.vars.values())

    def copy(self) -> 'CriteriaSet':
        return CriteriaSet(copyFrom=self)

def count_combinations(workflows: Dict[str, Workflow]) -> int:
    # Visit a rule r1 with some criteria. Recurse into the rule pushing the
    # accumulated criteria in there. Continue with r2, which is the rule
    # following r1. We negate r1.criteria and append that to the criteria we'll
    # push into r2.

    def count(w: Workflow, state: CriteriaSet) -> int:
        s = 0
        for rule in w.rules:
            substate = state.copy()
            if rule.lhs_field is not None:
                cons = Constraint(rule.op_char, rule.rhs_val)
                substate.apply(rule.lhs_field, cons)
                state.apply(rule.lhs_field, cons.negate())

            if rule.action == ACCEPT:
                s += substate.combinations()
            elif rule.action == REJECT:
                pass
            else:
                # It's a jump to another workflow.
                s += count(workflows[rule.action], substate)

        return s

    return count(workflows[START_WORKFLOW], CriteriaSet())

class Tests(unittest.TestCase):
    def test_constraint(self):
        c = Constraint('>', 1000)
        n = c.negate()
        self.assertEqual(n.op, '<')
        self.assertEqual(n.val, 1001)
        n2 = n.negate()
        self.assertEqual(n2.op, c.op)
        self.assertEqual(n2.val, c.val)

    def test_criteria(self):
        s = CriteriaSet()
        self.assertEqual(s.combinations(), (VAL_UPPERBOUND - VAL_LOWERBOUND)**4)

        s.apply('x', Constraint('>', 1000))
        self.assertEqual(s.vars['x'], (1001, VAL_UPPERBOUND))
        s.apply('x', Constraint('>', 1000))
        self.assertEqual(s.vars['x'], (1001, VAL_UPPERBOUND))
        s.apply('x', Constraint('>', 1001))
        self.assertEqual(s.vars['x'], (1002, VAL_UPPERBOUND))
        s.apply('x', Constraint('<', 2000))
        self.assertEqual(s.vars['x'], (1002, 2000))

        self.assertEqual(s.combinations(), (VAL_UPPERBOUND - VAL_LOWERBOUND)**3 * (2000-1002))

        s.apply('x', Constraint('>', 1999))
        self.assertEqual(s.combinations(), 0, "1999<x<2000 means there are no solutions.")
        s.apply('x', Constraint('>', 10))
        self.assertEqual(s.combinations(), 0)

if __name__ == "__main__":
    reading_workflows = True
    workflows: Dict[str, Workflow] = {}
    ratings: List[Rating] = []

    for line in sys.stdin:
        line = line.rstrip()
        if not line:
            reading_workflows = False
            continue

        if reading_workflows:
            w = read_workflow(line)
            workflows[w.name] = w
        else:
            ratings.append(read_rating(line))

    print(
        sum(
            sum(r.vals.values()) if eval_rating(r, workflows) else 0
            for r in ratings
        )
    )

    print(count_combinations(workflows))
