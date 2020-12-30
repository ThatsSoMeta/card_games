from schemas import *

print("Creating Player...")
drew = Player('Drew')
print(f"Say hello to our new player {drew}.")
print(f"Drew currently has ${drew.bank}, but we are about to give him $500.")
drew.bank += 500
print("Let's see if it worked!")
print(f"Drew's new bank: ${drew.bank}.")
print("Let's make a pot. We will start at $0.")
pot = 0
print(f"Pot: ${pot}")
while drew.bank:
    bet_attempt = input(f"How much should {drew} bet?\n$")
    pot += drew.bid(bet_attempt)
    print(f"Pot: ${pot}")
    print(f"Drew's new bank: ${drew.bank}.")
