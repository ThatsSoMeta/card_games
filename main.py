import random
import time
import argparse
import sys
# import textwrap
# from euchre import euchre


class Team:
    def __init__(self, name):
        self.name = name
        self.players = []
        self.score = 0
        self.tricks = 0
        for player in self.players:
            player.team = self

    def __repr__(self):
        return {
            "Team Name": self.name,
            "Players": self.players,
            "Score": self.score
            }

    def add_player(self, player):
        self.players.append(player)


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = sorted([], key=lambda card: card.suit)

    def __repr__(self):
        return self.name

    def deal(self, card):
        self.hand.append(card)

    def discard(self, card):
        return self.hand.pop(self.hand.index(card))


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


def war():
    """Automates a simple game of War"""
    players = []
    num_of_players = int(input('How many players? '))
    for i in range(1, num_of_players + 1):
        player = Player(input(f'Player {i} name: '))
        players.append(player)
    deck = Deck()
    deck.shuffle()
    while deck.deck:
        for player in players:
            if deck.deck:
                player.hand.append(deck.deal())
            else:
                break
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


def main(args):
    parser = argparse.ArgumentParser(
        description="""
                Play some games!
                I just need to know which one you want to play:
                """
    )
    parser.add_argument('--war', '-w', action='store_true',
                        help='Play a game of war!')
    parser.add_argument('--euchre', '-e', action='store_true',
                        help='Play a game of euchre!')

    if not args:
        parser.print_usage()
        sys.exit(1)

    ns = parser.parse_args(args)

    if ns.war:
        war()


if __name__ == "__main__":
    main(sys.argv[1:])
