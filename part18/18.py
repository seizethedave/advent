import sys

def reduce(num):
    prevlist = None
    carry = None

    def reduce_search(n, depth):
        nonlocal prevlist, carry
        if isinstance(n, int):
            if n > 9:
                # split
                return [n // 2, n - (n // 2)]
            elif carry is not None:
                n += carry
                carry = None
            return n
        else:
            # a list
            if depth >= 4:
                # explode
                if prevlist is not None:
                    prevlist[0] += n[0]
                carry = n[1]
                return 0

            if isinstance(n[0], int):
                prevlist = n

            n[0] = reduce_search(n[0], depth + 1)
            n[1] = reduce_search(n[1], depth + 1)
            return n
    
    return reduce_search(num, 0)


print(reduce([[[[[9,8],1],2],3],4]))
print(reduce([7,[6,[5,[4,[3,2]]]]]))
print(reduce([[6,[5,[4,[3,2]]]],1]))
print(reduce([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]))

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
