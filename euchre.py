from main import Player, Deck
import random
import os

# Drew = Player('Drew')
# Mom = Player('Mom')
# Erin = Player('Erin')
# Brandi = Player('Brandi')


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
    os.system('cls' if os.name == 'nt' else 'clear')
    deck = Deck()
    deck.deck = [card for card in deck.deck if card.value >= 9]  # only use 9+
    deck.shuffle()
    players = []
    team1 = {"score": 0, "players": []}
    team2 = {"score": 0, "players": []}
    # code below assigns teams via terminal prompt
    # this will be simplified in the actual app
    for i in range(2):
        for j in range(2):
            player = Player(input(f"Team {i + 1}, Player {j + 1} name: "))
            if i == 0:
                team1["players"].append(player)
            else:
                team2["players"].append(player)
    for i in range(2):
        players.append(team1["players"][i])
        players.append(team2["players"][i])
    # alone = False
    # game_active = True
    # Gameplay logic starts below. Will likely split up into multiple functions
    # LET THE GAMES BEGIN!
    dealer = random.choice(players)
    current_player = dealer
    print('Here we go!!')
    print(f"Players: {[player.name for player in players]}")
    print(f"Dealer: {dealer}")
    for _ in range(5):
        for player in players:
            player.deal(deck.deal())
    trump = select_trump(players, dealer, current_player, deck)
    current_player = next_player(dealer, players)
    # while game_active:
    print(f"{dealer} is dealer. Game will begin with {current_player}.")
    for _ in range(5):
        os.system('cls' if os.name == 'nt' else 'clear')
        trick = []
        for player in players:
            trick.append(euchre_play(current_player, trick, dealer, players, trump))
            print(f"{current_player}'s turn ends.")
            current_player = next_player(current_player, players)
            os.system('cls' if os.name == 'nt' else 'clear')
        trick_values = [hand[1].value for hand in trick]
        for hand in trick:
            if hand[1].value == max(trick_values):
                winner = hand
        print(f"Winning card: {winner}")
        winning_team = team1 if winner[0] in team1 else team2
        print(f"{winning_team['players'][0]} and {winning_team['players'][1]} take the trick.")


def select_trump(players, dealer, current_player, deck):
    possible_trump = [
        {'suit': 'hearts', 'color': 'red'},
        {'suit': 'diamonds', 'color': 'red'},
        {'suit': 'clubs', 'color': 'black'},
        {'suit': 'spades', 'color': 'black'},
                    ]
    trump = None
    turn_up = deck.deck[0]
    print(f"Turn up: {turn_up.name} of {turn_up.suit}")
    current_player = next_player(dealer, players)
    print(f"{current_player}'s turn!")
    for _ in range(4):
        if not trump:
            print(f"Players: {players}")
            input(f"Press Enter when {current_player.name} has the computer...")
            print()
            print(f"{current_player.name}'s hand: {current_player.hand}")
            print(f"""\tWould you like {dealer} to pick up the {turn_up.name} of {turn_up.suit}?""")
            if input('Y or N? ').lower() in ['y', 'yes']:
                for option in possible_trump:
                    if option['suit'] == turn_up.suit:
                        trump = possible_trump.pop(possible_trump.index(option))
                dealer.deal(turn_up)
                discard(dealer, trump)
                # dealer.discard(min(dealer.hand, key=lambda x: x.value))
                print(f"Press Enter when {current_player} has the computer...\n")
                print(f"Trump is {trump['suit']}.")
            else:
                print(f"{current_player} ends turn. {next_player(current_player, players)} is next.")
                current_player = next_player(current_player, players)
                print(f"{current_player}'s turn.")
        os.system('cls' if os.name == 'nt' else 'clear')
    for option in possible_trump:
        if option['suit'] == turn_up.suit:
            possible_trump.pop(possible_trump.index(option))
    options = [option['suit'] for option in possible_trump] + ['pass']
    for _ in range(4):
        os.system('cls' if os.name == 'nt' else 'clear')
        if not trump:
            print(f"Players: {players}")
            print(f"Dealer: {dealer}")
            input(f'Press Enter when {current_player.name} has the computer...\n')
            print()
            print(f"{current_player.name}'s hand: {current_player.hand}")
            request = None
            if not request:
                if current_player == dealer:
                    options.pop(options.index(options[-1]))
                for i, option in enumerate(options):
                    print(f"{i} - {option.title()}")
                request = input(f"{current_player.name}, what suit would you like to call?\n")
                while not request.isdigit() or int(request) not in range(len(options)):
                    request = input(f"Please pick a number from the given list...\n")
                if options[int(request)] != 'pass':
                    for suit in possible_trump:
                        if suit['suit'] == options[int(request)]:
                            trump = suit
                            print(f"Trump: {trump}")
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
    return trump


def discard(player, trump):
    hand = player.hand
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{trump['suit']} is trump.")
    input(f"Press Enter when {player} has the computer...\n")
    print("Your hand:")
    discard = None
    while not discard:
        for i, card in enumerate(hand):
            print(f"{i} - {card.name} of {card.suit}")
        discard = input(f"{player}, please select a card to discard?\n")
        while not discard.isdigit() or int(discard) not in range(len(hand)):
            discard = input('Please pick a number from the given list...\n')
        discard = hand[int(discard)]
    return player.discard(discard)
    # print(f"Table: {trick}")
    # for i, card in enumerate(hand):
    #     print(f"{i} - {card.name} of {card.suit}")
    # play = input(f'{player}, which card would you like to play? ')
    # while int(play) not in range(len(hand)) or not play.isdigit():
    #     play = input('Please pick a number from the given list...')
    # play = int(play)
    # if hand[play].suit != lead_suit and lead_suit in suits_in_hand:
    #     print(f"You must follow suit by playing {lead_suit}...")
    #     play = None
    #     print(f"{trump['suit'].title()} is trump.")

    discard = input('Please select a card to discard.\n')

def euchre_play(player, trick, dealer, players, trump):
    input(f"Press Enter when {player} has the computer...\n")
    hand = player.hand
    suits_in_hand = [card.suit for card in player.hand]
    hand.sort(key=lambda x: x.value, reverse=True)
    print(f"Players: {players}")
    print(f"Dealer: {dealer}")
    print(f"It is {player}'s turn...")
    print(f"Trump is {trump['suit']}")
    print(f"On the table: {trick}")
    print("Your hand:")
    if not trick:
        for i, card in enumerate(hand):
            print(f"{i} - {card.name} of {card.suit}")
        play = input('Which card would you like to play? ')
        while not play.isdigit() or int(play) not in range(len(hand)):
            play = input('Please pick a number from the given list... ')
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
        print(f"{player} plays {hand[play].name} of {hand[play].suit}")
        return (player, hand.pop(play))


def check_winner(teams):
    for team in teams:
        if team['score'] == 10:
            print(f"{team['players'][0]} and {team['players'][1]} win!!")
            return team


if __name__ == "__main__":
    euchre()
