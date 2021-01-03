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
        self.is_active = True
        self.bank = 0
        self.current_bet = 0

    def __repr__(self):
        return self.name

    def deal(self, cards):
        self.hand.extend(cards)

    def discard(self, card):
        try:
            return self.hand.pop(self.hand.index(card))
        except ValueError:
            print(f"{card} not in hand.")

    def bet(self, bet):
        if type(bet) != int:
            while not bet.isdigit() or int(bet) not in range(1, self.bank + 1):
                bet = input(f"Please choose a number between 1 and {self.bank}.\n$")
        try:
            self.bank -= int(bet)
            return int(bet)
        except TypeError:
            return self.bet(bet)
        except ValueError:
            return self.bet(bet)


class Card:
    def __init__(self, suit, color, name, value):
        self.suit = suit
        self.name = name
        self.value = value
        self.color = color

    def __repr__(self):
        return f"{self.name} of {self.suit.title()}"


class Deck:
    def __init__(self, count=1):
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
                     for _ in range(count)
                     ]
        self.spent_cards = []

    def __repr__(self):
        return self.deck

    def __str__(self):
        return str(self.deck)

    def deal(self, num_of_cards=1):
        if not self.deck:
            raise IndexError("Deck is empty.")
        cards_to_deal = []
        for _ in range(num_of_cards):
            dealt_card = self.deck.pop()
            self.spent_cards.append(dealt_card)
            cards_to_deal.append(dealt_card)
        return cards_to_deal

    def shuffle(self):
        self.deck.extend(self.spent_cards)
        random.shuffle(self.deck)

    def print(self):
        print("Remaining: ", self.deck)
        print("Spent: ", self.spent_cards)


def next_player(current_player, players):
    """Returns the next player in the game"""
    if len(players) == 1:
        return players[0]
    if current_player != players[-1]:
        return players[players.index(current_player) + 1]
    return players[0]
