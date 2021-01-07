import schemas
import holdem

cards = [14, 13, 12, 11, 10, 9, 8]

drew = schemas.Player('Drew')
drew.hand = []

deck = schemas.Deck()

for card in deck.deck:
    for value in cards:
        if card.value == value and card.suit == 'spades':
            drew.hand.append(card)

print(drew.hand)
print(holdem.assess_hand(drew))
