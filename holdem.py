from schemas import *
# import time


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
    all_hands = [[player, assess_hand(player)] for player in players]
    all_hands.sort(key=lambda hand: hand[1][1], reverse=True)
    print(all_hands)
    # for player in [drew, mom]:
    #     print(f"{player}: {assess_hand(player)}")
    print(f"{all_hands[0][0]} wins with a {all_hands[0][1][0]}.")
    return all_hands[0]


def assess_hand(player):
    values = {}
    suits = {}
    names = {}
    possible_plays = []
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
    # print(f"Values: {vals}")
    for suit, count in suits.items():
        if count == 5:
            # print(f"List(range(min - max)): {list(range(min(vals), max(vals) + 1))}")
            if vals == list(range(min(vals), max(vals) + 1)):
                if max(vals) == 14:
                    # print(f"You have a royal flush in {suit}!!!")
                    possible_plays.append("royal_flush")
                else:
                    # print(f"You have a straight flush in {suit}!")
                    possible_plays.append("straight_flush")
            else:
                # print(f"You have a flush in {suit}!")
                possible_plays.append("flush")
    for name, count in names.items():
        if count == 4:
            # print(f"You have four {name}s!")
            possible_plays.append("four_of_a_kind")
        elif count == 3:
            # print(f"You have three {name}s!")
            possible_plays.append("three_of_a_kind")
        elif count == 2:
            if "pair" in possible_plays:
                # print("You have two pairs!")
                possible_plays.append("two_pair")
            else:
                # print(f"You have a pair of {name}s!")
                possible_plays.append("pair")
    if len(vals) == 5 and vals == list(range(min(vals), max(vals) + 1)):
        # print("You have a straight!")
        possible_plays.append("straight")
    if "pair" in possible_plays and "three_of_a_kind" in possible_plays:
        # print("You have a full house!")
        possible_plays.append("full_house")
    possible_plays = [(play, hand_values[play]) for play in possible_plays]
    # print(possible_plays)
    # for play in possible_plays:
    #     print(f"{play}: {hand_values[play]}")
    best_hand = max(possible_plays, key=lambda play: play[1])
    # print(f"{player}'s best play is {best_hand}.")
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
print("\n\nI have made two hands. They are both empty. You need to choose 5 cards for each hand")
drew.hand = [deck[int(val)] for val in [0, 13, 1, 14, 27]]
mom.hand = [deck[int(val)] for val in [8, 9, 10, 11, 7]]
print(f"Drew:\n{drew.hand}\n\nMom:\n{mom.hand}\n")
# for index, hand in enumerate([hand1, hand2]):
    # while len(hand) < 5:
    #     for i, card in enumerate(deck):
    #         print(f"{i} - {card}", end=' ')
    #     choice = input(f"\n\nPlease pick a card for hand {index + 1}: ")
    #     while not choice.isdigit() or int(choice) not in range(len(deck)):
    #         choice = input("Please pick a different card...\n")
    #     chosen_card = deck[int(choice)]
    #     hand.append(chosen_card)
    #     print(f"Hand 1:\n{hand1}\n\nHand2:\n{hand2}\n")
    #     print("\n")

# time.sleep(3)
print("Let's check how many of each suit and value are in hand1:")
# print(f"{drew}:")
# assess_hand(drew)
# print(f"{mom}:")
# assess_hand(mom)
print("Let's see who wins:")
check_winner(players)
