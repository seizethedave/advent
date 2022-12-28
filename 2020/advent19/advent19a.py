import sys

class Terminal:
    def __init__(self, val):
        self.val = val

    def matches(self, text, offset, rules):
        return (True, len(self.val)) if text[offset:].startswith(self.val) else (False, 0)

class Seq(list):
    @classmethod
    def from_string(cls, s):
        return cls(int(n) for n in s.split())

    def matches(self, text, offset, rules):
        totalmatchlen = 0
        for rule_id in self:
            rule = rules[rule_id]
            match, matchlen = rule.matches(text, offset + totalmatchlen, rules)
            if not match:
                return False, 0
            totalmatchlen += matchlen
        else:
            return True, totalmatchlen

class Disjunction:
    def __init__(self, items):
        self.items = items

    def matches(self, text, offset, rules):
        for item in self.items:
            match, matchlen = item.matches(text, offset, rules)
            if match:
                return True, matchlen
        else:
            return False, 0

    def __repr__(self):
        return f"Disjunction({repr(self.items)})"

rules = {}

def load_rules():
    for line in sys.stdin:
        if line == "\n":
            break
        rule_id, rhs = line.strip().split(":")
        rule_id = int(rule_id)
        rhs = rhs.strip()
        if rhs.startswith('"'):
            # A string terminal.
            val = Terminal(rhs.strip('"'))
        else:
            # Non-terminal: 1+ sequences of terminals OR'd together (a disjunction).
            val = Disjunction([Seq.from_string(fragment.strip()) for fragment in rhs.split("|")])
        rules[rule_id] = val

def does_match(s, rules, rule_id):
    rule = rules[rule_id]
    match, matchlen = rule.matches(s, 0, rules)
    return match and matchlen == len(s)

if __name__ == "__main__":
    load_rules()

    # Remainder of stdin are input messages.
    print(sum(int(does_match(line.strip(), rules, 0)) for line in sys.stdin))