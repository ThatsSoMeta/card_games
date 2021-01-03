from schemas import Deck, Player, next_player
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


def check_winner(players):
    """Compares everyone's best hand and determines winner"""
    all_hands = {player: assess_hand(player) for player in players}
    # print(f"all_hands: {all_hands}")
    # print(f"hand_values: {hand_values}")
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
        winner = winners[0]
        print(f"{winner[0]} wins with {winner[1]}:")
        print(winner[2] + winner[3])
        return winner
    else:
        winners.sort(
            key=lambda winner: winner[2][0].value,
            reverse=True
        )
        # print(f"Winners:\n{winners}")
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
            print("We have a tie!!")
            print(f"values_list: {values_list}\nvalues_set: {values_set}")
            for winner in winners:
                player = winner[0]
                player.hand = winner[2] + winner[3]
                print(f"{player} wins!")
                for card in player.hand:
                    print(f"\t{card}")
        if winners[0][2][0].value > winners[1][2][0].value:
            winner = winners[0]
            print(f"{winner[0]} wins with {winner[1]}:")
            print(winner[2] + winner[3])
            return winner
        elif winners[0][3]:
            winners.sort(key=lambda winner: winner[3][0].value)
            # print(f"Multiple winners: {winners}")
            winner = None
            for i in range(len(winners[0][3])):
                if len(winners) == 1:
                    winner = winners[0]
                if not winner:
                    # print(
                    #     "\nLooks like we need to look a little deeper to find a winner.\n"
                    # )
                    # for option in winners:
                    #     print(f"{option[0]}'s remaining cards:")
                    #     print(option[3])
                    #     print()
                    first_player_card = winners[0][3][i]
                    second_player_card = winners[1][3][i]
                    if first_player_card.value > second_player_card.value:
                        # print(f"Popping out {winners[1]} because {second_player_card} is lower than {first_player_card}.")
                        winners.pop(1)
                    elif first_player_card.value < second_player_card.value:
                        # print(
                        #     f"Popping out {winners[0]} because {first_player_card} is lower than {second_player_card}.\n"
                        # )
                        winners.pop(0)
                    if winner:
                        print(f"{winner[0]} wins with {winner[1]}:")
                        print(winner[2] + winner[3])
                        # print(f"Winner: {winner}")
                        return winner
                else:
                    print(f"{winner[0]} wins with {winner[1]}:")
                    print(winner[2] + winner[3])
                    # print(f"Winner: {winner}")
                    return winner
        else:
            print(f"Multiple winners: {winners}")
            print("IT'S A DRAW!")
            for winner in winners:
                print(f"{winner[0]} wins with {winner[1]}:")
                print(winner[2] + winner[3])
                # print(f"Winner: {winner}")
            print(winners)
            return winners


def assess_hand(player):
    """Looks at player's cards and determines best poker hand"""
    hand = sorted(player.hand, key=lambda card: card.value, reverse=True)
    values = {}
    suits = {}
    names = {}
    possible_plays = {}
    for card in player.hand:
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
    # print(f"{player}: {possible_plays}")
    best_hand = list(max(possible_plays, key=lambda play: hand_values[play[0]]))
    print(f"{player}'s best hand: {best_hand[0]}")
    for card in best_hand[1]:
        print(f"\t{card}")
        player.discard(card)
    print()
    player.hand.sort(key=lambda card: card.value, reverse=True)
    return best_hand


def place_bets(args):
    players = args["players"]
    player = args["current_player"]
    blinds = args["blinds"]
    betting_active = True
    kitty = 0
    checks = []
    minimum_bet = 0
    count = 1
    while betting_active:
        active_players = [
            (player, f"${player.current_bet}") for player in players
            if player.is_active
        ]
        minimum_bet = max([int(player[1][1:]) for player in active_players])
        if player.is_active and player.bank:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"It is {player}'s turn.")
                input(f"Press Enter when {player} has the computer.\n")
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"It is {player}'s turn.")
                print(f"Players: {players}\nActive Players: {active_players}")
                print(f"Checked Players: {checks}\n")
                print(f"\n{player}'s current bet: ${player.current_bet}")
                print(f"Kitty: ${kitty}\nMinimum bet: ${minimum_bet}")
                print(f"\n{player}'s hand:")
                for card in player.hand:
                    print(f"\t{card}")
                bet = 0
                print(f"\n{player}, you have ${player.bank}.")
                if blinds and count == 1:
                    print("\nYou are the small blind. You bet $5.\n")
                    bet = 5
                    count += 1
                elif blinds and count == 2:
                    print("\nYou are the big blind. You bet $10.\n")
                    bet = 10
                    count += 1
                elif minimum_bet == 0:
                    print("Would you like to check or bet?")
                    print("\n1 - Check    2 - Bet\n")
                    choice = input("Select one: ").lower()
                    while choice == '':
                        print("Would you like to check or bet?")
                        choice = input("Select one: ")
                    if choice not in [2, '2', 'bet', 'b']:
                        bet = 0
                    else:
                        print("How much would you like to bet?\n")
                        bet = input("$")
                        while not bet.isdigit() or int(bet) not in range(
                            10, player.bank + 1
                        ):
                            if int(bet) > player.bank + 1:
                                print(f"You only have ${player.bank}.")
                                print("What would you like to bet?\n")
                                bet = input("$")
                            elif int(bet) < 10:
                                print("Minimum bet is $10.")
                                bet = input("$")
                        bet = int(bet)
                        print(f"You bet ${bet}.")
                else:
                    print("What would you like to do?")
                    print("\n0 - Fold    1 - Call    2 - Raise\n")
                    choice = input("Select one: ").lower()
                    if choice in [0, '0', 'fold', 'f']:
                        player.is_active = False
                        bet = 0
                        active_bets = [
                            player[1] for player in active_players
                            if player[0].is_active
                        ]
                        betting_active = len(set(active_bets)) != 1
                        print(f"{player} folds.")
                    elif choice not in [2, '2', 'raise', 'r']:
                        if player.current_bet != 5:
                            bet = min([player.bank, minimum_bet])
                            print("Current bet is not 5 (line 283)")
                            print(f"{player} bet: ${bet} (line 284)")
                        else:
                            bet = min([player.bank, minimum_bet])
                            print("Current bet is 5 (line 287")
                            print(f"{player} bet: ${bet} (line 288)")
                        print(f"{player} calls ${bet}. (line 289)")
                    else:
                        print("How much would you like to raise? (line 291)")
                        bet = input("$")
                        while not bet.isdigit() or int(bet) not in range(minimum_bet, player.bank + 1):
                            print(f"Please choose an amount between {minimum_bet} and {player.bank - minimum_bet * 2}.")
                            bet = input("$")
                        # if blinds
                        bet = int(bet) + minimum_bet
                        print(f"Bet after raise: ${bet} (line 298)")
                        if bet not in range(minimum_bet, player.bank + 1):
                            if minimum_bet + bet > player.bank:
                                print(f"You only have {player.bank}.")
                                print("How much would you like to raise?")
                                bet = input("$")
                                while not bet.isdigit():
                                    print(f"Please choose an amount between {minimum_bet} and {player.bank - minimum_bet}.")
                                    bet = input("$")
                                bet = int(bet)
                            elif minimum_bet + bet < minimum_bet:
                                print(f"Minimum bet: ${minimum_bet}.")
                                bet = input("$")
                                while not bet.isdigit():
                                    print(f"Please choose an amount between {minimum_bet} and {player.bank - minimum_bet}.")
                                    bet = input("$")
                        print(f"Bet after raise: ${bet}")
                        minimum_bet = bet
        print(f"{player}'s bet: ${bet} (line 311)")
        player.current_bet = bet
        active_players = [
            (player, f"${player.current_bet}") for player in players
            if player.is_active
        ]
        print("New current bets:")
        print(active_players)
        if player.current_bet == 0:
            if player.is_active:
                checks.append(player)
                print(f"{player} checks.")
            if len(checks) == len(active_players):
                print("All players have checked.")
                betting_active = False
        elif player.current_bet == next_player(player, players).current_bet:
            print(f"All players have called ${player.current_bet}")
            betting_active = False
        elif not player.is_active:
            betting_active = False
        else:
            checks = []
            print(f"You now have ${player.bank - player.current_bet}")
            if player.current_bet > minimum_bet:
                minimum_bet = player.current_bet
                print(f"Minimum bet is now ${minimum_bet}.")
        input("Press Enter to continue.")
        player = next_player(player, players)
    for player in players:
        kitty += player.current_bet
        print(f"{player} (line 346)")
    print(f"Betting is complete. Kitty is ${kitty}.")
    print(f"Active players: {active_players}")
    # print(f"Players who folded: {inactive_players}")
    for player in players:
        player.current_bet = 0
    print(f"Returning ${kitty}.")
    input("Press Enter to continue.")
    return kitty


def poker():
    """Automates a game of poker"""
    os.system('cls' if os.name == 'nt' else 'clear')
    lauren = Player("Lauren")
    drew = Player("Drew")
    mom = Player("Mom")
    players = [lauren, drew, mom]
    # num_of_players = input("How many players?\n")
    # while not num_of_players.isdigit() or int(num_of_players) < 2 or int(num_of_players) > 7:
    #     num_of_players = input("Please choose a number between 2 and 7.\n")
    # num_of_players = int(num_of_players)
    # for i in range(num_of_players):
    #     player_name = input(f"Player {i + 1}, what is your name?\n")
    #     while not player_name:
    #         player_name = input(f"Player {i + 1}, we need to call you something...\n")
    #     players.append(Player(player_name))
    # print("Creating Players...")
    print(f"Players: {players}")
    for player in players:
        player.bank += 500
    print("\nPlayers begin with $500.\n")
    # print("Let's try choosing some poker hands. Let me grab a deck.\n")
    deck = Deck()
    deck.shuffle()
    dealer = random.choice(players)
    current_player = next_player(dealer, players)
    print(f"{dealer} will deal first.\n")
    print(f"{current_player} plays first.\n")
    for _ in range(5):
        for player in players:
            player.deal(deck.deal())
    # code below can be used to pick what cards get dealt to hand
    # useful to test egde cases
    # while deck.deck:
    #     current_card = deck.deck[-1]
    #     for player in players:
    #         print(f"Possbile card:\n{deck.deck[-1]}\n")
    #         if len(player.hand) < 5 and current_card is deck.deck[-1]:
    #             print(f"{player}'s hand:\n{player.hand}")
    #             print(f"Do you want to add {deck.deck[-1]} to {player}'s hand?")
    #             if input("Y or N?\n").lower() in ['y', 'yes']:
    #                 choice = deck.deal()
    #                 print(f"Dealt card: {choice}")
    #                 player.deal(choice)
    #                 print(f"New current card:\n{current_card}")
    #                 # current_card = deck.deck[-1]
    #             else:
    #                 print(f"{player} does not pick up ")
    #             print(f"\n{player}'s new hand:\n{player.hand}\n")
    #             # input("Press Enter to continue.")
    #     if current_card is deck.deck[-1]:
    #         print("Card is discarded.")
    #         deck.deal()
    # The following lines can be used to hard-code hands to test scenarios
    # drew.deal(deck.deck[i] for i in [0, 13, 1, 14, 20])
    # lauren.deal(deck.deck[i + 13] for i in [0, 13, 1, 14, 20])
    # mom.deal(deck.deck[i] for i in [1, 5, 8, 15, 38])
    for player in players:
        player.hand.sort(key=lambda card: card.value, reverse=True)
    pot = 0
    print("Let's see who wins:\n")
    input("Press Enter to begin\n")
    os.system('cls' if os.name == 'nt' else 'clear')
    blinds = True
    betting_args = {
        "players": players,
        "current_player": current_player,
        "blinds": True
    }
    kitty = place_bets(betting_args)
    blinds = False
    pot += kitty
    print(f"${kitty} has been added to the pot.")
    print(f"Pot is now ${pot}.")
    check_winner(players)


if __name__ == "__main__":
    poker()
