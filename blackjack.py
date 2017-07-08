# Mini-project #6 - Blackjack
# By: Ahsanul Hadi 
# Date: Nov 27, 2013 

# =======================================
import simplegui
import random

# =======================================
C_WIDTH = 800
C_HEIGHT = 680
# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
left_pos = 25   # for print alignment. 
in_play = False # Flag: Whether the game is running.
outcome = ""    # Hit/stand print msg
result = ""     # game result msg
score = 0 
player_name = 'Player'  
dealer_name = 'Dealer'
exposed = False   # Flag: Maintain Dealer's Hole Card

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

rules = ["(1) Card Values: Numbered Card has value equal to Number. Face card (K, Q, J) has value 10. ACE has value 1 or 11 (players choice).", \
         "(2) Highest hand with value 21 or < 21, WINS. If hand value becomes > 21, then BUSTED.", \
         "(3) Player may ask the dealer to repeatedly HIT to deal him another card. If, at any point, the value of players hand exceeds 21, ", \
         "     then the player is BUSTED and loses game.", \
         "(4) Dealer will always Hit if he has hand value < 17 and always STAND, if value >= 17", \
         "(5) At any point prior to busting, the player may STAND and the dealer will then hit his hand until the value of his hand is 17 or more." ]
# =======================================
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

# =======================================        
# define hand class
class Hand:
    # def __init__(self):
    def __init__(self, name):  
        self.hand = []      # Cards in the hand
        self.counter = 0    # To increase X pos for respective players.
        self.name = name   # It is added to keep a track of the player and draw accordingly.

    def __str__(self):      # return a string representation of a hand
        cards_in_hand ="" 
        for card in list(self.hand): 
            cards_in_hand += str(card) + " "
            
        if len(self.hand) == 0: 
            return "Hand doesn't have any card."
        else: 
            return "Hand contains " + cards_in_hand	
    
    def add_card(self, card): # add a card object to a hand
        self.hand.append(card)	

    def get_value(self):  # compute the value of the hand, see Blackjack video
        no_of_Ace, hand_value = 0, 0 
        
        for card in list(self.hand):
            hand_value += VALUES.get(card.get_rank())            
            if card.get_rank() == 'A': 
                no_of_Ace += 1  # Count of Number of Ace. True/False would do too.
                
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust   
        if (no_of_Ace > 0) and (hand_value + 10 <= 21): 
            return hand_value + 10    # Never count two aces as 11, so always considering only one Ace.
        else:  
            return hand_value # other two cases (no Ace) OR (having Ace but hand value crossing limit)
                
    def draw(self, canvas, pos):  # draw a hand on the canvas, use the draw method for cards 
        self.counter = 0  # To increase X pos for respective players.
        pad = 10  # Gap between two cards.
        y = pos[1]   # Y pos is fixed for all players. 
        
        for card in list(self.hand):
            if self.counter == 0:   # For first card.
                x = pos[0] + (CARD_SIZE[0] * self.counter)  # No pad required for first card 
            else:
                x = pos[0] + ( (CARD_SIZE[0] + pad) * self.counter )  # Padding added.               
            
            if self.name == dealer_name and self.counter == 0 and not exposed:
                canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_BACK_SIZE)
            else:
                card.draw(canvas, [x, y])
            self.counter += 1
            
# =======================================        
# define deck class 
class Deck:
    def __init__(self):  # create a Deck object
        self.deck = []   # it's a list of Card Objetcs.  ['SA', 'C2', 'DK' .. ]
        for suit in list(SUITS): 
             map(lambda rank: self.deck.append(Card(str(suit), str(rank))),RANKS)    
        
    def shuffle(self): # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self): # deal a card object from the deck
        return self.deck.pop(len(self.deck)-1)
    
    def __str__(self):
        cards_in_deck ="" 
        for card in list(self.deck): cards_in_deck += str(card) + " "
        return "Deck contains " + cards_in_deck	        
        
# =======================================
#define event handlers for buttons
def deal():
    global outcome, in_play, result, score, first_time, exposed  # Variables 
    global deck, player, dealer # Objects

    if in_play:  # Deal button clicked in the middle of the game.
        result = "You give up! Dealer wins."
        score -= 1
        in_play = False 
    else:        # Normal: Deal button clicked after a game ends.
        in_play = True
        result = ""
        exposed = False
        
        deck = Deck()  # Create new 'deck' which is object of class 'Deck'
        deck.shuffle()  # Shuffle that deck    
        player = Hand(player_name) # Create 'player' which is object of class 'Hand'
        dealer = Hand(dealer_name) # Create 'player' which is object of class 'Hand'   
           
        player.add_card(deck.deal_card())  # Add cards to player/dealer hands. 
        player.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())          
                
# =======================================
def hit():
    global score, outcome, in_play, result  # Variables 
        
    # if the hand is in play, hit the player
    if in_play and (player.get_value() <= 21):
        player.add_card(deck.deal_card())  # Deal another card to player
            
    # if busted, assign a message to outcome, update in_play and score        
    if in_play and player.get_value() > 21:
        in_play = False
        result = "Player is Busted! Dealer Wins. "
        score -= 1 # Dealer Wins.
            
# =======================================       
def stand():
    global score, outcome, in_play, result, exposed  # Variables       
    exposed = True
    
    if in_play:   # if hand is in play 
        while dealer.get_value() < 17:    # Repeatedly Deal card till dealer's hand value is < 17 
            dealer.add_card(deck.deal_card())
            
        if dealer.get_value() > 21:  # If Dealer get Busted then assign a message and update score
            result = "Dealer is Busted! Player wins. "
            score += 1              
        else:  # Now Dealer's hand value >= 17 but <=21, So compare hands with Player
            print "Result: "
            print "Dealer's " + str(dealer) + ", Values = " + str(dealer.get_value())
            print "Player's " + str(player) + ", Values = " + str(player.get_value())
            print 
            if dealer.get_value() == player.get_value(): 
                result = "It's a Tie !!"
            elif dealer.get_value() > player.get_value(): 
                result = "Dealer wins."
                score -= 1
            else:
                result = "Player wins. "
                score += 1
        in_play = False # This round has finished, so update in_play        
    
# =======================================
# draw handler    
def draw(canvas):
    global score, outcome
    # -- Draw Title/ Header ----------------------------
    canvas.draw_line((0, 5), (C_WIDTH, 5), 3, 'Black')  # Top Line
    canvas.draw_text("Blackjack", [left_pos, 57], 50, "Yellow") # Title: Game
    canvas.draw_text("Score: " + str(score), [640, 53], 40, "Black") # Score
    canvas.draw_line((0, 85), (C_WIDTH, 85), 3, 'Black')    
    # -- Draw Dealer Cards ------------------------------
    canvas.draw_text("Dealer", [left_pos, 130], 35, "Black") # Title: Dealer
    dealer.draw(canvas, [left_pos + 3, 150])  # Draw Dealers CARD
    # -- Draw Player Cards ------------------------------
    canvas.draw_text("Player", [left_pos, 290], 35, "Black") # Title: Player  
    player.draw(canvas, [left_pos + 3, 320]) # Draw Players CARD  
    # -- Draw Outputs Messages ------------------------------
    canvas.draw_line((0, 450), (C_WIDTH, 450), 1, 'Black')
    if in_play: outcome = "Hit or Stand?"
    else: outcome = "New Deal?"        
    canvas.draw_text(outcome, [left_pos, 485], 28, "Black") 
    canvas.draw_text(result, [left_pos + 200, 485], 28, "White") 
    # -- Draw Rules ------------------------------
    canvas.draw_line((0, 507), (C_WIDTH, 507), 1, 'Black')
    canvas.draw_text("Rules: ", [left_pos, 535], 25, "Black")
    i = 0   # to increase line gap 
    for lines in list(rules): 
        canvas.draw_text(lines, [left_pos, 560 + i], 14, "Black")
        i += 20 
    
# =======================================
# initialization frame
frame = simplegui.create_frame("Blackjack", C_WIDTH, C_HEIGHT)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# =======================================
# Initialize Dec and Hands. 
# deck = Deck()  # Create new 'deck' which is object of class 'Deck'
# player = Hand(player_name) # Create 'player' which is object of class 'Hand'
# dealer = Hand(dealer_name) # Create 'player' which is object of class 'Hand'
# get things rolling
deal()
frame.start()


# remember to review the gradic rubric