from main import Player, Team, Deck
import random
import os
import time

# Drew = Player('Drew')
# Mom = Player('Mom')
# Erin = Player('Erin')
# Brandi = Player('Brandi')

team_schema = {"score": 0, "players": [], "tricks": 0}


def next_player(current_player, players):
    """Returns the next player in the game"""
    if current_player != players[-1]:
        return players[players.index(current_player) + 1]
    else:
        return players[0]


def automate_team_creation():
    # code below assigns teams via terminal prompt
    # this will be simplified in the actual app
    """Creates teams"""
    # code below would be useful for other games
    # how_many_teams = input("How many teams do you need?\n")
    # while not how_many_teams.isdigit():
    #     how_many_teams = input("Integers only, please.... ")
    # how_many_players = input("How many players per team?\n")
    # while not how_many_players.isdigit():
    #     how_many_players = input("Integers only please\n")
    how_many_teams = 2
    how_many_players = 2
    teams = []
    for i in range(int(how_many_teams)):
        name = input(f"Team {i + 1} name:\n")
        while not name:
            print("Come on. We need to call you something.")
            name = input(f"Team {i + 1} name:\n")
        team = Team(name)
        for j in range(int(how_many_players)):
            name = input(f"{team.name} - Player {j + 1} name:\n")
            while not name:
                print("We need a way to address you...")
                name = input(f"{team.name} - Player {j + 1} name:\n")
            player = Player(name)
            team.players.append(player)
        teams.append(team)
    return teams


def euchre(teams):
    """
    Play a game of euchre! (kinda)
    NOTE: There will not be this many prints in the real code.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    team1, team2 = teams
    players = []
    for i in range(2):
        players.append(team1.players[i])
        players.append(team2.players[i])
    game_active = True
    # Gameplay logic starts below. Will likely split up into multiple functions
    # LET THE GAMES BEGIN!
    dealer = random.choice(players)
    while game_active:
        deck = Deck()
        deck.deck = [card for card in deck.deck if card.value >= 9]  # only use 9+
        print('Shuffling deck...')
        deck.shuffle()
        time.sleep(5)
        dealer = next_player(dealer, players)
        current_player = dealer
        print('Here we go!!')
        print('Scores:')
        for team in teams:
            print(f"\t{team.name}: {team.score}")
        print(f"Players: {[player.name for player in players]}")
        print(f"Dealer: {dealer}")
        for _ in range(5):
            for player in players:
                player.deal(deck.deal())
        trump = select_trump(players, dealer, current_player, deck)
        current_player = next_player(dealer, players)
        print(f"{dealer} is dealer. Game will begin with {current_player}.")
        # alone = False
        for _ in range(5):
            trick = []
            for _ in range(4):
                os.system('cls' if os.name == 'nt' else 'clear')
                trick.append(euchre_play(current_player, trick, dealer, players, trump))
                print(f"{current_player}'s turn ends.")
                current_player = next_player(current_player, players)
                os.system('cls' if os.name == 'nt' else 'clear')
            trick_values = [card[1].value for card in trick]
            for card in trick:
                if card[1].value == max(trick_values):
                    winner = card
            print(f"Winning card: {winner}")
            winning_team = team1 if winner[0] in team1.players else team2
            winning_team.tricks += 1
            print(f"{winning_team.players[0]} and {winning_team.players[1]} take the trick.")
            print(f"Tricks:")
            for team in teams:
                print(f"\t{team.name}: {team.tricks}")
            time.sleep(5)
        print("Scores:")
        for team in teams:
            if team.tricks > 2:
                team.score += 1
            print(f"\t{team.players[0]} and {team.players[1]} have {team.score} points")
        time.sleep(5)
        check_winner([team1, team2])
        for team in teams:
            if team.score == 10:
                print(f"{team.players[0]} and {team.players[1]} win!!")
                game_active = False
                time.sleep(10)
                return team
        print('No winners yet...')



def update_scores(teams):
    """Updates scoreboard"""
    print("Scores:")
    for team in teams:
        if team.tricks > 2:
            team.score += 1
        print(f"\t{team.players[0]} and {team.players[1]} have {team.score} points")
    time.sleep(5)


def check_winner(teams):
    """Updates scores and determines if game is over"""
    for team in teams:
        if team.score == 10:
            print(f"{team.players[0]} and {team.players[1]} win!!")
            game_active = False
            time.sleep(10)
            return team
    return None


def select_trump(players, dealer, current_player, deck):
    """
    Cycle through players to select trump suit
    """
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
            print(f"\tWould you like {dealer} to pick up the {turn_up.name} of {turn_up.suit}?")
            if input('\tY or N? ').lower() in ['y', 'yes']:
                for option in possible_trump:
                    if option['suit'] == turn_up.suit:
                        trump = possible_trump.pop(possible_trump.index(option))
                dealer.deal(turn_up)
                discard(dealer, trump)
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
                trump['left_bauer'] = card
                card.value += 20
        elif card.suit == trump['suit']:
            card.value += 13
    return trump


def discard(player, trump):
    """
    Allow player to choose card to discard.
    Trump passed in only to help you make a good decision.
    """
    hand = sorted(player.hand, key=lambda card: card.value)
    hand.sort(key=lambda card: card.suit)
    os.system('cls' if os.name == 'nt' else 'clear')
    input(f"Press Enter when {player} has the computer...\n")
    print(f"{trump['suit'].title()} is trump.")
    print("\nYour hand:\n")
    discard = None
    while not discard:
        for i, card in enumerate(hand):
            print(f"\t{i} - {card.name} of {card.suit}")
        print()
        discard = input(f"{player}, please select a card to discard...\n")
        while not discard.isdigit() or int(discard) not in range(len(hand)):
            discard = input('Please pick a number from the given list...\n')
        discard = hand[int(discard)]
    return player.discard(discard)


def euchre_play(player, trick, dealer, players, trump):
    """
    Looks at board and simulates game play
    """
    input(f"Press Enter when {player} has the computer...\n")
    trump_suit = trump['suit']
    hand = sorted(player.hand, key=lambda card: card.suit)
    suits_in_hand = [card.suit for card in player.hand]
    if trump['left_bauer'] in hand:
        suits_in_hand.append(trump['suit'])
        suits_in_hand.pop(suits_in_hand.index(trump['left_bauer'].suit))
    hand.sort(key=lambda x: x.value, reverse=True)
    print(f"It is {player}'s turn...")
    print(f"Players: {players}\nDealer: {dealer}")
    print(f"Trump is {trump['suit']}")
    print(f"On the table: {trick}")
    print("\nYour hand:\n")
    for i, card in enumerate(hand):
        print(f"\t{i} - {card}")
    print()
    if not trick:
        play = input('Which card would you like to play? ')
        while not play.isdigit() or int(play) not in range(len(hand)):
            play = input('Please pick a number from the given list... ')
        play = int(play)
        print(f"{player} plays {hand[play]}")
        return (player, hand.pop(play))
    else:
        lead_suit = trick[0][1].suit
        # playable_cards = []
        # for card in hand:
        #     if card.suit == lead_suit:
        #         playable_cards.append(card)
        print(f"{lead_suit.title()} was led.")
        play = None
        while play not in range(len(hand)):
            play = input(f'{player}, which card would you like to play?\n')
            while int(play) not in range(len(hand)) or not play.isdigit():
                play = input('Please pick a number from the given list...')
            play = int(play)
            if lead_suit == trump['suit']:
                if lead_suit in suits_in_hand or trump['left_bauer'] in hand:
                    if hand[play].suit != lead_suit and hand[play] != trump['left_bauer']:
                        print(f"You must follow suit by playing {lead_suit} or {trump['left_bauer']}...")
                        play = None
                        print(f"{trump['suit'].title()} is trump.")
            else:
                if hand[play] == trump['left_bauer']:
                    print(f'That is the left bauer. It is considered {trump_suit}.')
                    play = None
        print(f"{player} plays {hand[play].name} of {hand[play].suit}")
        return (player, hand.pop(play))


if __name__ == "__main__":
    teams = automate_team_creation()
    euchre(teams)
