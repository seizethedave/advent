import sys

class Terminal:
    def __init__(self, val):
        self.val = val

    def matches(self, text, offset, rules):
        if text[offset:].startswith(self.val):
            yield len(self.val)

class Seq(list):
    @classmethod
    def from_string(cls, s):
        return cls(int(n) for n in s.split())

    def matches(self, text, offset, rules):
        if len(self) == 1:
            rule = rules[self[0]]
            yield from rule.matches(text, offset, rules)
            return

        prefix, suffix = Seq(self[:1]), Seq(self[1:])

        for m in prefix.matches(text, offset, rules):
            for submatch in suffix.matches(text, offset + m, rules):
                yield m + submatch

class Disjunction:
    def __init__(self, items):
        self.items = items

    def matches(self, text, offset, rules):
        for item in self.items:
            yield from item.matches(text, offset, rules)

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
    for m in rule.matches(s, 0, rules):
        if m == len(s):
            return True
    else:
        return False

if __name__ == "__main__":
    load_rules()

    # Remainder of stdin are input messages.
    print(sum(int(does_match(line.strip(), rules, 0)) for line in sys.stdin))