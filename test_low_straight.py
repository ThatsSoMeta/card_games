import schemas
import holdem

cards = [
    (14, 'clubs'),
    (13, 'clubs'),
    (12, 'diamonds'),
    (11, 'clubs'),
    (5, 'hearts'),
    (8, 'clubs'),
    (10, 'spades'),
]

cards2 = [14, 13, 12, 11, 10, 7, 4]

drew = schemas.Player('Drew')
drew.hand = []

deck = schemas.Deck()

for card in deck.deck:
    for (value, suit) in cards:
    # for value in cards2:
        if card.value == value and card.suit == suit:
            drew.hand.append(card)

print(drew.hand)
print(holdem.assess_hand(drew))
