# implementation of card game - Memory
# By: Ahsanul Hadi
# Date: Nov 16, 2013 
# =====================================
import simplegui
import random

F_WIDTH = 800      # Frame Width
F_HEIGHT = 105     # Frame Height
C_WIDTH = (F_WIDTH / 16)  
C_HEIGHT = (F_HEIGHT - 1)
c_ln_color = "Lime" 
c_bg_color = "Green"
card_list = [] 
last_draw = [0,0]
counter = 0;
timer_interval, timer_count = 100, 0 

temp_key = [0, 0] 
# =====================================
# helper function to initialize globals
def new_game():
    global card_list, exposed, state, counter, exposed, timer_count, scroll_pos  
    state, counter, timer_count = 0, 0, 0 
    exposed = []
    scroll_pos = [C_HEIGHT] * 16 
    card_list = range(0, 8)  
    card_list += card_list    # OR,  card_list.extend(range(0, 8))
    random.shuffle(card_list)
    if len(exposed) == 0:  
        for i in range(0, 16): exposed.insert(i, False)
    if timer.is_running():
        timer.stop()       
     
# =====================================     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, counter, key, last_draw
    
    card_idx = (pos[0] // C_WIDTH)

    if state == 0: # State 0 = Start of the Game. 
        timer.start() 
        if not exposed[card_idx]:
            exposed[card_idx] = True
            scroll_up(card_idx)
            last_draw[0] = card_idx
            state = 1 # Now, A Card is exposed so state is changed.
    elif state == 1: # State 1 = Single Exposed Upaired Card. 
        if not exposed[card_idx]:
            exposed[card_idx] = True
            scroll_up(card_idx)
            last_draw[1] = card_idx
            state = 2 # Now, two card is exposed.
    else: # State 2 = End of a Turn. 3rd card flipped.
        if not exposed[card_idx]:
            exposed[card_idx] = True
            scroll_up(card_idx)
            if card_list[last_draw[0]] != card_list[last_draw[1]]:  # If NOT matched, fold previous two.
                exposed[last_draw[0]], exposed[last_draw[1]]  = False, False 
                temp_key[0], temp_key[1] = last_draw[0], last_draw[1]
                scroll_down()
            last_draw[0] = card_idx
            state = 1
            counter += 1
        
# =====================================                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global c_ln_color, c_bg_color, scrollup, scrolldown  
    temp = 0 
        
    if exposed.count(True) == 16: 
        temp = 10
        timer.stop()
        
    label1.set_text("Turns = " + str(counter))
    label2.set_text("Times Taken = " + format(timer_count))
    
    for idx in range(0, len(card_list)):
        if(exposed[idx] == False):
            c_bg_color, c_ln_color = "Black", "Lime"  
            canvas.draw_polygon([ (C_WIDTH * idx, 1), (C_WIDTH * idx, C_HEIGHT), \
                                 (C_WIDTH * (idx + 1), C_HEIGHT), (C_WIDTH * (idx + 1), 1) ], \
                                2, c_ln_color, c_bg_color);
            canvas.draw_text(str(card_list[idx]), [(C_WIDTH * idx + 12), (60 - temp)], 40, "White");
            c_bg_color, c_ln_color = "Green", "Lime"
            canvas.draw_polygon([ (C_WIDTH * idx, 1), (C_WIDTH * idx, (1 + scroll_pos[idx]) ), \
                                 (C_WIDTH * (idx + 1), (1 + scroll_pos[idx]) ), (C_WIDTH * (idx + 1), 1) ], \
                                2, c_ln_color, c_bg_color);            
            
        else:  # Scroll up and Show Digit 
            # Card background 
            c_bg_color, c_ln_color = "Black", "Lime"
            canvas.draw_polygon([ (C_WIDTH * idx, 1),     (C_WIDTH * idx, C_HEIGHT), \
                                 (C_WIDTH * (idx + 1), C_HEIGHT),    (C_WIDTH * (idx + 1), 1) ], \
                                2, c_ln_color, c_bg_color);         
            
            canvas.draw_text(str(card_list[idx]), [(C_WIDTH * idx + 12), (60 - temp)], 40, "White");
            c_bg_color, c_ln_color = "Green", "Lime"
            canvas.draw_polygon([ (C_WIDTH * idx, 1),      (C_WIDTH * idx, (1 + scroll_pos[idx]) ), \
                                 (C_WIDTH * (idx + 1), (1 + scroll_pos[idx])),    (C_WIDTH * (idx + 1), 1) ], \
                                2, c_ln_color, c_bg_color);      
            

    if exposed.count(True) == 16 and sum(scroll_pos) == 0:
        canvas.draw_polygon([ (1, 70), (1, F_HEIGHT), \
                             (F_WIDTH, F_HEIGHT), (F_WIDTH, 70) ], \
                              2, "Lime", "Black"); 
        message = "Congratulation :) You took " + str(counter) + " moves in " + format(timer_count)
        canvas.draw_text(message, [10, 92], 18, "Lime");

# =====================================                 
def format(t):    
    # From Stopwatch program. 
    global a,b,c,d,time_value
    
    a = (t // 600)    # Minute value
    # whole second = (count // 10) % 60, but we need to identify separately, so ..
    b = (t // 100) % 6 # 1st digit of Second's value. Mod 6 cause range needs to be [0-5]
    c = (t // 10) % 10 # 2nd digit of Second's value. For this, range is [0-9]
    d = t % 10  # Tenth of a second
    # string representation of the formatted time
    time_value = str(a) + ' min ' + str(b) + str(c) + '.' + str(d) + ' sec'
    return time_value        
# =====================================         
# define event handler for timer with 0.1 sec interval
def time_counter1():
    global timer_count
    timer_count += 1 

def scrollup_timecounter():
    scroll_pos[key] -= 1  
    if scroll_pos[key] <= 0 : scrollup_timer.stop()

def scrolldown_timecounter1():
    scroll_pos[temp_key[0]] += 1  
    if scroll_pos[temp_key[0]] >= 103 : scrolldown_timer1.stop()

def scrolldown_timecounter2():
    scroll_pos[temp_key[1]] += 1  
    if scroll_pos[temp_key[1]] >= 103 : scrolldown_timer2.stop() 

def scroll_up(card_idx):
    global key 
    key = card_idx
    scrollup_timer.start()

def scroll_down():   
    scrolldown_timer1.start()
    scrolldown_timer2.start()    
           
    
    
# =====================================
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", F_WIDTH, F_HEIGHT)
frame.add_button("Restart", new_game)
label1 = frame.add_label(" ")
label1.set_text("Turns = " + str(counter))
label2 = frame.add_label(" ")
label2.set_text("Times Taken = " + format(timer_count))

timer = simplegui.create_timer(timer_interval, time_counter1)
scrollup_timer = simplegui.create_timer(0.5, scrollup_timecounter)
scrolldown_timer1 = simplegui.create_timer(0.5, scrolldown_timecounter1)
scrolldown_timer2 = simplegui.create_timer(5, scrolldown_timecounter2)

# =====================================
# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric