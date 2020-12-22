import random
import time
import argparse
import sys
# import textwrap


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def __repr__(self):
        return self.name

    def deal(self, card):
        self.hand.append(card)

    def discard(self, card):
        self.hand.pop(self.hand.index(card))


class Card:
    def __init__(self, suit, color, name, value):
        self.suit = suit
        self.name = name
        self.value = value
        self.color = color

    def __repr__(self):
        return str(f'({self.name}, {self.suit}, {self.value})')


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


def next_player(current_player, players):
    """Returns the next player in the game"""
    if current_player != players[-1]:
        return players[players.index(current_player) + 1]
    else:
        return players[0]


def euchre():
    """Play a game of euchre! (kinda)"""
    deck = Deck()
    deck.deck = [card for card in deck.deck if card.value >= 9]  # only use 9+
    deck.shuffle()
    trump = None
    possible_trump = [
        {'suit': 'hearts', 'color': 'red'},
        {'suit': 'diamonds', 'color': 'red'},
        {'suit': 'clubs', 'color': 'black'},
        {'suit': 'spades', 'color': 'black'},
                    ]
    team1 = {"score": 0, "players": []}
    team2 = {"score": 0, "players": []}
    # code below assigns teams via terminal prompt
    for i in range(2):
        for j in range(2):
            player = Player(input(f"Team {i + 1}, Player {j + 1} name: "))
            if i == 0:
                team1["players"].append(player)
            else:
                team2["players"].append(player)
    players = []
    for i in range(2):
        players.append(team1["players"][i])
        players.append(team2["players"][i])
    # Gameplay logic starts below. Will likely split up into multiple functions
    dealer = random.choice(players)
    current_player = dealer
    print(f"Current Player: {current_player}")
    print('Here we go!!')
    print(f"Players: {players}")
    print(f"Dealer: {dealer}")
    for _ in range(5):
        for player in players:
            player.deal(deck.deal())
    print([(player.name, player.hand) for player in players])
    turn_up = deck.deck[0]
    print(f"Turn up: {turn_up}")
    current_player = next_player(dealer, players)
    print(f"{current_player}'s turn!")
    for i in range(4):
        if not trump:
            print()
            print(f"{current_player.name}'s hand: {current_player.hand}")
            print(f"""\tWould you like {dealer} to pick up the {turn_up.name} of {turn_up.suit}?""")
            if input('Y or N? ').lower() in ['y', 'yes']:
                for option in possible_trump:
                    if option['suit'] == turn_up.suit:
                        trump = possible_trump.pop(possible_trump.index(option))
                dealer.deal(turn_up)
                dealer.discard(min(dealer.hand, key=lambda x: x.value))
                print(f"Trump is {trump['suit']}.")
                # for card in ([', '.join(player.hand) for player in players] + deck.deck):
                #     if card.suit == trump['suit'] and card.name == 'J':
                #         print(card)
                #         card.value += 25
                #         print(card)
                #     elif card.color == trump['color'] and card.suit != trump['suit'] and card.name == 'J':
                #         print(card)
                #         card.value += 20
                #         print(card)
                #     elif card.suit == trump['suit'] and card.name != 'J':
                #         print(card)
                #         card.value += 13
                #         print(card)
                #     time.sleep(1)
            else:
                print(f"{current_player} ends turn. {next_player(current_player, players)} is next.")
                current_player = next_player(current_player, players)
                print(f"{current_player}'s turn.")
        for option in possible_trump:
            if option['suit'] == turn_up.suit:
                possible_trump.pop(possible_trump.index(option))
    options = [option['suit'] for option in possible_trump]
    for i in range(4):
        if not trump:
            print()
            print(f"{current_player.name}'s hand: {current_player.hand}")
            print(f"{current_player.name}, what suit would you like to call (if any)?")
            request = input(options)
            for option in possible_trump:
                if option['suit'] == request.lower():
                    trump = possible_trump.pop(possible_trump.index(option))
                    print(f"Trump is {trump['suit']}.")
        current_player = next_player(current_player, players)
    print(f"Trump: {trump}")
    while not trump:
        print(f"{dealer} must choose trump!")
        request = input(options)
        for option in possible_trump:
                if option['suit'] == request.lower():
                    trump = possible_trump.pop(possible_trump.index(option))
                    print(f"Trump is {trump['suit']}.")

    # print(f"{dealer}'s new hand: {dealer.hand}")
    # print(f"Deck after trump called: {deck.deck}")
    # print(f'Hands: {[player.hand for player in players]}')
    print(f"Dealer: {dealer}")
    print(f"Order: {players}")
    print(f'Game continues... it is now {current_player}\'s turn')


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
    if ns.euchre:
        euchre()


if __name__ == "__main__":
    main(sys.argv[1:])
