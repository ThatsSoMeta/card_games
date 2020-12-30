from main import Player, Team, Deck
import random
import os
import time

team1 = Team('Team One')
team2 = Team('Team Two')
team1.add_player(Player('Drew'))
team1.add_player(Player('Mom'))
team2.add_player(Player('Brandi'))
team2.add_player(Player('Erin'))
teams = [team1, team2]


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


def print_game_info(player, teams, dealer, trump=None, turn_up=None, lead_suit=None, trick=None):
    print(f"It is {player}'s turn.\n")
    for team in sorted(teams, key=lambda team: team.tricks):
        print(f"{team}:\n\tTricks: {team.tricks}\n\tScore: {team.score}")
    print()
    if dealer:
        print(f"Dealer: {dealer}")
    if turn_up:
        print(f"Turn up: {turn_up}\n")
    if trump:
        print(f"Trump: {trump['suit'].title()}")
        if trump['alone']:
            print(f"{trump['called_by']} is going alone.")
    if lead_suit:
        print(f"{lead_suit.title()} was led.")


def euchre(teams):
    """
    Play a game of euchre! (kinda)
    NOTE: There will not be this many prints in the real code.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    # random.shuffle(teams)
    team1, team2 = teams
    players = []
    for i in range(2):
        players.append(team1.players[i])
        players.append(team2.players[i])
    game_active = True
    for player in players:
        if player in team1.players:
            player.team = team1
        else:
            player.team = team2
    # Gameplay logic starts below. Will likely split up into multiple functions
    # LET THE GAMES BEGIN!
    dealer = random.choice(players)
    while game_active:
        deck = Deck()
        deck.deck = [card for card in deck.deck if card.value >= 9]  # only use 9+
        deck.shuffle()
        print('Shuffling deck...\n')
        time.sleep(3)
        os.system('cls' if os.name == 'nt' else 'clear')
        current_player = dealer
        for _ in range(5):
            for player in players:
                player.deal(deck.deal())
        trump = select_trump(players, teams, dealer, current_player, deck)
        if trump['alone']:
            print(f"{trump['called_by']} is going alone.")
            for player in trump['responsibility'].players:
                if player != trump['called_by']:
                    player.active = False
        winner = None
        winning_card = None
        for _ in range(5):
            if winner:
                current_player = winner
            else:
                current_player = next_player(current_player, players)
            trick = []
            for _ in range(4):
                os.system('cls' if os.name == 'nt' else 'clear')
                if current_player.active:
                    trick.append(euchre_play(current_player, trick, dealer, teams, trump))
                else:
                    print(f"Skipping {current_player}'s turn because their partner is going alone.")
                    time.sleep(2)
                current_player = next_player(current_player, players)
                os.system('cls' if os.name == 'nt' else 'clear')
            if trick == []:
                print("For some reason the trick is empty...")
                return
            for card in trick:
                if card[1].suit != trick[0][1].suit and card[1].suit != trump['suit']:
                    if card[1] is not trump['left_bauer']:
                        card[1].value = 0
            winner, winning_card = max(trick, key=lambda x: x[1].value)
            for card in trick:
                print(f"{card[0]}:\t{card[1]}\n\tValue: {card[1].value}")
            print(f"{winner} wins with the {winning_card}!")
            winning_team = winner.team
            winning_team.tricks += 1
            print(f"{winning_team.players[0]} and {winning_team.players[1]} take the trick.\n")
            for team in sorted(teams, key=lambda team: team.score):
                print(f"{team.name}: {team.players}\n\tTricks: {team.tricks}\n\tScore: {team.score}")
            input("Press Enter to continue.")
        print("Scores:")
        teams.sort(key=lambda team: team.tricks)
        for team in teams:
            # alone = False
            if team.tricks == 5:
                if trump['alone'] and trump['called_by'] in team.players:
                    print(f"{trump['called_by']} went alone and got them all! Their team earns 4 points!")
                    team.score += 4
                else:
                    print(f"\t{team} take them all and earn 2 points!")
                    team.score += 2
            elif trump['responsibility'] != team and team.tricks > 2:
                print(f"\t{team} have euchred their opponents! They earn 2 points.")
                team.score += 2
            elif team.tricks > 2:
                print(f"\t{team} take {team.tricks} tricks and earn 1 point.")
                team.score += 1
            print(f"{team.name}: {team.players}\n\tScore: {team.score}")
        for team in teams:
            if team.score == 10:
                print(f"{team} win!!")
                game_active = False
                time.sleep(10)
                return team
        print('No winners yet...')
        input("Press Enter to continue.")
        os.system('cls' if os.name == 'nt' else 'clear')
        dealer = next_player(dealer, players)
        for team in teams:
            team.tricks = 0
            for player in team:
                player.active = True


def select_trump(players, teams, dealer, current_player, deck):
    """
    Cycle through players to select trump suit
    """
    possible_trump = [
        {'suit': 'hearts', 'color': 'red', 'responsibility': None, 'called_by': None, 'alone': False},
        {'suit': 'diamonds', 'color': 'red', 'responsibility': None, 'called_by': None, 'alone': False},
        {'suit': 'clubs', 'color': 'black', 'responsibility': None, 'called_by': None, 'alone': False},
        {'suit': 'spades', 'color': 'black', 'responsibility': None, 'called_by': None, 'alone': False}
                    ]
    trump = None
    turn_up = deck.deck[0]
    current_player = next_player(dealer, players)
    for _ in range(4):
        if not trump:
            print_game_info(current_player, teams, dealer, turn_up=turn_up)
            input(f"Press Enter when {current_player} has the computer.\n")
            hand = current_player.hand
            hand.sort(key=lambda card: card.value, reverse=True)
            hand.sort(key=lambda card: card.suit)
            print(f"{current_player.name}'s hand:\n")
            for card in hand:
                print(f"    {card}", end=" ")
            if current_player == dealer:
                print(f"\n\nYou are the dealer.\nWould you like to pick up the {turn_up}?")
            else:
                print(f"\n\nWould you like {dealer} to pick up the {turn_up}?")
            if input('\nY or N?\n').lower() in ['y', 'yes']:
                for option in possible_trump:
                    if option['suit'] == turn_up.suit:
                        trump = possible_trump.pop(possible_trump.index(option))
                trump['responsibility'] = current_player.team
                trump['called_by'] = current_player
                print("Would you like to go alone?")
                if input("\nY or N?\n").lower() in ['y', 'yes']:
                    trump['alone'] = True
                dealer.deal(turn_up)
                discard(dealer, trump)
                print(f"{trump['suit'].title()} is trump.")
            else:
                current_player = next_player(current_player, players)
        os.system('cls' if os.name == 'nt' else 'clear')
    for option in possible_trump:
        if option['suit'] == turn_up.suit:
            possible_trump.pop(possible_trump.index(option))
    options = [option['suit'] for option in possible_trump] + ['pass']
    for _ in range(4):
        os.system('cls' if os.name == 'nt' else 'clear')
        if not trump:
            # print(f"Players: {players}")
            # print(f"Dealer: {dealer}")
            hand = current_player.hand
            print_game_info(current_player, teams, dealer)
            input(f'Press Enter when {current_player.name} has the computer...\n')
            print(f"{current_player.name}'s hand:\n")
            for card in hand:
                print(f"    {card}", end=" ")
            choice = None
            if not choice:
                if current_player == dealer:
                    options.pop(options.index(options[-1]))
                print("\n\nOptions:\n")
                for i, option in enumerate(options):
                    print(f"\t{i} - {option.title()}")
                print()
                choice = input(f"{current_player.name}, what suit would you like to call?\n")
                while not choice.isdigit() or int(choice) not in range(len(options)):
                    choice = input(f"Please pick a number from the given list...\n")
                if options[int(choice)] != 'pass':
                    for suit in possible_trump:
                        if suit['suit'] == options[int(choice)]:
                            trump = suit
                    trump['responsibility'] = current_player.team
                    trump['called_by'] = current_player
                    print("Would you like to go alone?")
                    if input("\nY or N\n").lower() in ['y', 'yes']:
                        trump['alone'] = True
                    print(f"Trump: {trump['suit']}")
        current_player = next_player(current_player, players)
    while not trump:
        print(f"{dealer} must choose trump!")
        choice = input(options)
        for option in possible_trump:
            if option['suit'] == choice.lower():
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
    hand = player.hand
    hand.sort(key=lambda card: card.value, reverse=True)
    hand.sort(key=lambda card: card.suit)
    os.system('cls' if os.name == 'nt' else 'clear')
    input(f"Press Enter when {player} has the computer...\n")
    print(f"{trump['suit'].title()} is trump.\n")
    print("\nYour hand:\n")
    discard = None
    while discard is None:
        for i, card in enumerate(hand):
            print(f"\t{i} - {card}")
        print()
        choice = input(f"{player}, please select a card to discard...\n")
        while not choice.isdigit() or int(choice) not in range(len(hand)):
            choice = input('Please pick a number from the given list...\n')
        discard = hand[int(choice)]
        print(f"You have selected the {discard}.")
        if discard.suit == trump['suit']:
            print(f"The {discard} is trump. Are you sure you want to discard it?")
            confirmed = input("Y/N:\n")
            if confirmed.lower() not in ['y', 'yes']:
                discard = None
    return player.discard(discard)


def euchre_play(player, trick, dealer, teams, trump):
    """
    Looks at board and simulates game play
    """
    trump_suit = trump['suit'].lower()
    hand = player.hand
    suits_in_hand = [card.suit.lower() for card in player.hand]
    print(f"On the table: {trick}")
    print(f"It is {player}'s turn.")
    input(f"Press Enter when {player} has the computer...\n")
    if trump['left_bauer'] in hand:
        suits_in_hand.append(trump_suit)
        suits_in_hand.pop(suits_in_hand.index(trump['left_bauer'].suit.lower()))
    hand.sort(key=lambda x: x.value, reverse=True)
    hand.sort(key=lambda x: x.suit)
    selected_card = None
    print(f"\n{player}'s hand:\n")
    for i, card in enumerate(hand):
        print(f"\t{i} - {card}")
    print()
    if not trick:
        print(f"Trump is {trump_suit}.")
        # print_game_info(player, teams, dealer, trump=trump, trick=[])
        print("It is your lead. Choose any card.")
        play = input(f'{player}, which card would you like to play? ')
        while not play.isdigit() or int(play) not in range(len(hand)):
            play = input('Please pick a number from the given list... ')
        play = int(play)
        selected_card = player.discard(hand[play])
        print(f"{player} plays the {selected_card}.")
        time.sleep(1)
    else:
        if trick[0][1] == trump['left_bauer']:
            lead_suit = trump_suit
        else:
            lead_suit = trick[0][1].suit
        # print_game_info(player, teams, dealer, trump=trump, trick=trick)
        print(f"Trump is {trump_suit}.")
        print(f"{lead_suit.title()} was led.")
        while not selected_card:
            play = input(f'{player.name}, which card would you like to play?\n')
            # selected_card = None
            while not play.isdigit() or int(play) not in range(len(hand)):
                play = input('Please pick a number from the given list... ')
            play = int(play)
            if lead_suit not in suits_in_hand:
                selected_card = player.discard(hand[play])
                print(f"{player.name} has no {lead_suit}.")
                print(f"{player.name} plays the {selected_card}.")
                # input("Press Enter to continue.")
                time.sleep(1)
            else:
                if lead_suit != trump_suit:
                    if hand[play] is not trump['left_bauer']:
                        if hand[play].suit == lead_suit:
                            selected_card = player.discard(hand[play])
                            print(f"{player.name} has {lead_suit}.")
                            print(f"{player.name} plays the {selected_card}.")
                            # input('Press Enter to continue.')
                            time.sleep(1)
                        else:
                            print("You must follow suit.")
                    else:
                        print(f"That card is a {trump_suit[:-1]}. You must play {lead_suit}.")
                else:
                    if hand[play] == trump['left_bauer']:
                        selected_card = player.discard(hand[play])
                        print(f"{player.name} plays the {selected_card}.")
                        # input('Press Enter to continue.')
                        time.sleep(1)
                    elif hand[play].suit == lead_suit:
                        selected_card = player.discard(hand[play])
                        print(f"{player.name} has {lead_suit}.")
                        print(f"{player.name} plays the {selected_card}.")
                        # input('Press Enter to continue.')
                        time.sleep(1)
                    else:
                        print("You must follow suit.")
            play = None
            # print("That play is not valid. Your hand is:")
            # for i, card in enumerate(hand):
            #     print(f"{i} - {card}")
    return (player, selected_card)


if __name__ == "__main__":
    # teams = automate_team_creation()
    euchre(teams)
