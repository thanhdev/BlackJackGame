"""
Module to handle Player logics
"""
import json

BLACKJACK = 21


class Player:
    def __init__(self, name):
        """
        Initialize a Player
        """
        # Set name with entered input
        self.name = name
        # Set initial chips to 1000
        self.chips = 1000
        # Set player's hand to an empty list
        self.hand = []
        # Set hand's value to zero
        self.hand_value = 0

    def refresh(self):
        """
        Refresh player's hand to empty, hand's value to zero
        """
        self.hand = []
        self.hand_value = 0

    def hit(self, deck):
        """
        Draw a card from the deck
        Add Card's value to Player's hand value
        An ace can be count as 11 or 1, depends on which is better.
        """
        card = deck.draw()
        self.hand.append(card)
        if card.rank == 'A':
            if self.hand_value + 11 <= BLACKJACK:
                self.hand_value += 11
            else:
                self.hand_value += 1
        else:
            if card.rank in ['J', 'Q', 'K']:
                self.hand_value += 10
            else:
                self.hand_value += card.rank

    def save_score(self):
        """
        Function to save Player's score to The Leaderboard (if player's score
        is high enough to take place in The Leaderboard)
        """
        # Load saved scores
        try:
            with open('blackjack.json') as f:
                scores = json.load(f)
        except FileNotFoundError:
            scores = []

        # Add new score, sort by score descending
        scores.append((self.name, self.chips))
        scores.sort(key=lambda x: x[1], reverse=True)

        # Save top 10 score list
        with open('blackjack.json', 'w') as f:
            json.dump(scores[:10], f)

    @property
    def hand_string(self):
        """
        Stringify Player's hand
        """
        return ' '.join(str(c) for c in self.hand)

    @property
    def has_blackjack(self):
        """
        Player has Blackjack when Player has two cards with total value is 21
        """
        return len(self.hand) == 2 and self.hand_value == BLACKJACK
