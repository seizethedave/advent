import sys
from typing import Tuple, Union, Optional

class Node(object):
    def __init__(self, val: Union[int, Tuple['Node', 'Node']], prev: Optional['Node']=None, nxt: Optional['Node']=None, depth: int=0):
        self.val = val
        self.prev = prev
        self.next = nxt
        self.depth = depth

    def __eq__(self, other):
        return isinstance(other, Node) and self.__dict__ == other.__dict__

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

        def incr(node):
            node.depth += 1

        self.map_nodes(incr)
        other.map_nodes(incr)
        return Node((self, other))


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


def reduce_tree(head: Node) -> Node:
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
            return n

        assert isinstance(n.val, tuple)
        #assert depth < 5
        lhs, rhs = n.val

        if n.depth >= 4:
            # explode
            if lhs.prev is not None:
                assert isinstance(lhs.prev.val, int)
                lhs.prev.val += lhs.val
                lhs.prev = reduce_tree_scan(lhs.prev)
            if rhs.next is not None:
                assert isinstance(rhs.next.val, int)
                rhs.next.val += rhs.val
                rhs.next = reduce_tree_scan(rhs.next)
            n.val = 0
            n.prev = lhs.prev
            n.next = rhs.next
            if lhs.prev is not None:
                lhs.prev.next = n
            if rhs.next is not None:
                rhs.next.prev = n
            # print("   > ", head)
            return n
    
        n.val = (
            reduce_tree_scan(lhs),
            reduce_tree_scan(rhs)
        )
        return n
        
    return reduce_tree_scan(head)

def parse_reduce(s):
    parsed = parse(s)
    print("before:", parsed)
    print("after:", reduce_tree(parsed))





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
            total = reduce_tree(total)



        print("   ", total)

    print(total)
