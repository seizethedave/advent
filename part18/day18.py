import sys
from typing import Tuple, Union, Optional

class Node(object):
    def __init__(self, val: Union[int, Tuple['Node', 'Node']], prev: Optional['Node']=None, nxt: Optional['Node']=None, depth: int=0):
        self.val = val
        self.prev = prev
        self.next = nxt
        self.depth = depth

    def __eq__(self, other):
        return isinstance(other, Node) and vars(self) == vars(other)

    def __repr__(self) -> str:
        #nextstr = "nil" if self.next is None else self.next.val
        #return f"Node({self.val})" if self.prev is None else f"Node({self.val}, prev={self.prev.val}, next={nextstr})"
        if isinstance(self.val, int):
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

    def add(self, other: 'Node'):
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

    def validate(self):
        def scan(n, depth):
            if n.depth != depth:
                raise Exception(f"invalid depth. expected {depth}, got {n.depth}")
            if isinstance(n.val, tuple):
                lhs, rhs = n.val
                scan(lhs, depth + 1)
                scan(rhs, depth + 1)
        scan(self, 0)

    def magnitude(self):
        pass

    def reduce(self):
        def reduce_tree_scan(n: Node) -> Node:
            if isinstance(n.val, int):
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
                    if n.next is not None:
                        n.next.prev = rhs
                    n.val = (lhs, rhs)
                    reduce_tree_scan(n)
                    self.validate()
                return

            assert isinstance(n.val, tuple)
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
                if lhs.prev:
                    reduce_tree_scan(lhs.prev)
                if rhs.next:
                    reduce_tree_scan(rhs.next)
                self.validate()
                return

            reduce_tree_scan(lhs)
            reduce_tree_scan(rhs)
        
        reduce_tree_scan(self)
        return self
        
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
    n.validate()
    return n


if "__main__" == __name__:
    total = None

    for line in sys.stdin:
        num = parse(line)
        print(num)

        if total is None:
            total = num
        else:
            total = total.add(num)
            print("added=", total)
            total.reduce()

        print("= subtotal", total)

    print(total)
