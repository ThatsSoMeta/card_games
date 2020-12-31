import random


class Team:
    def __init__(self, name):
        self.name = name
        self.players = []
        self.score = 0
        self.tricks = 0
        for player in self.players:
            player.team = self

    def __repr__(self):
        if len(self.players) == 2:
            return " & ".join([player.name for player in self.players])
        else:
            return self.name

    def add_player(self, player):
        self.players.append(player)


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = sorted([], key=lambda card: card.suit)
        self.active = True
        self.bank = 0

    def __repr__(self):
        return self.name

    def deal(self, card):
        self.hand.append(card)

    def discard(self, card):
        return self.hand.pop(self.hand.index(card))

    def bid(self, bet):
        while not bet.isdigit() or int(bet) not in range(1, self.bank + 1):
            bet = input(f"Please choose a number between 1 and {self.bank}.\n$")
        try:
            self.bank -= int(bet)
            return int(bet)
        except TypeError:
            return self.bid(bet)
        except ValueError:
            return self.bid(bet)


class Card:
    def __init__(self, suit, color, name, value):
        self.suit = suit
        self.name = name
        self.value = value
        self.color = color

    def __repr__(self):
        return f"{self.name} of {self.suit.title()}"


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
        self.suits = [['hearts', 'red'], ['diamonds', 'red'], ['spades', 'black'], ['clubs', 'black']]
        self.deck = [Card(suit[0], suit[1], item['name'], item['value'])
                     for suit in self.suits
                     for item in self.values
                     ]
        self.spent_cards = []

    def __repr__(self):
        return self.deck

    def __str__(self):
        return str(self.deck)

    def deal(self):
        if not self.deck:
            raise IndexError("Deck is empty.")
        dealt_card = self.deck.pop()
        self.spent_cards.append(dealt_card)
        return dealt_card

    def shuffle(self):
        self.deck.extend(self.spent_cards)
        random.shuffle(self.deck)

    def print(self):
        print("Remaining: ", self.deck)
        print("Spent: ", self.spent_cards)
