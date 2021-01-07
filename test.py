from schemas import Deck
# vals = [0, 2, 4, 5, 6, 7, 8]
deck = Deck()
hand = []
vals = [10, 10, 11, 11, 12, 13, 14]
for card in deck.deck:
    if card:
        print(card)
    if len(hand) < 7:
        if card.value in vals:
            hand.append(card)
print(f"Hand: {hand}")
hand.sort(key=lambda card: card.value)
possible_straights = []
vals = list(set(vals))
for i in range(len(vals) - 4):
    print(i)
    current_frag = vals[i: i + 5]
    test_list = list(range(vals[i], vals[i] + 5))
    print(f"Current frag: {current_frag}")
    print(f"Test list: {test_list}")
    if vals[i: i + 5] == list(range(vals[i], vals[i] + 5)):
        possible_straights.append(vals[i: i + 5])
        print(possible_straights)
best_straight = possible_straights.pop()
best_hand = [
    card for card in hand
    if card.value in best_straight
]
print(f"Best straight: {best_straight}")
print(f"Best hand: {best_hand}")
