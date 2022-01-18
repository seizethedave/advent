import sys
from typing import Tuple, Union, Optional
import unittest


class Node(object):
    def __init__(self, val: Union[int, Tuple['Node', 'Node']], prev: Optional['Node']=None):
        self.val = val
        self.prev = prev
        self.next: Optional[Node] = None

    def __repr__(self) -> str:
        #nextstr = "nil" if self.next is None else self.next.val
        #return f"Node({self.val})" if self.prev is None else f"Node({self.val}, prev={self.prev.val}, next={nextstr})"
        if isinstance(self.val, int):
            return repr(self.val)
        return f"[{self.val[0]},{self.val[1]}]"

def parse(s: str) -> Node:
    prev: Node = None
    def parse_inner(i: int) -> Tuple[Node, int]:
        nonlocal prev
        c = s[i]
        if c.isnumeric():
            # A numeric leaf node. Thread prev/next pointers between leaves.
            ret = Node(int(c), prev)
            if prev is not None:
                prev.next = ret
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
                lhs.next = rhs
                rhs.next = n.next
                if n.prev is not None:
                    n.prev.next = lhs
                if n.next is not None:
                    n.next.prev = rhs
                n.val = (lhs, rhs)
                return reduce_tree_scan(n, depth + 1)

            return n

        assert isinstance(n.val, tuple)
        #assert depth < 5
        lhs, rhs = n.val

        if depth >= 4:
            # explode
            if lhs.prev is not None:
                assert isinstance(lhs.prev.val, int)
                lhs.prev.val += lhs.val # TODO <- split if needed.
                if lhs.prev.val > 9:
                    print("NEED TO SPLIT", lhs.prev.val)
            carry = rhs.val
            n.val = 0
            n.prev = lhs.prev
            n.next = rhs.next
            if lhs.prev is not None:
                lhs.prev.next = n
            if rhs.next is not None:
                rhs.next.prev = n
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


class Tests(unittest.TestCase):
    def test_reduce(self):
        self.assertEqual(
            repr(reduce_tree(parse("[[[[[9,8],1],2],3],4]"))),
            "[[[[0,9],2],3],4]"
        )
        self.assertEqual(
            repr(reduce_tree(parse("[7,[6,[5,[4,[3,2]]]]]"))),
            "[7,[6,[5,[7,0]]]]"
        )
        self.assertEqual(
            repr(reduce_tree(parse("[[6,[5,[4,[3,2]]]],1]"))),
            "[[6,[5,[7,0]]],3]"
        )
        self.assertEqual(
            repr(reduce_tree(parse("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"))),
            "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"
        )




if "__main__" == __name__:
    unittest.main()

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