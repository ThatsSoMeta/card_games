import random
import time


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def __repr__(self):
        return self.name


class Card:
    def __init__(self, suit, name, value):
        self.suit = suit
        self.name = name
        self.value = value

    def __repr__(self):
        return str(f'{self.name} {self.suit}')


class Deck:
    def __init__(self):
        self.values = [
            {'name': '2', 'value': 2},
            {'name': '3', 'value': 3},
            {'name': '4', 'value': 4},
            {'name': '5', 'value': 5},
            {'name': '6', 'value': 6},
            {'name': '7', 'value': 7},
            {'name': '8', 'value': 8},
            {'name': '9', 'value': 9},
            {'name': '10', 'value': 10},
            {'name': 'J', 'value': 11},
            {'name': 'Q', 'value': 12},
            {'name': 'K', 'value': 13},
            {'name': 'A', 'value': 14},
            ]
        self.suits = ['hearts', 'diamonds', 'spades', 'clubs']
        self.deck = [Card(suit, item['name'], item['value'])
                     for suit in self.suits
                     for item in self.values
                     ]
        self.spent_cards = []

    def __repr__(self):
        return self.deck

    def deal(self):
        dealt_card = self.deck.pop()
        self.spent_cards.append(dealt_card)
        return dealt_card

    def shuffle(self):
        self.deck = self.deck + self.spent_cards
        random.shuffle(self.deck)

    def print(self):
        print("Remaining: ", self.deck)
        print("Spent: ", self.spent_cards)


# players = [Player(name) for name in ['Mom', 'Erin', 'Drew', 'Brandi']]
players = [Player(name) for name in ['Mom', 'Drew']]


def war():
    players = []
    num_of_players = int(input('How many players? '))
    for i in range(1, num_of_players + 1):
        player = Player(input(f'Player {i} name: '))
        players.append(player)
    deck = Deck()
    deck.shuffle()
    while deck.deck:
        for player in players:
            player.hand.append(deck.deal())
    hands = [player.hand for player in players]
    rounds = min([len(hand) for hand in hands])
    for player in players:
        player.points = 0
    for _ in range(rounds):
        trick = [[player, player.hand.pop()] for player in players]
        print(trick)
        winner = max(trick, key=lambda x: x[1].value)[0]
        print(f'{winner} wins!')
        winner.points += 1
        time.sleep(1)
    for player in players:
        print(player, player.points)


war()
