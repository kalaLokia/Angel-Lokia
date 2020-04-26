import random

class DeckOfCards():
    '''
    All talks here is about cards
    '''
    cards = {'A':11,'K':10,'Q':10,'J':10,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10}
    
    def __init__(self):
        '''
        Initialize deck of cards
        '''
        self.deck = list(self.cards.keys())*4

    def shuffle(self):
        '''
        Simply shuffles the deck of cards
        '''
        return random.shuffle(self.deck)

    def handValue(self, hand):
        '''
        Calculates and returns the hand value, expecting a string value to be feeded.
        '''
        result = 0

        for element in hand:
            result = result + self.cards[element]
       
        for _ in range(hand.count('A')):
            if result > 21:
                result -= 10

        return result

    def hit(self):
        '''
        Pop out and returns the last card in the deck
        '''
        return self.deck.pop()
    
    def initiate(self):
        '''
        Pop out 2 cards from the deck and return as a tuple
        '''
        return (self.deck.pop(), self.deck.pop() )