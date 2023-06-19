"""
Module to handle Card and Deck logics
"""
from random import shuffle

# Card ranks
RANKS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
# Card suits
SUITS = ['♠', '♥', '♣', '♦']


class Card(object):
    def __init__(self, rank, suit):
        """
        Initialize a card with rank and suit
        """
        self.rank = rank
        self.suit = suit

    def __str__(self):
        """
        Stringify a card
        :return:
        """
        return f'{str(self.rank)}{self.suit}'


class Deck(object):
    def __init__(self):
        """
        Initialize a deck with 52 shuffled cards
        """
        self.refresh()

    def refresh(self):
        """
        Initialize or refresh a deck with 52 shuffled cards
        """
        self.cards = []
        for rank in RANKS:
            for suit in SUITS:
                self.cards.append(Card(rank, suit))
        shuffle(self.cards)

    def draw(self):
        """
        Draw a card from the deck
        """
        return self.cards.pop()
