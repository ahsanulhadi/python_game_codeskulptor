# ======================================================================|
# === A map of BANGLADESH with a draggable magnification option. =======|
# === Written by: Ahsanul Hadi    ======================================|
# === Date: Nov 17, 2013     ===========================================|
# === Sample Code Source:  Codeskulptor.org Documentation and examples. |
# ======================================================================|
# === Version # --- Update Date  ---- Change Descriptions --------------|
# ===    1.0   ---- Nov 17, 2013 ---- 
# ===
# ======================================================================|
# Note: Need to modify code for corner viewing issues. 

import simplegui
# =====================================
# Variable DECLARATIONS
map_url = 'https://dl.dropboxusercontent.com/u/7177475/map_bangladesh.png'
IMG_WIDTH, IMG_HEIGHT = 2348, 2948    # MAP width, Height 
SCALE = 4   # Scaling Factor 
F_WIDTH, F_HEIGHT = (IMG_WIDTH // SCALE), (IMG_HEIGHT // SCALE)  # Frame width, height 
center_source = [(IMG_WIDTH // 2), (IMG_HEIGHT // 2)]   # Source Image's Center Position
center_dest = [(F_WIDTH // 2), (F_HEIGHT // 2)]   # Frame's Center Position 
# Magnifier scale and position
MAG_SIZE = 50 * SCALE   # Size of magnification
mag_pos = [(IMG_WIDTH // (2 * SCALE)), (IMG_HEIGHT // (2 * SCALE))]   # Magnifying Glass position
message = "Loading "
msg_color = "White"
counter = 0
# =====================================
# Define HELPER FUNCTIONS to initialize globals.

# =====================================     
# Define EVENT HANDLERS
# Allow magnifier to be dragged
def drag(pos):
    mag_pos[0] = pos[0]
    mag_pos[1] = pos[1]
    
# Move magnifier to clicked position
def click(pos):
    mag_pos[0] = pos[0]
    mag_pos[1] = pos[1]

# Timer Handler which keeps time and check for Image Loading status. 
def load():
    global image_found, message, counter, msg_color
    image_found = ((0,0) != (image.get_width(), image.get_height()))     
    if image_found:
        timer.stop()
        frame.set_draw_handler(draw)
    elif counter >= 10:
        timer.stop()
        message = "Image Not Found."
        msg_color = "Red"
    else:
        message += "."        
    counter += 1      # Added 
        
# Until the Image is loaded, print a notification message.
def draw_loading(canvas):
    canvas.draw_text(message, [50, 60], 20, msg_color)
    canvas.draw_text("Time: "+ str(counter) + " sec.", [50, 100], 17, "White")

# Image loaded, now Draw map and magnified region
def draw(canvas):
    # Draw Map 
    canvas.draw_image(image, center_source, (IMG_WIDTH, IMG_HEIGHT), center_dest, (F_WIDTH, F_HEIGHT))
    # Draw magnifier    
    map_center = [SCALE * mag_pos[0], SCALE * mag_pos[1]]
    map_rectangle = [MAG_SIZE, MAG_SIZE]    
    mag_center = mag_pos
    mag_rectangle = [MAG_SIZE, MAG_SIZE]
    canvas.draw_image(image, map_center, map_rectangle, mag_center, mag_rectangle)        
    # Draw outline around magnifier
    magleft  = mag_center[0] - (mag_rectangle[0] // 2)
    magright = mag_center[0] + (mag_rectangle[0] // 2)
    magtop   = mag_center[1] - (mag_rectangle[1] // 2)
    magbottom = mag_center[1] + (mag_rectangle[1] // 2)    
    magtopleft = (magleft, magtop)
    magtopright = (magright, magtop)
    magbotleft = (magleft, magbottom)
    magbotright = (magright, magbottom)    
    box = [magtopleft, magbotleft, magbotright, magtopright, magtopleft] 
    canvas.draw_polyline(box, 2, "Black")
# =====================================
# CREATE Frame, add frame objects, labels, Timers.
frame = simplegui.create_frame("Bangladesh Map", F_WIDTH, F_HEIGHT)
image = simplegui.load_image(map_url)
timer = simplegui.create_timer(1000, load)
# =====================================
# REGISTER event handlers.    
frame.set_draw_handler(draw_loading)
frame.set_mousedrag_handler(drag)
frame.set_mouseclick_handler(click)
# =====================================
# INITIATE Application.
# Start timer and window animation
timer.start()
frame.start()
# =====================================









