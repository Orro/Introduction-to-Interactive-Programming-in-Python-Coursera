# Implementation of card game - Memory
#
# In Memory, a turn (or a move) consists of the player flipping over two cards. If they match, 
# the player leaves them face up. If they don't match, the player flips the cards back face down. 
# The goal of Memory is to end up with all of the cards flipped face up in the minimum number of turns
#
# 07/09/2013

import simplegui
import random

# helper function to initialize globals
def new_game():
    global deck, counter, exposed, index, paired, state, pos
    pos = 10
    deck1 = range(8)
    deck2 = range(8)
    deck = deck1 + deck2
    random.shuffle(deck)
    counter = 0
    state = 0
    label.set_text('Turns = ' + str(counter))
    exposed = [False, False, False, False, False, False, False, False,
               False, False, False, False, False, False, False, False]
    index = []
    paired = False
    
# define event handlers
def mouseclick(pos):
    # add game state logic here
    
    global state, exposed, index, paired, counter
    
    if state == 0:
        state = 1 
        exposed[pos[0]/50] = True 
        index.append(pos[0]/50) 
           
    elif state == 1:
        if not exposed[pos[0]/50]:
            state = 2            
            exposed[pos[0]/50] = True 
            index.append(pos[0]/50)
            counter += 1
            label.set_text('Turns = ' + str(counter))
            if deck[index[0]] == deck[pos[0]/50]:
                exposed[index[0]] = True
                paired = True
                
    else:
        if not exposed[pos[0]/50]:
            state = 1
            if not paired: 
                exposed[index[0]] = False
                exposed[index[1]] = False        
            exposed[pos[0]/50] = True        
            index = []
            index.append(pos[0]/50)
            paired = False
       
# cards are logically 50x100 pixels in size    
def draw(canvas):  
    global pos

    for j in range(len(exposed)):
        if not exposed[j]:
            canvas.draw_polygon([(j * 50, 0), (j * 50 + 50, 0), (j * 50 + 50, 100), 
                                 (j * 50, 100)], 1, 'Green', 'Green')
            canvas.draw_line([j * 50, 0], [j * 50, 100], 1, "Red")            
        else:
            canvas.draw_text(str(deck[j]), [(j) * 50 + pos, 70], 60, "White") 
  
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

# Always remember to review the grading rubric
