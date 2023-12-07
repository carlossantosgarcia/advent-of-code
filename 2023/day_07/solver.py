import argparse
import collections
import functools


def find_hand(cards: str) -> str:
    """Returns the string encoding the hand given as input."""
    set_cards = set(cards)
    if len(set_cards) == 5:
        return "single"
    if len(set_cards) == 4:
        return "onepair"
    elif len(set_cards) == 1:
        return "five"
    else:
        freqs = collections.Counter(cards).most_common(1)
        for _, freq in freqs:
            match freq:
                case 2:
                    return "twopair"
                case 4:
                    return "four"
                case 3 if len(set_cards) == 2:
                    return "house"
                case 3 if len(set_cards) == 3:
                    return "three"


def strongest_hand(cards: str, card_values: dict[str, int]) -> str:
    """Finds the strongest possible hand when containing Jokers."""
    nb_jokers = cards.count("J")
    if nb_jokers < 5:
        other_cards = cards.replace("J", "")
        most_common = collections.Counter(other_cards).most_common()
        if len(most_common) > 1:
            if (val := most_common[0][1]) == most_common[1][1]:
                frq_cards = [c[0] for c in most_common if c[1] == val]
                frq_values = [card_values[c] for c in frq_cards]
                best = frq_cards[frq_values.index(max(frq_values))]
            else:
                best = most_common[0][0]
        else:
            best = most_common[0][0]
    else:
        best = "A"
    strongest_hand = cards.replace("J", best)
    return strongest_hand


def part_1(file: str) -> int:
    """Computes the total winnings after sorting the hands.

    Args:
        file (str): Path to the puzzle input

    Returns:
        int: Total sum of points.
    """
    input_cards, bets = [], []
    # Read file
    with open(file, "r") as f:
        for line in f.readlines():
            cards, bet = line.rstrip().split()
            input_cards.append(cards)
            bets.append(int(bet))

    cards = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
    card_values = dict(zip(cards, reversed(range(len(cards)))))
    hands = ["five", "four", "house", "three", "twopair", "onepair", "single"]
    hand_values = dict(zip(hands, reversed(range(len(hands)))))

    def compare(elem1: tuple[str, int], elem2: tuple[str, int]) -> int:
        """Custom function to compare the strength of two cards."""
        cards1, cards2 = elem1[0], elem2[0]
        hand1, hand2, = find_hand(cards1), find_hand(cards2)
        if hand_values[hand1] < hand_values[hand2]:
            return -1
        elif hand_values[hand1] > hand_values[hand2]:
            return 1
        else:
            for idx in range(len(cards1)):
                card1, card2 = cards1[idx], cards2[idx]
                if card1 == card2:
                    continue
                if card_values[card1] < card_values[card2]:
                    return -1
                elif card_values[card1] > card_values[card2]:
                    return 1
            if idx == len(cards1) - 1:
                return 0

    sorted_hands = sorted(zip(input_cards, bets),
                          key=functools.cmp_to_key(compare), reverse=False)
    total_winnings = sum([(idx + 1) * bet
                         for idx, (_, bet) in enumerate(sorted_hands)])
    return total_winnings


def part_2(file: str) -> int:
    """Computes the final number of scratchcards.

    Args:
        file (str): Path to the puzzle input

    Returns:
        int: The final number of scratchcards.
    """
    input_cards, bets = [], []
    # Read file
    with open(file, "r") as f:
        for line in f.readlines():
            cards, bet = line.rstrip().split()
            input_cards.append(cards)
            bets.append(int(bet))

    cards = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
    card_values = dict(zip(cards, reversed(range(len(cards)))))
    hands = ["five", "four", "house", "three", "twopair", "onepair", "single"]
    hand_values = dict(zip(hands, reversed(range(len(hands)))))

    # Updates value for Joker
    card_values["J"] = -1

    def compare_with_jokers(
            elem1: tuple[str, int], elem2: tuple[str, int]) -> int:
        """Custom function to compare the strength of two cards."""
        cards1, cards2 = elem1[0], elem2[0]
        hand1 = find_hand(strongest_hand(
            cards1, card_values)) if "J" in cards1 else find_hand(cards1)
        hand2 = find_hand(strongest_hand(
            cards2, card_values)) if "J" in cards2 else find_hand(cards2)
        if hand_values[hand1] < hand_values[hand2]:
            return -1
        elif hand_values[hand1] > hand_values[hand2]:
            return 1
        else:
            for idx in range(len(cards1)):
                card1, card2 = cards1[idx], cards2[idx]
                if card1 == card2:
                    continue
                if card_values[card1] < card_values[card2]:
                    return -1
                elif card_values[card1] > card_values[card2]:
                    return 1
            if idx == len(cards1)-1:
                return 0

    sorted_hands = sorted(zip(input_cards, bets), key=functools.cmp_to_key(
        compare_with_jokers), reverse=False)

    total_winnings = sum([(idx + 1) * bet
                         for idx, (_, bet) in enumerate(sorted_hands)])

    return total_winnings


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solves Day 7 puzzles")
    parser.add_argument("--file", type=str, help="Path to puzzle file")
    args = parser.parse_args()

    sol1 = part_1(file=args.file)
    sol2 = part_2(file=args.file)

    print(f"Part 1 solution: {sol1}")
    print(f"Part 2 solution: {sol2}")
