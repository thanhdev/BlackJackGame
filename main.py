"""
Blackjack
The goal of the game is to beat the dealer by having a higher card total
without going over 21.
(This simulation excludes some additional actions like doubling down,
 splitting, and insurance to keep it simple.)
Rules:
    Card Values
        - 2 to 10 = Face Value
        - J, Q, K = 10
        - Ace = 1 or 11
    Definitions
        - Blackjack = an Ace and a card worth 10 points (21 total)
        - Hand = cards holding by a player
        - Hole = the dealer’s card that is face down
        - Hit = draw another card
        - Stand = take no more cards
        - Bust = going over 21
    How to play
        - The players place a bet by putting the desired number of chips.
        - The dealer deals two cards face up to the player.
        - The dealer receives one card face up and one face down.
        - The player can choose whether he/she want to hit or stand.
        - Then, the dealer can choose whether he/she want to hit or stand.
    Winning
        - If the player busts, he/she loses immediately
        - If the player's hand value is higher than the dealer's
        (or the dealer busts), he/she wins 1:1 his/her bet.
        - If the player's hand value is lower than the dealer's
        (or the dealer busts), he/she loses his/her bet.
        - If the player's hand value is equal to the dealer's
        (or the dealer busts), the player receives his bet back.
        - If the player gets Blackjack, he/she wins 3:2 his/her bet.
        - If the player and the dealer both get Blackjack,
        the player receives his bet back.
"""
import json

from deck import Deck
from player import Player

BLACKJACK = 21


def get_player_bet(player):
    """
    Function to handle player's bet
    Return a positive number that doesn't exceed player's chips
    """
    # Show player's current chips
    print('Your current chips: ', player.chips)
    # Loop until a valid bet amount is entered
    while True:
        # Check if a valid number is entered
        try:
            bet_amount = int(input('How much do you want to bet? '))
            # Check if a positive number is entered
            if bet_amount <= 0:
                print('Please enter a positive number.')
            # Check if the player has enough chips to place the bet
            elif bet_amount > player.chips:
                print('You don\'t have enough chips.')
            # Take chips from the player, return bet_amount
            else:
                player.chips -= bet_amount
                return bet_amount
        except ValueError:
            print('Please enter a valid number.')


def show_leaderboard():
    """
    Function to show The Leaderboard
    """
    # Load saved scores
    try:
        with open('blackjack.json') as f:
            scores = json.load(f)
    except FileNotFoundError:
        scores = []

    # Print Leaderboard
    print('LeaderBoard'.center(22, '-'))
    # Format each column 15 characters wide
    print('{:<15} {:<15}'.format('Name', 'Score'))
    # Print a dash line
    print('-' * 22)
    # Loop through list of score
    for name, score in scores:
        # Print formatted name and score
        print('{:<15} {:<15}'.format(name, score))
    # Print a dash line
    print('-' * 22)


def handle_continue(deck, player, dealer):
    """
    Function to handle if players want to continue playing or not
    If players choose not to continue, update the Leaderboard and show.
    """
    # Loop until a valid action is entered
    while True:
        action = input('Do you want to continue?\n'
                       '\t1. Yes\n'
                       '\t2. No\n')
        # Player chooses Yes
        if action == '1':
            # Refresh game state
            deck.refresh()
            player.refresh()
            dealer.refresh()
            break
        # Player chooses No
        elif action == '2':
            # Show Player's score
            print(f'Your final score: {player.chips}')
            # Save Player's score
            player.save_score()
            # Show the Leaderboard
            show_leaderboard()
            # Print goodbye message
            print(f'See you again {player.name}!')
            # Exit Program with no error
            exit(0)
        else:
            print('Please enter a valid action.')


def handle_player_turn(player, deck):
    """
    Function to handle the player's turn
    """
    # Loop until Player gets 21, stands, or busts
    while player.hand_value < BLACKJACK:
        # Input action from Player
        action = input('What is your action?\n'
                       '\t1. Hit\n'
                       '\t2. Stand\n')
        # If Player chooses to hit
        if action == '1':
            # Deal a card to Player
            player.hit(deck)
            # Show Player the card and new hand value
            print(f'You drawn {player.hand[-1]} ({player.hand_value})')
            # If Player busts
            if player.hand_value > BLACKJACK:
                # Show Player busts
                print('You bust.')
                # Break the loop
                break
        # If Player chooses to stand
        elif action == '2':
            # Break the loop
            break
        else:
            print('Please input valid action.')


def handle_dealer_turn(dealer, player, deck, bet_amount):
    """
    Function to handle the dealer's turn
    """
    # Show Dealer's hand
    print(f'Dealer cards: {dealer.hand_string} ({dealer.hand_value})')
    # If Dealer gets Blackjack
    if dealer.has_blackjack:
        # Show Dealer wins
        print('Dealer wins.')
    else:
        # Loop until Dealer has greater or equal value
        # than Player's or busts
        while dealer.hand_value < player.hand_value \
                and dealer.hand_value < BLACKJACK:
            # Deal a card to Dealer
            dealer.hit(deck)
            # Show Player the card and dealer's new hand value
            print(f'Dealer drawn {dealer.hand[-1]} '
                  f'({dealer.hand_value})')

        # If Dealer busts
        if dealer.hand_value > BLACKJACK:
            # Show Dealer busts
            print('Dealer busts.')
            # Show Player wins twice of bet amount
            print(f'You win {bet_amount * 2}!')
            # Add win amount to Player's chips
            player.chips += 2 * bet_amount
        else:
            # If Dealer has equal value to Player's
            if dealer.hand_value == player.hand_value:
                # Show it's a tie
                print('It\'s a tie.')
                # Add back bet amount to Player's chips
                player.chips += bet_amount
            # Dealer has greater value than Player's
            else:
                # Show Dealer wins
                print('Dealer wins.')


def main():
    """
    Main function
    """
    # Print welcome message
    print('Welcome to the Blackjack Game')
    # Show the leaderboard of top 10 players
    show_leaderboard()
    # Input name from Player
    name = input('Enter your name (maximum 10 characters):\n')[:10]
    # Initialize a Player with name and 1000 chips
    player = Player(name)
    # Initialize a Dealer
    dealer = Player('Dealer')
    # Initialize a deck with 52 shuffled cards
    deck = Deck()

    # Loop until Player has no more chips to play
    while player.chips:
        # Input bet amount from Player
        bet_amount = get_player_bet(player)

        # Deal 2 cards to each player
        for _ in range(2):
            dealer.hit(deck)
            player.hit(deck)

        # Show the first card of Dealer
        print('Dealer\'s first card: ', dealer.hand[0])

        # Show both cards of Player
        print(f'Your cards: {player.hand_string} ({player.hand_value})')

        # If Player does not get Blackjack
        if not player.has_blackjack:
            # Call function to handle Player's turn
            handle_player_turn(player, deck)

            # If player busts
            if player.hand_value > BLACKJACK:
                # Show Dealer wins
                print('Dealer wins.')
            # Player does not bust
            else:
                # Call function to handle Dealer's turn
                handle_dealer_turn(dealer, player, deck, bet_amount)
        # Player gets Blackjack
        else:
            # Show Dealer's hand
            print(f'Dealer cards: {dealer.hand_string} ({dealer.hand_value})')

            # If Dealer also gets Blackjack
            if dealer.has_blackjack:
                # Print tie game
                print('Both have Blackjack. It\'t a Tie.')
            # Dealer does not get Blackjack
            else:
                # Player wins 2.5 times of bet amount with Blackjack
                win_amount = int(bet_amount * 2.5)
                print(f'You win {win_amount} chips with Blackjack!')
                # Add win amount to Player's chips
                player.chips += win_amount

        # If player still has chips to play
        if player.chips:
            # Call function to handle continue
            handle_continue(deck, player, dealer)
    else:
        # Show game over message
        print('Game over! Good luck next time!')


if __name__ == '__main__':
    main()
