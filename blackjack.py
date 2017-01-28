# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0


# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards =[]	# create Hand object

    def __str__(self):
        res = ""
        for card in self.cards:
            res+= (card.suit + card.rank +" ")
        return res	# return a string representation of a hand

    def add_card(self, card):
        self.cards.append(card)
        print self.cards# add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        value = 0
        A_count = 0
        for card in self.cards:             
            if A_count == 0 and card.rank != 'A':
                value += VALUES[card.rank]
            elif A_count == 0 and card.rank == 'A':
                value += 1
                A_count += 1  
            elif A_count ==1:
                if card.rank != 'A':
                    value += VALUES[card.rank]
                elif card.rank == 'A':
                    value += 11
                    A_count += 1
            elif A_count ==2:
                if card.rank == 'A':
                    value = value +1 -10
                    A_count += 1
                elif card.rank in ["T","J","Q","K"]:
                    value = value + VALUES[card.rank] - 10
                    A_count -= 1
                else:
                    value += VALUES[card.rank]
        return value
    def draw(self, canvas, pos):
        pass	# draw a hand on the canvas, use the draw method for cards 
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = [Card(SUITS[i], RANKS[j]) for i in range(len(SUITS)-1) for j in range(len(RANKS)-1)]	# create a Deck object

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)    # use random.shuffle()

    def deal_card(self): # deal a card object from the deck
        deck = self.deck
        card_dealt = deck.pop()
        return card_dealt
        
    
    def __str__(self):
        res = ""
        for card in self.deck:
            res += card.suit+card.rank+" "
        return res # return a string representing the deck
deck = Deck()
player_hand=Hand()
dealer_hand=Hand()

#define event handlers for buttons
def deal():
    global outcome, in_play
    # your code goes here
    deck.shuffle()
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    in_play = True

def hit():
    global outcome, in_play, player_hand
    # replace with your code below
    # if the hand is in play, hit the player
    # if busted, assign a message to outcome, update in_play and score
    if in_play == True:
        if player_hand.get_value <= 21:
            player_hand = Hand.add_card(Deck.deal_card())
        elif player_hand.get_value > 21:
            print "You have busted."
            in_play = False
       
def stand():
    global outcome, in_play, dealer_hand, player_hand
    # replace with your code below
   
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score
    if in_play == True:
        while dealer_hand.get_value < 17:
            dealer_hand.add_card(deck.deal_card())
    elif dealer_hand.get_value > 21:
        print "Deal has busted."
        in_play = False
    elif player_hand.get_value <= dealer_hand.get_value:
        outcome = "Dealer won."
        in_play = False
    else : 
        outcome = "Player won."
        in_play = False
    print outcome

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    
    card = Card("S", "A")
    card.draw(canvas, [300, 300])


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric