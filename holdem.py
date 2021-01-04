from schemas import Deck, Player, next_player, previous_player
import random
import os


hand_values = {
    "high_card": 1,
    "pair": 2,
    "two_pair": 3,
    "three_of_a_kind": 4,
    "straight": 5,
    "flush": 6,
    "full_house": 7,
    "four_of_a_kind": 8,
    "straight_flush": 9,
    "royal_flush": 10
}


def check_winners(players, board_cards=[]):
    """Compares everyone's best hand and determines winner"""
    all_hands = {player: assess_hand(player) for player in players}
    best_hand_value = max(
        [hand_values[player[0]] for player in all_hands.values()]
    )
    for hand, value in hand_values.items():
        if value == best_hand_value:
            best_hand = hand
    winners = [
        [player, hand[0], hand[1], player.hand]
        for player, hand in all_hands.items()
        if hand[0] == best_hand
    ]
    if len(winners) == 1:
        return winners
    else:
        winners.sort(
            key=lambda winner: winner[2][0].value,
            reverse=True
        )
        if winners[0][3]:
            values_list = [
                tuple(
                    card.value
                    for card in winner[3]
                )
                for winner in winners
            ]
        else:
            values_list = [
                tuple(
                    card.value
                    for card in winner[2]
                )
                for winner in winners
            ]
        values_set = {tuple(vals) for vals in values_list}
        if len(values_set) < len(values_list):
            for winner in winners:
                player = winner[0]
                player.hand = winner[2] + winner[3]
        if winners[0][2][0].value > winners[1][2][0].value:
            return winners[:1]
        elif winners[0][3]:
            winners.sort(key=lambda winner: winner[3][0].value)
            winner = None
            for i in range(len(winners[0][3])):
                if len(winners) == 1:
                    winner = winners
                if not winner:
                    first_player_card = winners[0][3][i]
                    second_player_card = winners[1][3][i]
                    if first_player_card.value > second_player_card.value:
                        winners.pop(1)
                    elif first_player_card.value < second_player_card.value:
                        winners.pop(0)
                    if winner:
                        return winners
                else:
                    return winners
        else:
            return winners


def assess_hand(player, board_cards=[]):
    """Looks at player's cards and determines best poker hand"""
    full_hand = player.hand + board_cards
    hand = sorted(full_hand, key=lambda card: card.value, reverse=True)
    values = {}
    suits = {}
    names = {}
    possible_plays = {}
    for card in hand:
        try:
            values[card.value] += 1
        except KeyError:
            values[card.value] = 1
        try:
            suits[card.suit] += 1
        except KeyError:
            suits[card.suit] = 1
        try:
            names[card.name] += 1
        except KeyError:
            names[card.name] = 1
    vals = sorted([val for val in values.keys()])
    for count in suits.values():
        if count == 5:
            if vals == list(range(min(vals), max(vals) + 1)):
                if max(vals) == 14:
                    possible_plays["royal_flush"] = [
                        card for card in hand
                    ]
                else:
                    possible_plays["straight_flush"] = [
                        card for card in hand
                    ]
            else:
                possible_plays["flush"] = [
                    card for card in hand
                ]
    for value, count in values.items():
        if count == 4:
            possible_plays["four_of_a_kind"] = [
                card for card in hand if card.value == value
            ]
        elif count == 3:
            possible_plays["three_of_a_kind"] = [
                card for card in hand if card.value == value
            ]
        elif count == 2:
            try:
                new_pair = [
                    card for card in hand if card.value == value
                ]
                if possible_plays['pair'][0].value > new_pair[0].value:
                    possible_plays["pair"].extend(new_pair)
                else:
                    possible_plays["pair"] = new_pair.extend(
                        possible_plays["pair"]
                    )
            except KeyError:
                possible_plays["pair"] = [
                    card for card in hand if card.value == value
                ]
            if len(possible_plays["pair"]) == 4:
                possible_plays["two_pair"] = possible_plays["pair"]
    if len(vals) == 5 and vals == list(range(min(vals), max(vals) + 1)):
        possible_plays["straight"] = [card for card in hand]
    if "pair" in possible_plays and "three_of_a_kind" in possible_plays:
        possible_plays["full_house"] = (
            possible_plays["three_of_a_kind"] + possible_plays["pair"]
        )
    possible_plays["high_card"] = [hand[0]]
    possible_plays = [play for play in possible_plays.items()]
    best_hand = list(
        max(possible_plays, key=lambda play: hand_values[play[0]])
    )
    for card in best_hand[1]:
        player.discard(card)
    print()
    player.hand.sort(key=lambda card: card.value, reverse=True)
    return best_hand


def place_bets(args):
    players = args["players"]
    player = args["current_player"]
    blinds = args["blinds"]
    pot = args["pot"]
    board_cards = args["board_cards"]
    # play = args["play"]
    big_blind = args['big_blind']
    # small_blind = args['small_blind']
    betting_active = True
    checks = []
    folded_players = []
    minimum_bet = 0
    count = 1
    bet = 0
    while betting_active:
        active_players = [
            player for player in players
            if player.is_active
        ]
        active_bets = [
            int(player.current_bet) for player in active_players
        ]
        if len(set(active_bets)) == 1 and active_bets[0] != 0:
            if player is not big_blind:
                print(
                    f"Betting is done. All players have bet ${active_bets[0]}."
                )
                break
        minimum_bet = max(active_bets)
        if player.is_active and player.bank:
            os.system('cls' if os.name == 'nt' else 'clear')
            kitty = sum([
                int(player.current_bet) for player in players
            ])
            # print(f"It is {player}'s turn.\n")
            print(f"Player: {player}")
            print(f"Bank: ${player.bank - player.current_bet}")
            print(f"Current Bet: ${player.current_bet}")
            print(f"Minimum Bet: ${minimum_bet}\n")
            print("\tPlayer:\t\tCurrent Bet:")
            for name in active_players:
                print(f"\t{name}\t\t${name.current_bet}")
            print(f"\nPot: ${pot}\nKitty: ${kitty}")
            print("\nOn the table:")
            for card in board_cards:
                print(f"\t{card}")
            input(f"\nPress Enter when {player} has the computer.")
            # print(f"\n{player}'s current bet: ${player.current_bet}")
            print(f"\n{player}'s hand:")
            for card in player.hand:
                print(f"\t{card}")
            # print(f"\n{player}, you have ${player.bank}.")
            print()
            if blinds and count == 1:
                count += 1
                print("\nYou are the small blind. You bet $5.\n")
                input("Press Enter to continue.")
                bet = 5
            elif blinds and count == 2:
                count += 1
                print("\nYou are the big blind. You bet $10.\n")
                input("Press Enter to continue.")
                bet = 10
            elif minimum_bet == 0:
                count += 1
                checks.append(player)
                print("Would you like to check or bet?")
                print("\n1 - Check    2 - Bet\n")
                choice = input("Select one: ").lower()
                while choice == '' or choice not in [
                    2, '2', 'bet', 'b', 1, '1', 'check', 'c'
                ]:
                    choice = input("Select one: ")
                if choice in [1, '1', 'check', 'c']:
                    bet = 0
                else:
                    checks = [player]
                    print("How much would you like to bet?")
                    bet = input("$")
                    while not bet.isdigit() or int(bet) not in range(player.bank + 1):
                        if bet in [0, '0']:
                            # checks.append(player)
                            bet = minimum_bet
                            print(f"{player} checks.")
                        elif int(bet) > player.bank + 1:
                            print(f"You only have ${player.bank}.")
                            print("What would you like to bet?\n")
                            bet = input("$")
                        elif int(bet) < 10:
                            print("Minimum bet is $10.")
                            bet = input("$")
                    if bet != 0:
                        bet = int(bet)
                    print(f"You bet ${bet}.")
            else:
                print("What would you like to do?")
                print("\n0 - Fold    1 - Call    2 - Raise\n")
                choice = input("Select one: ").lower()
                while choice not in [
                    0, 1, 2, '0', '1', '2', 'f', 'c', 'r',
                    'fold', 'call', 'raise'
                ]:
                    choice = input("Select one: ").lower()
                if choice in [0, '0', 'fold', 'f']:
                    player.is_active = False
                    # bet = player.current_bet
                    active_bets = [
                        player.current_bet for player in players
                        if player.is_active
                    ]
                    betting_active = len(set(active_bets)) != 1
                    print(f"{player} folds.")
                elif choice in [1, '1', 'call', 'c']:
                    checks.append(player)
                    if player.current_bet != 5:
                        bet = min([player.bank, minimum_bet])
                        # print("Current bet is not 5.")
                        print(f"{player}'s' bet: ${bet}")
                    else:
                        bet = min([player.bank, minimum_bet])
                        print("Current bet is 5")
                        print(f"{player}'s' bet: ${bet}")
                    print(f"{player} calls ${bet}.")
                elif choice in [2, '2', 'raise', 'r']:
                    checks = [player]
                    print("How much would you like to raise?")
                    bet = input("$")
                    if bet in [0, '0']:
                        checks.append(player)
                        bet = 0
                        print(f"{player} checks.")
                    else:
                        while not bet.isdigit() or int(bet) not in range(
                            minimum_bet, player.bank + 1
                        ):
                            print(f"Please choose an amount between")
                            print(f" {minimum_bet} and {player.bank - minimum_bet * 2}.")
                            bet = input("$")
                    bet = int(bet) + int(minimum_bet)
                    print(f"Bet after raise: ${bet}")
                    if int(bet) not in range(minimum_bet, player.bank + 1):
                        if minimum_bet + bet > player.bank:
                            print(f"You only have {player.bank}.")
                            print("How much would you like to raise?")
                            bet = input("$")
                            while not bet.isdigit():
                                print(f"Please choose an amount between {minimum_bet} and {player.bank - minimum_bet}.")
                                bet = input("$")
                            # bet = int(bet)
                        elif minimum_bet + bet < minimum_bet:
                            print(f"Minimum bet: ${minimum_bet}.")
                            bet = input("$")
                            while not bet.isdigit():
                                print(f"Please choose an amount between {minimum_bet} and {player.bank - minimum_bet}.")
                                bet = input("$")
                        bet = int(bet)
                    print(f"Bet after raise: ${bet}")
                    minimum_bet = bet
        if player.is_active:
            print(f"{player}'s bet: ${bet}")
        player.current_bet = bet
        active_players = [
            player for player in players
            if player.is_active
        ]
        print("New current bets:")
        for person in players:
            print(f"{person}: ${person.current_bet}")
        if player.current_bet == 0:
            if player.is_active:
                checks.append(player)
                print(f"{player} checks.")
            if len(checks) == len(active_players):
                print("All players have checked.")
                betting_active = False
        # elif not player.is_active and player.current_bet != 5:
        #     betting_active = False
        else:
            checks = []
            print(f"You now have ${player.bank} - {player.current_bet}")
            if player.current_bet > minimum_bet:
                minimum_bet = player.current_bet
                print(f"Minimum bet is now ${minimum_bet}.")
        # input("Press Enter to continue.")
        if not player.is_active:
            while not player.is_active:
                player = next_player(player, players)
        else:
            player = next_player(player, active_players)
        # player = next_player(player, players)
        active_players = [
            player for player in players
            if player.is_active
        ]
        # active_players_only = [
        #     active_player for active_player in players
        #     if active_player.is_active
        # ]
        # active_bets = [
        #     active_player[1] for active_player in active_players
        #     if active_player[0].is_active
        # ]
        # active_bets = [
        #     player.current_bet for player in players
        #     if player.is_active
        # ]
        if len(active_players) == 1:
            betting_active = False
            print(f"Everyone has folded. {player} wins!")
            # kitty += player.current_bet
            # return [kitty, folded_players]
        # print(f"{player} bets ${player.current_bet} and has ${player.bank}. (line 346)")
        # print(f"Kitty is now ${kitty}.")
    kitty = sum([
        player.current_bet for player in players
    ])
    print(f"Betting is complete. Kitty is ${kitty}.")
    print(f"Active players: {active_players}")
    # print(f"Players who folded: {inactive_players}")
    input("Press Enter to continue.")
    for player in players:
        player.current_bet = 0
    return [kitty, folded_players]


def poker():
    """Automates a game of poker"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Welcome to the poker table. Please have a seat!\n")
    lauren = Player("Lauren")
    # nancy = Player("Nancy")
    drew = Player("Drew")
    # mom = Player("Mom")
    brandi = Player("Brandi")
    # john = Player("John")
    # players = [lauren, drew, brandi]
    players = []
    if not players:
        num_of_players = input("How many players?\n")
        while not num_of_players.isdigit() or int(num_of_players) < 2 or int(num_of_players) > 7:
            num_of_players = input("Please choose a number between 2 and 7.\n")
        num_of_players = int(num_of_players)
        for i in range(num_of_players):
            player_name = input(f"Player {i + 1}, what is your name?\n")
            while not player_name:
                player_name = input(f"Player {i + 1}: ")
            players.append(Player(player_name))
            print()
        print("Creating Players...\n")
    # active_players = [
    #     player for player in players
    #     if player.is_active
    # ]
    print("Each player gets $500 to start the game.\n")
    print("Players:")
    for player in players:
        player.bank += 500
        print(f"\t{player}")
    deck = Deck()
    deck.shuffle()
    dealer = random.choice(players)
    current_player = next_player(dealer, players)
    while not current_player.is_active:
        current_player = next_player(current_player, players)
    print(f"\n{dealer} will deal first.\n")
    print(f"{current_player} plays first.\n")
    for _ in range(2):
        for player in players:
            player.deal(deck.deal())
    for player in players:
        player.hand.sort(key=lambda card: card.value, reverse=True)
    pot = 0
    print("Let's play.\n")
    input("Press Enter to begin.\n")
    os.system('cls' if os.name == 'nt' else 'clear')
    blinds = True
    small_blind = next_player(dealer, players)
    big_blind = next_player(small_blind, players)
    board_cards = []
    betting_args = {
        "players": players,
        "current_player": current_player,
        "board_cards": board_cards,
        "blinds": blinds,
        "pot": pot,
        "big_blind": big_blind,
        # "small_blind": small_blind,
        "play": "On the table: "
    }
    print("Let's start the betting!")
    print(f"Betting will begin with {current_player}")
    kitty, folded_players = place_bets(betting_args)
    for player in folded_players:
        print(f"{player} folds.")
        player.is_active = False
    blinds = False
    pot += kitty
    current_player = next_player(current_player, players)
    while not current_player.is_active:
        current_player = next_player(current_player, players)
    print(f"${kitty} has been added to the pot.")
    print(f"Pot is now ${pot}.")
    big_blind = None
    small_blind = None
    for option in ["flop", "turn", "river"]:
        active_players_only = [
            player for player in players
            if player.is_active
        ]
        betting_args = {
            "players": active_players_only,
            "current_player": current_player,
            "board_cards": board_cards,
            "blinds": blinds,
            "pot": pot,
            "play": option,
            "big_blind": None
        }
        if len(active_players_only) == 1:
            break
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Betting is done\n\nPot: ${pot}\n")
        input(
            f"Let's take a look at the {option}. Press Enter to continue.\n"
        )
        deck.deal()  # Burn a card
        if option == "flop":
            board_cards.extend(deck.deal(3))
        else:
            board_cards.extend(deck.deal())
        print("On the table:")
        for card in board_cards:
            print(f"\t{card}")
        while not current_player.is_active:
            current_player = next_player(current_player, players)
        print(f"\nBetting will begin with {current_player}.")
        input("Press Enter to continue.")
        kitty, folded_players = place_bets(betting_args)
        for player in folded_players:
            print(f"{player} folds.")
            player.is_active = False
        pot += kitty
        print(f"${kitty} has been added to the pot.")
        print(f"Pot is now ${pot}.")
    # Afer all game play, check for winner:
    print("Now let's check for the winner!")
    input("Press Enter to continue.")
    for player in players:
        player.hand.extend(board_cards)
    winners = check_winners([
        player for player in players
        if player.is_active
    ])
    if len(winners) == 1:
        # print(f"winners: {winners}")
        winner = winners[0][0]
        winning_hand_name = winners[0][1]
        winning_cards = winners[0][2]
        other_cards = winners[0][3]
        print(f"Pot: ${pot}")
        print(f"{winner} wins with {winning_hand_name}:")
        winning_hand = winning_cards + other_cards
        print(winning_hand[:5])
        print(f"\n{winner} wins ${pot}!")
        winner.bank += pot
        print(f"{winner} now has ${winner.bank}")
    else:
        print(f"Winners: {winners}")
        # remainder = pot % len(winners)
        win = pot // len(winners)
        for option in winners:
            winner,
            winning_hand_name,
            winning_cards,
            other_cards = option
            print(f"Pot: ${pot}")
            print(f"{winner} wins with {winning_hand_name}:")
            winning_hand = winning_cards + other_cards
            print(winning_hand[:5])
            print(f"\n{winner} wins ${win}")
    for player in players:
        if player.bank:
            player.is_active = True


if __name__ == "__main__":
    poker()
