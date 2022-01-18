from ast import Str
import sys
from typing import Tuple, Union, Optional


class Node(object):
    def __init__(self, val: Union[int, Tuple['Node', 'Node']], prev: Optional['Node']=None):
        self.val = val
        self.prev = prev

    def __repr__(self) -> str:
        # return f"Node({self.val})" if self.prev is None else f"Node({self.val}, prev={self.prev.val})"
        if isinstance(self.val, int):
            return repr(self.val)
        return f"[{self.val[0]},{self.val[1]}]"

def parse(s: str) -> Node:
    prev = None
    def parse_inner(i: int) -> Tuple[Node, int]:
        nonlocal prev
        c = s[i]
        if c.isnumeric():
            # A numeric leaf node. Thread a backwards path through leaves with
            # `prev` pointers.
            ret = Node(int(c), prev)
            prev = ret
            return (ret, i + 1)
        elif c == "[":
            lhs, i = parse_inner(i + 1)
            assert s[i] == ","
            rhs, i = parse_inner(i + 1)
            assert s[i] == "]"
            return (Node((lhs, rhs)), i + 1)

    n, _ = parse_inner(0)
    return n


def reduce_tree(head: Node) -> Node:
    carry = 0

    def reduce_tree_scan(n: Node, depth: int) -> Node:
        nonlocal carry

        if isinstance(n.val, int):
            n.val += carry
            carry = 0

            if n.val > 9:
                # split
                half = n.val // 2
                lhs = Node(half, n.prev)
                rhs = Node(n.val - half, lhs)
                n.val = (lhs, rhs)
                return reduce_tree_scan(n, depth + 1)

            return n

        assert isinstance(n.val, tuple)
        assert depth < 5
        lhs, rhs = n.val

        if depth == 4:
            # explode
            if lhs.prev is not None:
                assert isinstance(lhs.prev.val, int)
                lhs.prev.val += lhs.val # TODO <- split if needed.
                if lhs.prev.val > 9:
                    print("NEED TO SPLIT", lhs.prev.val)
            carry = rhs.val
            n.val = 0
            n.prev = lhs.prev
            return n
    
        n.val = (
            reduce_tree_scan(lhs, depth + 1),
            reduce_tree_scan(rhs, depth + 1)
        )
        return n
        
    return reduce_tree_scan(head, 0)


def parse_reduce(s):
    parsed = parse(s)
    print("before:", parsed)
    print("after:", reduce_tree(parsed))

parse_reduce("[[[[[9,8],1],2],3],4]")
parse_reduce("[7,[6,[5,[4,[3,2]]]]]")
parse_reduce("[[6,[5,[4,[3,2]]]],1]")
parse_reduce("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]")

"""
if "__main__" == __name__:
    total = None

    for line in sys.stdin:
        entry = eval(line)

        if total is None:
            total = entry
        else:
            total = reduce([total, entry])

        print(entry)
        print("   ", total)

    print(total)

    print(reduce([[[[[4,3],4],4],[7,[[8,4],9]]],  [1,1]]))
"""