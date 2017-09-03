'''
Brief:
    cblackjack_count.py - A script to count cards in a game of blackjack.
        Provides various statistics to alert the user to chances for various cards.

License:
    MIT License

Author(s):
    Charles Machalow
'''
import random

T = 10
J = 'JACK'
Q = 'QUEEN'
K = 'KING'
A = 'ACE'

FACES = [J, Q, K]

SPADES = 'SPADES'
CLUBS = 'CLUBS'
HEARTS = 'HEARTS'
DIAMONDS = 'DIAMONDS'

SUITS = [SPADES, CLUBS, HEARTS, DIAMONDS]

LINE = [2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, A]

try:
    raw_input         # py2 will be fine here
except:
    raw_input = input # py3 will get here

class CardCounter(dict):
    '''
    dict wrapper to add functions usefull to statistics
    '''
    def getNumberOfCardsWith10Value(self):
        '''
        Returns the number of cards remaining in the counter with a value of 10
        '''
        return self.get(J, 0) + self.get(Q, 0) + self.get(K, 0) + self.get(10, 0)

class Card(object):
    '''
    A playing card. It knows its value and suit.
    '''
    def __init__(self, value, suit):
        '''
        init for the Card. Cards have a value and a suit
        '''
        self.value = value
        self.suit = suit

    def __repr__(self):
        '''
        pretty, usefull repr for Card
        '''
        return '<Card with %s:%s>' % (self.value, self.suit)

class Deck(object):
    '''
    Deck of 52 playing cards
    '''
    def __init__(self):
        '''
        init for a standard deck of 52 cards
        '''
        self._cards = []
        for num in LINE:
            for suit in SUITS:
                self._cards.append(Card(num, suit))

        self._setupCounts()
        random.shuffle(self._cards) # shuffles in place

    def _setupCounts(self):
        '''
        Gets the counts dictionary ready
        '''
        self._counts = None # must set first.
        self._counts = self.getCounts()

    def draw(self):
        '''
        Draws a single card from the top of the deck and returns the card
        '''
        retCard = self._cards.pop()
        self._counts[retCard.value] -= 1 # keep track of counts
        return retCard

    def getNumberOfRemainingCards(self):
        '''
        Returns the number of cards left in the deck
        '''
        return len(self._cards)

    def getCounts(self, bustCache=False):
        '''
        Method to get a dictionary of card value to number remaining in the deck
        '''
        # check to use cache
        if bustCache:
            self._counts = None

        if self._counts is not None:
            return self._counts

        # generate counts
        counts = CardCounter()
        for card in self._cards:
            value = card.value
            if card.value in counts:
                counts[card.value] += 1
            else:
                counts[card.value] = 1

        return counts

    def getBlackjackChance(self):
        '''
        prints the percent chance of blackjack on the next 2 cards
        '''
        if self.getNumberOfRemainingCards() > 1:
            aceChance = self.getCounts().get(A, 0) / (self.getNumberOfRemainingCards() - 1)
            tenChance = self.getCounts().getNumberOfCardsWith10Value() / (self.getNumberOfRemainingCards() - 1)

            print ("Chance for blackjack: %.2f%%" % (aceChance * tenChance * 100))
        else:
            print ("No chance for blackjack")

    def getPercentChances(self):
        '''
        prints chances for what the next card will be
        '''
        if self.getNumberOfRemainingCards():
            for cardValue in LINE:
                numInDeck = float(self.getCounts().get(cardValue, 0))
                print ("%-12s : %0.02f%% (%d cards left)" % (cardValue, numInDeck / self.getNumberOfRemainingCards() * 100, numInDeck))

            tenVals = self.getCounts().getNumberOfCardsWith10Value()
            print ("%-12s : %0.02f%% (%d cards left)" % ("Any 10-Value", tenVals / self.getNumberOfRemainingCards() * 100, tenVals))

            self.getBlackjackChance()

            print ('%d cards left' % self.getNumberOfRemainingCards())
        else:
            print ('No cards remaining')

    def removeCardWithValue(self, value):
        '''
        Removes a card with the given value from the deck
        '''
        try:
            try:
                value = int(value)
            except:
                value = eval(value.upper()) # sketchy :)
        except:
            print ('-Warning- Had trouble getting the value of %s' % value)
            return

        delCardIdx = None
        for idx, itm in enumerate(self._cards):
            if itm.value == value:
                print ("Removed a %s" % value)
                self._counts[value] -= 1 # update counts
                removed = True # skip
                delCardIdx = idx
                break

        if delCardIdx is None:
            print ("-Warning- No card with value %s found!" % value)
        else:
            del self._cards[delCardIdx]

    def getBustChance(self, handValue):
        '''
        prints the chance for a bust based off the current hand value
        '''
        cardsThatWouldBust = 0.0
        maxOkCard = 21 - handValue
        for cardValue, cardCount in self.getCounts().items():
            if cardValue in FACES:
                cardValue = 10
            elif cardValue == A:
                cardValue = 1

            if cardValue > maxOkCard:
                cardsThatWouldBust += 1

        if self.getNumberOfRemainingCards() > 0:
            print ('Chance for bust: %.2f%%' % (cardsThatWouldBust / self.getNumberOfRemainingCards() * 100))
        else:
            print ("No remaining cards")

class Shoe(Deck):
    '''
    Shoe containing a certain number of decks
    '''
    def __init__(self, numDecks=6):
        '''
        init for the shoe. Will contain a certain number of decks shuffled together
        '''
        self._cards = []
        singleDeckCards = Deck()._cards
        for i in range(numDecks):
            self._cards.extend(singleDeckCards)

        self._setupCounts()
        random.shuffle(self._cards) # shuffle in place

if __name__ == '__main__':
    numDecks = int(raw_input("How many decks? "))
    shoe = Shoe(numDecks=numDecks)
    while True:
        print ('=' * 40)
        cards = raw_input("Give cards to remove from deck. 10/T=Ten, J=Jack, Q=Queen, K=King, A=Ace\n  Or you can give 'b' to get the percent chance for bust if you take the next card: ")
        if cards.lower() == 'b':
            currentHandValue = int(raw_input("Current hand value: "))
            shoe.getBustChance(currentHandValue)
            continue

        cards = cards.replace('10', 'T') # get into one-character mode
        if ',' in cards:
            cards = cards.split(',')
        for i in cards:
            shoe.removeCardWithValue(i)

        shoe.getPercentChances()