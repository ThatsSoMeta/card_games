from schemas import Deck
deck = Deck()
hand = []
cards = [(8, 'spades'), (9, 'hearts'), (10, 'spades'), (3, 'diamonds'), (12, 'spades'), (13, 'clubs'), (14, 'spades')]
vals = [card[0] for card in cards]
for card in deck.deck:
    if len(hand) < 7:
        if (card.value, card.suit) in cards:
            hand.append(card)
hand.sort(key=lambda card: card.value)
print(f"Hand: {hand}")
flush_cards = []
suits = {}
for card in hand:
    try:
        suits[card.suit] += 1
    except KeyError:
        suits[card.suit] = 1
for suit, value in suits.items():
    if value > 4:
        print(f"There is a flush in {suit}")
        flush_cards = sorted(
            [card for card in hand if card.suit == suit],
            key=lambda card: card.value
        )
        # print(flush_cards)
        flush_values = [
            card.value for card in flush_cards
        ]
        best_flush = flush_cards[-5:]
        print(best_flush)
        # TODO: Add flush to possible_plays
        for i in range(len(flush_values) - 4):
            flush_frag = list(flush_values[i: i + 5])
            str_flush_test = list(range(flush_values[i], flush_values[i] + 5))
            if flush_frag == str_flush_test:
                print("Straight flush!")
                straight_flush = flush_cards[-5:]
                print(straight_flush)
                # TODO: Add straight flush to possile_plays
                if flush_cards[-1].value == 14:
                    print("Royal flush!!!")
                    royal_flush = [straight_flush]
                    # TODO: Add royal_flush to possible_plays
possible_straights = []
vals_set = list(set(vals))
# print(f"Vals set:{vals_set}")
if len(vals_set) > 4:
    # print("Straight is possible... checking for consecutives")
    for i in range(len(vals_set) - 4):
        # print(i)
        current_frag = list(vals_set[i: i + 5])
        test_list = list(range(vals[i], vals[i] + 5))
        # print(f"Current frag: {current_frag}")
        # print(f"Test list: {test_list}")
        if current_frag == test_list:
            possible_straights.append(current_frag)
if possible_straights:
    best_straight_values = possible_straights.pop()
    # print(f"Straight values: {best_straight_values}")
    best_straight = []
    for card in hand:
        values = []
        if card.value in best_straight_values:
            if card.value not in values:
                values.append(card.value)
                best_straight.append(card)
    print(f"Best straight: {best_straight}")
    # TODO: Add best_straight to possible_plays
