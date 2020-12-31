from schemas import Deck, Player


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
    all_hands = {player: assess_hand(player) for player in players}
    best_hand_value = max([hand_values[play[0]] for play in all_hands.values()])
    for hand, value in hand_values.items():
        if value == best_hand_value:
            best_hand = hand
    winners = [
        (player, hand) for player, hand in all_hands.items()
        if hand[0] == best_hand
    ]
    if len(winners) == 1:
        print(f"Winner is: {winners[0]}")
        return winners[0]
    else:
        high_values = [
            winner[1][1] for winner in winners
        ]
        narrowed = [
            winner for winner in winners
            if winner[1][1] == max(high_values)
        ]
        if len(narrowed) == 1:
            print(f"Winner is: {narrowed[0]}")
            return narrowed[0]
        else:
            print(f"There is a tie: {narrowed}")


    # print(f"{all_hands[0][0]} wins with a {all_hands[0][1]}.")
    # return all_hands[0]


def assess_hand(player):
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
    for _, count in suits.items():
        if count == 5:
            if vals == list(range(min(vals), max(vals) + 1)):
                if max(vals) == 14:
                    possible_plays["royal_flush"] = max(vals)
                else:
                    possible_plays["straight_flush"] = max(vals)
            else:
                possible_plays["flush"] = max(vals)
    for value, count in values.items():
        if count == 4:
            possible_plays["four_of_a_kind"] = value
        elif count == 3:
            possible_plays["three_of_a_kind"] = value
        elif count == 2:
            try:
                possible_plays["pair"].append(value)
            except KeyError:
                possible_plays["pair"] = [value]
            if len(possible_plays["pair"]) == 2:
                possible_plays["two_pair"] = possible_plays["pair"]
    if len(vals) == 5 and vals == list(range(min(vals), max(vals) + 1)):
        possible_plays["straight"] = max(vals)
    if "pair" in possible_plays and "three_of_a_kind" in possible_plays:
        possible_plays["full_house"] = [
            possible_plays["three_of_a_kind"],
            possible_plays["pair"][0]
        ]
    possible_plays["high_card"] = max(card.value for card in player.hand)
    possible_plays = [play for play in possible_plays.items()]
    print(f"{player}: {possible_plays}")
    best_hand = max(possible_plays, key=lambda play: hand_values[play[0]])
    print(f"{player}'s best hand:")
    print(f"{best_hand} with a value of {hand_values[best_hand[0]]}")
    return best_hand


# player = Player(input("Player name:\n"))
print("Creating Players...")
drew = Player('Drew')
mom = Player('Mom')
players = [drew, mom]
for player in players:
    print(f"Say hello to our new player {player}.")
    print(f"{player} currently has ${player.bank}, but we are about to give them $500.")
    player.bank += 500
    print("Let's see if it worked!")
    print(f"{player}'s new bank: ${player.bank}.")
print("Let's make a pot. We will start at $0.")
pot = 0
print(f"Pot: ${pot}")
# bet_attempt = input(f"How much should {player} bet?\n$")
# pot += player.bid(bet_attempt)
# print(f"Pot: ${pot}")
# print(f"{player}'s new bank: ${player.bank}.")
print("Let's try choosing some poker hands. Let me grab a deck.\n")
deck = Deck()
deck = deck.deck
# print("\n\nI have made two hands. They are both empty. You need to choose 5 cards for each hand")
# drew.hand = [deck[int(val)] for val in [0, 13, 1, 14, 30]]
# mom.hand = [deck[int(val)] for val in [8, 9, 2, 11, 7]]
drew.hand = []
mom.hand = []
print(f"Drew:\n{drew.hand}\n\nMom:\n{mom.hand}\n")
for player in players:
    hand = player.hand
    while len(hand) < 5:
        for i, card in enumerate(deck):
            print(f"{i} - {card}", end=' ')
        choice = input(f"\n\nPlease pick a card for {player}'s hand: ")
        while not choice.isdigit() or int(choice) not in range(len(deck)):
            choice = input("Please pick a different card...\n")
        chosen_card = deck[int(choice)]
        hand.append(deck.pop(deck.index(chosen_card)))
        print(f"{player}: {hand}")
        print("\n")
print("Let's see who wins:")
check_winner(players)
