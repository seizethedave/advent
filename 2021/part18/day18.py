import sys
from typing import Tuple, Union, Optional
import itertools

class Recombobulate(Exception):
    pass

class Node(object):
    def __init__(self, val: Union[int, Tuple['Node', 'Node']], prev: Optional['Node']=None, nxt: Optional['Node']=None, depth: int=0):
        self.val = val
        self.prev = prev
        self.next = nxt
        self.depth = depth

    def __eq__(self, other):
        return isinstance(other, Node) and vars(self) == vars(other)

    def __repr__(self) -> str:
        if self.is_leaf:
            return repr(self.val)
        return f"[{self.val[0]},{self.val[1]}]"

    @property
    def is_leaf(self):
        return isinstance(self.val, int)

    def iter_nodes(self):
        nodes = [self]
        while nodes:
            n = nodes.pop()
            yield n
            if not n.is_leaf:
                nodes.extend(n.val)

    def search_leaves(self, predicate) -> Optional['Node']:
        for n in self.iter_nodes():
            if n.is_leaf and predicate(n):
                return n
        else:
            return None

    def map_nodes(self, fn):
        for n in self.iter_nodes():
            fn(n)

    def add(self, other: 'Node') -> 'Node':
        lhs_tail = self.search_leaves(lambda n: n.next is None)
        assert lhs_tail is not None
        rhs_head = other.search_leaves(lambda n: n.prev is None)
        assert rhs_head is not None
        lhs_tail.next = rhs_head
        rhs_head.prev = lhs_tail

        def incr_depth(node):
            node.depth += 1

        self.map_nodes(incr_depth)
        other.map_nodes(incr_depth)
        return Node((self, other))

    def magnitude(self):
        if self.is_leaf:
            return self.val
        lhs, rhs = self.val
        return 3 * lhs.magnitude() + 2 * rhs.magnitude()

    def reduce_explode(self):
        def rexp(n):
            if n.is_leaf:
                return
            lhs, rhs = n.val

            if n.depth >= 4:
                # explode
                if lhs.prev is not None:
                    assert isinstance(lhs.prev.val, int)
                    lhs.prev.next = n
                    lhs.prev.val += lhs.val
                if rhs.next is not None:
                    assert isinstance(rhs.next.val, int)
                    rhs.next.prev = n
                    rhs.next.val += rhs.val
                n.val = 0
                n.prev = lhs.prev
                n.next = rhs.next
                return

            rexp(lhs)
            rexp(rhs)
        rexp(self)

    def reduce_split(self):
        def rsplit(n):
            if n.is_leaf:
                if n.val > 9:
                    # split
                    half = n.val // 2
                    lhs = Node(half, n.prev)
                    rhs = Node(n.val - half, lhs)
                    lhs.depth = rhs.depth = (n.depth + 1)
                    lhs.next = rhs
                    rhs.next = n.next
                    if n.prev is not None:
                        n.prev.next = lhs
                        n.prev = None
                    if n.next is not None:
                        n.next.prev = rhs
                        n.next = None
                    n.val = (lhs, rhs)
                    # Signal that we need to re-explode.
                    raise Recombobulate()
                return
            lhs, rhs = n.val
            rsplit(lhs)
            rsplit(rhs)

        rsplit(self)
        
    def reduce(self):
        while True:
            self.reduce_explode()
            try:
                self.reduce_split()
            except Recombobulate:
                continue
            else:
                break
        return self

    def dump(self, level=0):
        indent = " " * level
        if self.is_leaf:
            print(f"{indent}Node({id(self)} d={self.depth} val={self.val})")
        else:
            print(f"{indent}Node({id(self)} d={self.depth}")
            lhs, rhs = self.val
            lhs.dump(level+1)
            rhs.dump(level+1)
            print(f"{indent})")

        
def parse(s: str) -> Node:
    prev: Node = None
    def parse_inner(i: int, depth: int) -> Tuple[Node, int]:
        nonlocal prev
        c = s[i]
        if c.isnumeric():
            # A numeric leaf node. Thread prev/next pointers between leaves.
            node = Node(int(c), prev)
            node.depth = depth
            if prev is not None:
                prev.next = node
            prev = node
            return (node, i + 1)
        elif c == "[":
            lhs, i = parse_inner(i + 1, depth + 1)
            assert s[i] == ","
            rhs, i = parse_inner(i + 1, depth + 1)
            assert s[i] == "]"
            node = Node((lhs, rhs))
            node.depth = depth
            return (node, i + 1)

    n, _ = parse_inner(0, 0)
    return n

def part1():
    total = None

    for line in sys.stdin:
        num = parse(line)
        if total is None:
            total = num
        else:
            total = total.add(num)
            total.reduce()

    print(total)
    print(total.magnitude())

def part2():
    mag = 0
    for lhs, rhs in itertools.product(sys.stdin.readlines(), repeat=2):
        v = parse(lhs).add(parse(rhs))
        v.reduce()
        mag = max(mag, v.magnitude())
    print(mag)

if "__main__" == __name__:
    part2()