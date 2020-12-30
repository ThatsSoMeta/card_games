import time
import argparse
import sys
from schemas import Player, Deck


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
