import sys
from collections import Counter

HighCard = 1
OnePair = 2
TwoPair = 3
ThreeOfKind = 4
FullHouse = 5
FourOfKind = 6
FiveOfKind = 7

Joker = 1

Part1ValMap = {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
Part2ValMap = {'T': 10, 'J': 1, 'Q': 12, 'K': 13, 'A': 14}

def hand_to_numeric(h: str, valmap: dict[str, int]):
    return [int(c) if c.isdigit() else valmap[c] for c in h]

def hand_from_counts(counts):
    if len(counts) == 1:
        return FiveOfKind
    elif counts[0] == 4:
        return FourOfKind
    elif counts[:2] == [3, 2]:
        return FullHouse
    elif counts[0] == 3:
        return ThreeOfKind
    elif counts[:2] == [2, 2]:
        return TwoPair
    elif counts[0] == 2:
        return OnePair
    return HighCard

def calc_hand_type_part_1(h: str) -> int:
    norm = Counter(h)
    counts = sorted(list(norm.values()), reverse=True)
    return hand_from_counts(counts)

def calc_hand_type_part_2(h: str) -> int:
    if h == [Joker] * 5:
        return FiveOfKind
    norm = Counter()
    jokers = 0
    for c in h:
        if c == Joker:
            jokers += 1
        else:
            norm[c] += 1
    counts = sorted(list(norm.values()), reverse=True)
    # Whatever is in counts[0] will contribute the most to the hand.
    # Our jokers will make the most impact by duplicating that card.
    counts[0] += jokers
    return hand_from_counts(counts)

if __name__ == "__main__":

    input_lines = []
    
    for line in sys.stdin:
        hand, score = line.split()
        input_lines.append((hand, score))

    hands = []
    for (hand, score) in input_lines:    
        numeric_hand = hand_to_numeric(hand, Part1ValMap)
        hand_type = calc_hand_type_part_1(numeric_hand)
        hands.append((hand_type, numeric_hand, int(score)))

    print(
        sum(
            rank * score
            for rank, (_, _, score) in enumerate(sorted(hands), start=1)
        )
    )

    # part 2:

    hands = []
    for (hand, score) in input_lines:    
        numeric_hand = hand_to_numeric(hand, Part2ValMap)
        hand_type = calc_hand_type_part_2(numeric_hand)
        hands.append((hand_type, numeric_hand, int(score)))

    print(
        sum(
            rank * score
            for rank, (_, _, score) in enumerate(sorted(hands), start=1)
        )
    )
