import operator
import sys
from typing import Any, Callable, Dict, Iterable, List, NamedTuple

OPS = {"<": operator.lt, ">": operator.gt}
START_WORKFLOW = "in"
ACCEPT = "A"
REJECT = "R"

class Rule(NamedTuple):
    lhs_field: str
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
            rules.append(Rule(lhs, OPS[op], int(rhs), action))
        else:
            rules.append(Rule(None, None, None, r))
        
    return Workflow(name, rules)

def read_rating(s: str) -> Rating:
    vals = {}
    for item in s.strip("{}").split(","):
        k, v = item.split("=")
        vals[k] = int(v)
    return Rating(vals)

def eval_workflow(rating: Rating, workflow: Workflow) -> str:
    for rule in workflow.rules:
        if rule.lhs_field is not None:
            if rule.op(rating.vals[rule.lhs_field], rule.rhs_val):
                return rule.action
        else:
            return rule.action

def eval_rating(r: Rating, workflows: Dict[str, Workflow]) -> bool:
    w = workflows[START_WORKFLOW]
    while True:
        action = eval_workflow(r, w)
        if action == ACCEPT:
            return True
        elif action == REJECT:
            return False
        else:
            w = workflows[action]

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