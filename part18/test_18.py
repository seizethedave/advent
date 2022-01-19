import unittest

from day18 import *

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

    def test_reduce_bigone(self):
        self.assertEqual(
            repr(reduce_tree(parse("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]"))),
            "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"
        )

    def test_node_eq(self):
        self.assertEqual(Node(93), Node(93))
        self.assertEqual(Node((Node(1), Node(2))), Node((Node(1), Node(2))))
        self.assertNotEqual(Node((Node(1), Node(2))), Node((Node(3), Node(4))))
        self.assertNotEqual(Node((Node(1), Node(2))), Node((Node(1), Node(2, depth=1))))
        self.assertNotEqual(Node(93), Node(94))
        self.assertEqual(Node(1, depth=2), Node(1, depth=2))
        self.assertNotEqual(Node(1, depth=2), Node(1, depth=20))
        self.assertNotEqual(Node(93), Node(94))

