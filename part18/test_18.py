import unittest

from day18 import parse, Node

class Tests(unittest.TestCase):
    def test_reduce(self):
        self.assertEqual(
            repr(parse("[[[[[9,8],1],2],3],4]").reduce()),
            "[[[[0,9],2],3],4]"
        )
        self.assertEqual(
            repr(parse("[7,[6,[5,[4,[3,2]]]]]").reduce()),
            "[7,[6,[5,[7,0]]]]"
        )
        self.assertEqual(
            repr(parse("[[6,[5,[4,[3,2]]]],1]").reduce()),
            "[[6,[5,[7,0]]],3]"
        )
        self.assertEqual(
            repr(parse("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]").reduce()),
            "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"
        )

    def test_reduce_big1(self):
        self.assertEqual(
            repr(parse("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]").reduce()),
            "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"
        )

    def test_reduce_big2(self):
        self.assertEqual(
            repr(parse("[[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]],[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]]").reduce()),
            "[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]"
        )

    def test_reduce_2(self):
        self.assertEqual(
            repr(parse("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]").reduce()),
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

    def test_node_add(self):
        one = Node(1)
        two = Node(2)
        three = one.add(two)
        self.assertEqual(
            three,
            Node((one, two))
        )

        self.assertEqual(three.depth, 0)
        self.assertEqual(one.depth, 1)
        self.assertEqual(two.depth, 1)
        self.assertIs(one.next, two)
        self.assertIs(two.prev, one)
        self.assertIsNone(three.prev)
        self.assertIsNone(three.next)

    def test_node_map(self):
        ct = 0
        def count_em(node):
            nonlocal ct
            ct += 1
            
        n = Node(6)
        n.map_nodes(count_em)
        self.assertEqual(ct, 1)

        ct = 0
        n = Node(
            (
                Node((Node(1), Node(2))),
                Node((Node(3), Node(4)))
            )
        )
        n.map_nodes(count_em)
        self.assertEqual(ct, 7)

    def test_node_mag(self):
        self.assertEqual(
            parse("[[1,2],[[3,4],5]]").magnitude(),
            143
        )
        self.assertEqual(
            parse("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]").magnitude(),
            3488
        )
