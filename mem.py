# implementation of card game - Memory

import simplegui
import random

# helper function to initialize globals

def new_game():
    global state, card_index1, card_index2, count, exposed, deck, count
    state = 0
    card_index1 = None
    card_index2 = None
    count = 0
    exposed = [False] *16
    deck = generate_deck()

def generate_deck():
    cards = []
    for i in range(8):
        cards.append(random.randrange(0,8))
    deck = cards *2
    random.shuffle(deck)
    return deck


# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, card_index1, card_index2, count
    index = pos[0]/50
    if state == 0 and not exposed[index]:
        card_index1 = index
        exposed[index] = True
        state = 1
        count += 1
    elif state == 1 and not exposed[index]:
        card_index2 = index
        exposed[index] = True
        state = 2
        count += 1
    elif state == 2 and not exposed[index]:
        if deck[card_index1] != deck[card_index2]:
            exposed[card_index1] = False
            exposed[card_index2] = False
        card_index1 = index
        exposed[index] = True
        state = 1
        count += 1
    return count
                                     
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for i in range(16):
        if not exposed[i]:
            canvas.draw_polygon([[50*i, 90], [50*i, 10], [50*i+45, 10], [50*i+45, 90]], 5, 'Green', 'White')
        else: 
            canvas.draw_text(str(deck[i]),(50*i, 90), 100, 'Red')

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
#count = mouseclick(pos) 
frame.set_draw_handler(draw)
print count
label.set_text("Turns = "+ str(count))
# get things rolling
new_game()
frame.start()




# Always remember to review the grading rubric