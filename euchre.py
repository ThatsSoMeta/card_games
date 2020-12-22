from main import Player, Deck
import random
import os

Drew = Player('Drew')
Mom = Player('Mom')
Erin = Player('Erin')
Brandi = Player('Brandi')


def next_player(current_player, players):
    """Returns the next player in the game"""
    if current_player != players[-1]:
        return players[players.index(current_player) + 1]
    else:
        return players[0]


def euchre():
    """
    Play a game of euchre! (kinda)
    NOTE: There will not be this many prints in the real code.
    """
    deck = Deck()
    deck.deck = [card for card in deck.deck if card.value >= 9]  # only use 9+
    deck.shuffle()
    game_active = True
    trump = None
    alone = False
    possible_trump = [
        {'suit': 'hearts', 'color': 'red'},
        {'suit': 'diamonds', 'color': 'red'},
        {'suit': 'clubs', 'color': 'black'},
        {'suit': 'spades', 'color': 'black'},
                    ]
    team1 = {"score": 0, "players": [Drew, Mom]}
    team2 = {"score": 0, "players": [Erin, Brandi]}
    # code below assigns teams via terminal prompt
    # this will be simplified in the actual app
    # for i in range(2):
    #     for j in range(2):
    #         player = Player(input(f"Team {i + 1}, Player {j + 1} name: "))
    #         if i == 0:
    #             team1["players"].append(player)
    #         else:
    #             team2["players"].append(player)
    players = []
    for i in range(2):
        players.append(team1["players"][i])
        players.append(team2["players"][i])
    # Gameplay logic starts below. Will likely split up into multiple functions
    dealer = random.choice(players)
    current_player = dealer
    print(f"Current Player: {current_player}")
    print('Here we go!!')
    print(f"Players: {[player.name for player in players]}")
    print(f"Dealer: {dealer}")
    for _ in range(5):
        for player in players:
            player.deal(deck.deal())
    turn_up = deck.deck[0]
    print(f"Turn up: {turn_up.name} of {turn_up.suit}")
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
    while not trump:
        print(f"{dealer} must choose trump!")
        request = input(options)
        for option in possible_trump:
            if option['suit'] == request.lower():
                trump = possible_trump.pop(possible_trump.index(option))
                print(f"Trump is {trump['suit']}.")
    for card in (deck.deck + deck.spent_cards):
        if card.color == trump['color'] and card.name == 'J':
            if card.suit == trump['suit']:
                card.value += 25
            else:
                card.value += 20
        elif card.suit == trump['suit']:
            card.value += 13
    # LET THE GAMES BEGIN!
    current_player = next_player(dealer, players)
    # while game_active:
    print(f"{dealer} is dealer. Game will begin with {current_player}")
    for _ in range(5):
        os.system('cls' if os.name == 'nt' else 'clear')
        trick = []
        for player in players:
            trick.append(euchre_play(current_player, trick, players, trump))
            print(f"{current_player}'s turn ends.")
            current_player = next_player(current_player, players)
            os.system('cls' if os.name == 'nt' else 'clear')
        trick_values = [hand[1].value for hand in trick]
        for hand in trick:
            if hand[1].value == max(trick_values):
                winner = hand
        print(f"Winning card: {winner}")
        winning_team = team1 if winner[0] in team1 else team2
        winning_team['score'] += 1
        print(f"Winning team: {winning_team}")


def euchre_play(player, trick, players, trump):
    input(f"Press Enter when {player} has the computer...")
    hand = player.hand
    suits_in_hand = [card.suit for card in player.hand]
    hand.sort(key=lambda x: x.value, reverse=True)
    print(f"It is {player}'s turn...")
    print(f"Trump is {trump['suit']}")
    print(f"On the table: {trick}")
    if not trick:
        for i, card in enumerate(hand):
            print(f"{i} - {card.name} of {card.suit}")
        play = input('Which card would you like to play? ')
        while not play.isdigit() or int(play) not in range(len(hand)):
            play = input('Please pick a number from the given list...')
        play = int(play)
        print(f"{player} plays {hand[play]}")
        return (player, hand.pop(play))
    else:
        lead_suit = trick[0][1].suit
        print(f"{lead_suit.title()} was led.")
        play = None
        while not play:
            print(f"Table: {trick}")
            for i, card in enumerate(hand):
                print(f"{i} - {card.name} of {card.suit}")
            play = input(f'{player}, which card would you like to play? ')
            while int(play) not in range(len(hand)) or not play.isdigit():
                play = input('Please pick a number from the given list...')
            play = int(play)
            if hand[play].suit != lead_suit and lead_suit in suits_in_hand:
                print(f"You must follow suit by playing {lead_suit}...")
                play = None
                print(f"{trump['suit'].title()} is trump.")
            else:
                pass
        print(f"{player} plays {hand[play].name} of {hand[play].suit}")
        return (player, hand.pop(play))


if __name__ == "__main__":
    euchre()
