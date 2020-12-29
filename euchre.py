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


def euchre(teams):
    """
    Play a game of euchre! (kinda)
    NOTE: There will not be this many prints in the real code.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    random.shuffle(teams)
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
        current_player = dealer
        print('Here we go!!')
        print(f"Players: {[player.name for player in players]}")
        print(f"Dealer: {dealer}")
        for _ in range(5):
            for player in players:
                player.deal(deck.deal())
        trump = select_trump(players, dealer, current_player, deck)
        winner = None
        winning_card = None
        for _ in range(5):
            lead_suit = None
            print(f"{dealer} is dealer. Round will begin with {current_player}.")
            # alone = False
            if winner:
                current_player = winner
            else:
                current_player = next_player(current_player, players)
            trick = []
            for _ in range(4):
                os.system('cls' if os.name == 'nt' else 'clear')
                trick.append(euchre_play(current_player, trick, dealer, players, trump))
                print(f"{current_player}'s turn ends.")
                current_player = next_player(current_player, players)
                os.system('cls' if os.name == 'nt' else 'clear')
            # trick = [card for card in trick]
            # trick_values = [card[1].value for card in trick]
            if trick == []:
                print("For some reason the trick is empty...")
                return
            for card in trick:
                if card[1].suit != lead_suit and card[1].suit != trump['suit'] and card[1] is not trump['left_bauer']:
                    card[1].value = 0
            winner, winning_card = max(trick, key=lambda x: x[1].value)
            print(f"Winner: {winner} with the {winning_card}")
            winning_team = team1 if winner in team1.players else team2
            winning_team.tricks += 1
            print(f"{winning_team.players[0]} and {winning_team.players[1]} take the trick.")
            print("Tricks:")
            for team in teams:
                print(f"\t{team.name}: {team.tricks}")
            time.sleep(5)
        print("Scores:")
        for team in teams:
            if team.tricks == 5:
                print(f"\t{team.players[0]} and {team.players[1]} take them all and get 2 points!")
                team.score += 2
            elif team.tricks > 2:
                team.score += 1
            print(f"\t{team.players[0]} and {team.players[1]} now have {team.score} points")
        time.sleep(5)
        for team in teams:
            if team.score == 10:
                print(f"{team.players[0]} and {team.players[1]} win!!")
                game_active = False
                time.sleep(10)
                return team
        print('No winners yet...')
        dealer = next_player(dealer, players)
        for team in teams:
            team.tricks = 0


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
                print("\nOptions:")
                for i, option in enumerate(options):
                    print(f"\t{i} - {option.title()}")
                print()
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
    trump_suit = trump['suit'].lower()
    hand = player.hand
    suits_in_hand = [card.suit.lower() for card in player.hand]
    if trump['left_bauer'] in hand:
        suits_in_hand.append(trump_suit)
        suits_in_hand.pop(suits_in_hand.index(trump['left_bauer'].suit.lower()))
    hand.sort(key=lambda x: x.value, reverse=True)
    hand.sort(key=lambda x: x.suit)
    selected_card = None
    print(f"It is {player}'s turn...")
    print(f"Players: {players}\nDealer: {dealer}")
    print(f"{trump_suit.title()} is trump.")
    print(f"On the table: {trick}")
    print(f"\n{player}'s hand:\n")
    for i, card in enumerate(hand):
        print(f"\t{i} - {card}")
    print()
    if not trick:
        play = input(f'{player}, which card would you like to play? ')
        while not play.isdigit() or int(play) not in range(len(hand)):
            play = input('Please pick a number from the given list... ')
        play = int(play)
        selected_card = player.discard(hand[play])
    else:
        lead_suit = trick[0][1].suit.lower()
        print(f"{lead_suit.title()} was led.")
        while not selected_card:
            play = input(f'{player.name}, which card would you like to play?\n')
            # selected_card = None
            while not play.isdigit() or int(play) not in range(len(hand)):
                play = input('Please pick a number from the given list... ')
            play = int(play)
            if lead_suit not in suits_in_hand:
                selected_card = player.discard(hand[play])
                print(f"{player.name} selects {selected_card}.")
            else:
                if hand[play].suit == lead_suit:
                    selected_card = player.discard(hand[play])
                    print(f"{player.name} selects {selected_card}.")
                else:
                    if lead_suit == trump_suit and hand[play] == trump['left_bauer']:
                        selected_card = player.discard(hand[play])
                        print(f"{player.name} selects {selected_card}.")
            play = None
            print("That play is not valid...")
                    # else:
                    #     # print('Invalid play, please try again.')
                    #     selected_card = None
    if selected_card:
        print(f"{player.name} plays {selected_card}.")
        return (player, selected_card)
    else:
        print("Card selection failed...")
        return euchre_play(player, trick, dealer, players, trump)


if __name__ == "__main__":
    # teams = automate_team_creation()
    euchre(teams)
