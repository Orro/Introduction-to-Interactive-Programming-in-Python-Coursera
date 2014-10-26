# Blackjack
#
# Blackjack is a simple, popular card game that is played in many casinos.
#
# 14/09/2013

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
message = ""
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
        self.hand = []	# create Hand object

    def __str__(self):
        ans = ""
        for i in range(len(self.hand)):
            ans += str(self.hand[i])
        return ans	# return a string representation of a hand

    def add_card(self, card):
        self.hand.append(card)	# add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        hand_value = 0
        aces = False
        
        for i in range(len(self.hand)):
            hand_value += VALUES.get(self.hand[i].get_rank())	# compute the value of the hand, see Blackjack video
            if self.hand[i].get_rank() == 'A':
                aces = True
        if not aces:
            return hand_value
        else:
            if hand_value + 10 <= 21:
                return hand_value + 10
            else:
                return hand_value
                   
    def draw(self, canvas, pos):
        for i in range(len(self.hand)):
             
            self.hand[i].draw(canvas, pos)
            pos[0] += 100
            
# define deck class 
class Deck:
    def __init__(self):
        self.deck = [Card(x, y) for x in SUITS for y in RANKS] 	# create a Deck object
        
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self):
        d = self.deck.pop()
        return 	d # deal a card object from the deck
    
    def __str__(self):         
        ans = ""
        for i in range(len(self.deck)):
            ans += str(self.deck[i])
        return ans	# return a string representing the deck
        
#define event handlers for buttons
def deal():
    global outcome, in_play, deck, new_player, dealer, message, score
    
    new_player = Hand()
    dealer = Hand()
    deck = Deck()
    deck.shuffle()
    new_player.add_card(deck.deal_card())
    new_player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())

    if in_play:
        outcome = "Hit or Stand?"
        message = "You hit Deal button. You lose."
        score -= 1
    else:
        outcome = "Hit or Stand?"
        message = ""
        in_play = True
    
def hit():
    global message, outcome, score, in_play
    
    if new_player.get_value() <= 21:
        new_player.add_card(deck.deal_card())
        
        if new_player.get_value() > 21:
           score -= 1
           message = "You have busted"
           outcome = "New deal?" 
           in_play = False 
            
def stand():
    global message, outcome, in_play, score
    
    in_play = False
    if new_player.get_value() > 21:
        score -= 1
        message = "You have busted"
        outcome = "New deal?"
    else:
        while dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())
            print "dealer's hand", dealer, dealer.get_value()
    if dealer.get_value() > 21:
        score += 1
        message = "Dealer has busted"
        outcome = "New deal?"
    elif new_player.get_value() <= dealer.get_value():
        score -= 1
        message = "Dealer wins!"
        outcome = "New deal?"
    else:
        score += 1
        message = "You win!"
        outcome = "New deal?"
        
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text("Blackjack", (75, 75), 40, 'Blue')
    canvas.draw_text("Score: " + str(score), (300, 75), 30, 'Black')
    canvas.draw_text("Dealer", (75, 150), 30, 'Black')
    canvas.draw_text("Player", (75, 350 ), 30, 'Black')
    canvas.draw_text(message, (250, 150), 30, 'Black')
    canvas.draw_text(outcome, (250, 350), 30, 'Black')
    new_player.draw(canvas,[50, 400])
    dealer.draw(canvas,[50, 200])
    
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [86.5, 250], CARD_BACK_SIZE)
    
# initialization frame
frame = simplegui.create_frame("Blackjack", 700, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()
