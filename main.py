import requests
import os

def calculate(hand):
    value, aces = 0, 0
    for card in hand:
        value += int(card['value']) if card['value'].isdigit() else 10
        if card['value'] == 'Ace':
            aces += 1
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

def display(hand, title):
    cards = [f"{card['value']} of {card['suit']}" for card in hand]
    print(f"{title}: " + ", ".join(cards))

def shuffle_deck():
    response = requests.get("https://www.deckofcardsapi.com/api/deck/new/shuffle/?deck_count=6")
    return response.json()['deck_id'] if response.status_code == 200 else None

def draw_cards(deck_id, count):
    response = requests.get(f"https://www.deckofcardsapi.com/api/deck/{deck_id}/draw/?count={count}")
    return response.json()['cards'] if response.status_code == 200 else []

def play_game():
    os.system("clear")
    print("Welcome to Blackjack")

    deck_id = shuffle_deck()
    if not deck_id:
        print("Game servers are not available yet.")
        return

    player = draw_cards(deck_id, 2)
    dealer = draw_cards(deck_id, 2)

    while True:
        display(player, "Player's cards")
        player_value = calculate(player)
        if player_value > 21:
            print("You bust! Dealer wins.")
            return
        
        action = input("Hit or Stand? (h/s): ").strip().lower()
        if action == 'h':
            player.append(draw_cards(deck_id, 1)[0])
        elif action == 's':
            break

    display(dealer, "Dealer's cards")
    dealer_value = calculate(dealer)
    while dealer_value < 17:
        dealer.append(draw_cards(deck_id, 1)[0])
        dealer_value = calculate(dealer)

    display(dealer, "Dealer's cards")
    print("Dealer's hand value:", dealer_value)

    if dealer_value > 21:
        print("Dealer busts! You win!")
    elif player_value > dealer_value:
        print("You win!")
    elif player_value < dealer_value:
        print("Dealer wins!")
    else:
        print("It's a tie!")

def main():
    first_time = True
    while True:
        if first_time:
            decision = input("Do you wish to start a game? (y: yes, n: no): ").lower()
            if decision == "n":
                break
            elif decision != "y":
                print("Invalid option. Please enter 'y' or 'n'.")
                continue

        play_game()
        first_time = False
        if input("Do you want to play again? (y/n): ").strip().lower() != 'y':
            break

if __name__ == "__main__":
    main()
