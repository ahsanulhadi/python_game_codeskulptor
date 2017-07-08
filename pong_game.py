# Implementation of classic arcade game Pong

# By: Ahsanul Hadi
# Date: Nov 9, 2013 
# Original pong game info: http://en.wikipedia.org/wiki/Pong
# ===================================
import simplegui
import random 

# ===================================
# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
PAD_COLOR = "White"
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

paddle1_init_pos = [HALF_PAD_WIDTH, ((HEIGHT/ 2) - HALF_PAD_HEIGHT)]   # Left Paddle position at center 
paddle2_init_pos = [(WIDTH - HALF_PAD_WIDTH), ((HEIGHT/ 2) - HALF_PAD_HEIGHT)]  # Right Paddle position at center
paddle1_pos = list(paddle1_init_pos)
paddle2_pos = list(paddle2_init_pos) 
paddle1_vel = 0
paddle2_vel = 0
acc = 7  # Accelerator increase
# initialize ball_pos and ball_vel for new bal in middle of table
center_pos = [WIDTH / 2, HEIGHT / 2]
ball_pos = list(center_pos)
ball_vel = [0.0, 0.0]  # VELOCITY i.e. 2D Vector 
# Players Score Elements: [ Point, Position [x,y], Font size, Font color ] 
score_color = "Red"
score_p1 = [0, [(WIDTH /4) * 1, 50], 50, score_color ]   # (*1) is not required, alignment :P               
score_p2 = [0, [(WIDTH /4) * 3, 50], 50, score_color ]
total_score = 10
# Sound effects.
# Thanks to Xavier Rovira for sharing the code on Loading sound, in the forum. 
hit_sound = simplegui.load_sound('http://www.allmusiclibrary.com/free_sound_effects/simple_beep.mp3')
hit_sound.set_volume(1)
miss_sound = simplegui.load_sound('http://s1download-universal-soundbank.com/mp3/sounds/18541.mp3')
miss_sound.set_volume(0.5)

time = 0  # Timer count
countdown = 4 # Countdown message 
banner_text = ("Player 1", "Player 2")
result_text = [" "," "]   

# ===================================
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists    
    ball_pos = list(center_pos)     # Set to Center 
    x = random.randrange(120, 240)  # Horizontal Velocity | Pixels per second
    y = random.randrange(60, 180)   # Vertical Velocity | Pixels per second
    if direction:    # Is TRUE i.e RIGHT 
        ball_vel = [x/60, -y/60]    # refresh rate: 60 frame per second
    else:            # Is FALSE i.e LEFT 
        ball_vel = [-x/60, -y/60]   
     
# -----------------------------------
# Starts a new game. 
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel      
    paddle1_pos = list(paddle1_init_pos)   # set in center .. 
    paddle2_pos = list(paddle2_init_pos) 
    paddle1_vel, paddle2_vel = 0, 0
    
    if score_p1[0] > score_p2[0]:   # If Player 1 won last time, then spawn ball to LEFT
        spawn_ball(LEFT)
    elif score_p1[0] < score_p2[0]: # If Player 2 won last time, then spawn ball to RIGHT   
        spawn_ball(RIGHT) 
    else:                           #  For new game, spawn at random side
        spawn_ball(random.choice([RIGHT,LEFT]))  
    
    score_p1[0], score_p2[0] = 0, 0         # Reset Score, cause countdown will start
    
# -----------------------------------
# Every time ball hits the paddle, increase velocity by 10% .
def increase_vel():
    # No need to declare Global, as we will just change Elements of a list.
    ball_vel[0] = ball_vel[0] * 1.1
    ball_vel[1] = ball_vel[1] * 1.1
    
# -----------------------------------
# define event handlers
def draw(c):
    global paddle1_pos, paddle2_pos, ball_pos, ball_vel,countdown, time 
        
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")   # Center Line
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")   # Left Gutter 
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White") # Right Gutter
        
    # update ball : New position = Old Position + (Time * velocity) | Here, Time is the refresh rate time.
    ball_pos[0] = ball_pos[0] + ball_vel[0]
    ball_pos[1] = ball_pos[1] + ball_vel[1] 
    
    # draw ball
    c.draw_circle(ball_pos, BALL_RADIUS,2, "Grey", "White")

    # REFLECTION PART: collide and reflect off of TOP or BOTTOM side of canvas
    if (ball_pos[1] <= BALL_RADIUS) or (ball_pos[1] >= (HEIGHT - 1) - BALL_RADIUS):
        ball_vel[1] = - ball_vel[1]
        
    # REFLECTION PART: collide and reflect off of LEFT hand side of canvas    
    if (ball_pos[0] <= (BALL_RADIUS + PAD_WIDTH)):    # LEFT Gutter touched 
        if ((paddle1_pos[1] + PAD_HEIGHT) >= ball_pos[1] >= paddle1_pos[1] ):  # Left paddle touched
            hit_sound.play()
            increase_vel()
            ball_vel[0] = - ball_vel[0]
        else:
            miss_sound.play()
            score_p2[0] += 1   # Player 2 win. Add score to player 2.  
            if score_p2[0] == 10:
                result_text[1] = "WINS"
                reset()                
            else:
                spawn_ball(RIGHT)  # Spawn ball at winner. 
            
            
    # REFLECTION PART: collide and reflect off of RIGHT hand side of canvas             
    if (ball_pos[0] >= (WIDTH - 1) - (BALL_RADIUS + PAD_WIDTH)):  # RIGHT Gutter touched
        if ((paddle2_pos[1] + PAD_HEIGHT) >= ball_pos[1] >= paddle2_pos[1]):   # RIGHT paddle touched 
            hit_sound.play()
            increase_vel()
            ball_vel[0] = - ball_vel[0]
        else:
            miss_sound.play()
            score_p1[0] += 1   # Player 1 win. Add score to player 1.
            if score_p1[0] == 10:
                result_text[0] = "WINS"
                reset()
            else:
                spawn_ball(LEFT)   # Spawn ball at winner.      
    
   
    # update paddle's vertical position,  
    paddle1_pos[1] += paddle1_vel
    paddle2_pos[1] += paddle2_vel

    # keep paddle on the screen 
    if  paddle1_pos[1] <= 0:   # Check : Keep Left paddle on the screen
        # if the last update set pos[1] i.e. Y = -1 ..then will add that (+)val and keep it on screen.
        paddle1_pos[1] += (paddle1_pos[1] * -1) 
    elif paddle1_pos[1] + PAD_HEIGHT >  HEIGHT:
        # whenever crossing Height limit, reset pos[1], to keep it on screen. 
        paddle1_pos[1] -= (paddle1_pos[1] % (HEIGHT- PAD_HEIGHT))     
        # OR, paddle1_pos[1] =  HEIGHT - PAD_HEIGHT
        
    if  paddle2_pos[1] <= 0: # Check : Keep Right paddle on the screen
        paddle2_pos[1] += (paddle2_pos[1] * -1)
    elif paddle2_pos[1] + PAD_HEIGHT >  HEIGHT:
        paddle2_pos[1] -= (paddle2_pos[1] % (HEIGHT- PAD_HEIGHT))
        # OR, paddle2_pos[1] =  HEIGHT - PAD_HEIGHT

    # draw paddles
    c.draw_line(paddle1_pos, [paddle1_pos[0], (paddle1_pos[1] + PAD_HEIGHT)], PAD_WIDTH, PAD_COLOR)   # Left Paddle
    c.draw_line(paddle2_pos, [paddle2_pos[0], (paddle2_pos[1] + PAD_HEIGHT)], PAD_WIDTH, PAD_COLOR)   # Right Paddle
    
    # draw scores
    c.draw_text(str(score_p1[0]), score_p1[1],score_p1[2], score_p1[3])
    c.draw_text(str(score_p2[0]), score_p2[1],score_p2[2], score_p2[3])
    
    # Draw banner info: 
    if time <> 0:        
        c.draw_text(str(countdown), (275, 340), 100, "White") 
        c.draw_text(banner_text[0], (105, 100), 40, score_color)
        c.draw_text(banner_text[1], (400, 100), 40, score_color)
        
        c.draw_text(result_text[0], (130, 155), 30, score_color)
        c.draw_text(result_text[1], (430, 155), 30, score_color)

# -----------------------------------    
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP['w']:      # Left hand player -> UP     
        paddle1_vel = -acc                 # Reduce Y. Only one dimension
    elif key == simplegui.KEY_MAP['s']:    # Left hand player -> DOWN   
        paddle1_vel = acc                  # Increase Y   
    elif key == simplegui.KEY_MAP['up']:   # Right hand player -> UP   
        paddle2_vel = -acc      
    elif key == simplegui.KEY_MAP['down']: # Right hand player -> DOWN  
        paddle2_vel = acc   
    else:
        pass
        
# -----------------------------------
def keyup(key):
    global paddle1_vel, paddle2_vel    
    paddle1_vel, paddle2_vel = 0, 0         # Stop acceleration

# -----------------------------------
def reset():
    global ball_pos    
    ball_pos = list(center_pos)             # Reset Ball Position, cause countdown will start
    ball_vel[0], ball_vel[1] = [0.0, 0.0]   # Reset Ball Velocity, cause countdown will start
    score_p1[3] = score_p2[3] = "Red"      # Set Score color to Red
    timer.start()                           # Start countdown. 

# -----------------------------------
# Timer added to show Game Start Countdown
def tick():
    global time, countdown, score_color
    time += 1
    countdown -= 1
    # print time, countdown
    if time == 4:        
        timer.stop() # Countdown to Zero ended. 
        countdown = time 
        time = 0
        score_p1[3] = score_p2[3] = "Grey"
        result_text[0] = result_text[1] = " " 
        new_game()   # Now start New game. 
            
# ===================================
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)

# ===================================
# Register EVENT Handlers

frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

frame.add_button("RESTART", reset, 80)

timer = simplegui.create_timer(1000, tick)  # Timer (Per second) added to show Game Start Countdown

# Set Text messages
label = frame.add_label("  ")
label = frame.add_label("Total Game points: 10 ")
label = frame.add_label("Control Key Map:")
label = frame.add_label(" ")
label = frame.add_label("* Player 1 (Left hand Side) *") 
label = frame.add_label("> Paddle Up   = w")
label = frame.add_label("> Paddle Down = s")
label = frame.add_label(" ")
label = frame.add_label("* Player 2 (Right hand Side) *") 
label = frame.add_label("> Paddle Up   = key Up")
label = frame.add_label("> Paddle Down = key down")

# ===================================
# start frame
# new_game()
frame.start()
timer.start()   # First "Game Start countdown" started