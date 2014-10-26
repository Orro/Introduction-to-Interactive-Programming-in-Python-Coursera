# Implementation of classic arcade game Pong
#
# 31/08/2013

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [3, 10]
paddle1_pos = [HALF_PAD_WIDTH, HEIGHT / 2]
paddle2_pos = [WIDTH - HALF_PAD_WIDTH, HEIGHT / 2]
paddle1_vel = [0, 0]
paddle2_vel = [0, 0]
acc = 10
score1 = 0
score2 = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
        
    if direction == LEFT:
        ball_vel = [(-random.randrange(120, 240))/60, (-random.randrange(60, 180))/60]        
    else:
        ball_vel = [(random.randrange(120, 240))/60, (-random.randrange(60, 180))/60]
        
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    score1 = 0
    score2 = 0
    spawn_ball(LEFT)
    
def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, acc
 
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1] 
    
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    elif ball_pos[1] >= (HEIGHT - BALL_RADIUS):
        ball_vel[1] = -ball_vel[1]
    
    if (ball_pos[0] - BALL_RADIUS <= PAD_WIDTH) and ((paddle1_pos[1] - ball_pos[1] > HALF_PAD_HEIGHT) or 
                                       (ball_pos[1] - paddle1_pos[1] > HALF_PAD_HEIGHT)):
        spawn_ball(RIGHT)
        score2 += 1			# if the ball did not hit the paddle, a new ball is spawned and the score is increased
    elif (ball_pos[0] - BALL_RADIUS <= PAD_WIDTH) and ((paddle1_pos[1] - ball_pos[1] < HALF_PAD_HEIGHT) or 
                                         (ball_pos[1] - paddle1_pos[1] < HALF_PAD_HEIGHT)):
         ball_vel[0] = -ball_vel[0] * 110/100   # if the ball hit the paddle the horizontal velocity is increased by 10%
    
    if (ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH) and ((paddle2_pos[1] - ball_pos[1] > HALF_PAD_HEIGHT) or 
                                       (ball_pos[1] - paddle2_pos[1] > HALF_PAD_HEIGHT)):
        spawn_ball(LEFT)	# if the ball did not hit the paddle, a new ball is spawned and the score is increased
        score1 += 1
    elif (ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH) and ((paddle2_pos[1] - ball_pos[1] < HALF_PAD_HEIGHT) or 
                                       (ball_pos[1] - paddle2_pos[1] < HALF_PAD_HEIGHT)):
         ball_vel[0] = -ball_vel[0] * 110/100	 # if the ball hit the paddle the horizontal velocity is increased by 10%    
    
    # draw ball
    c.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    
    if (paddle1_pos[1] + paddle1_vel[1] >= (HALF_PAD_HEIGHT)) and (paddle1_pos[1] + paddle1_vel[1] <=
                                                                   (HEIGHT - HALF_PAD_HEIGHT)):
        paddle1_pos[1] += paddle1_vel[1]
   
    if (paddle2_pos[1] + paddle2_vel[1] >= HALF_PAD_HEIGHT) and (paddle2_pos[1] + paddle2_vel[1] <=
                                                                 HEIGHT - HALF_PAD_HEIGHT):    
        paddle2_pos[1] += paddle2_vel[1]
    
    # draw paddles
    c.draw_polygon([(0, paddle1_pos[1] - HALF_PAD_HEIGHT), (PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT),
                    (PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT), (0, paddle1_pos[1] + HALF_PAD_HEIGHT)],
                   2, "White", "White")
    c.draw_polygon([(WIDTH - PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT), (WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT),
                    (WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT), (WIDTH - PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT)],
                   2, "White", "White")
    # draw scores
    c.draw_text(str(score1), [200, 110], 50, "White")    
    c.draw_text(str(score2), [400, 110], 50, "White")    
        
def keydown(key):
    global paddle1_vel, paddle2_vel, acc
    
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel[1] -= acc
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel[1] += acc
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel[1] += acc
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel[1] -= acc   

def keyup(key):
    global paddle1_vel, paddle2_vel
    paddle1_vel = [0, 0]
    paddle2_vel = [0, 0]

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game, 100)

# start frame
new_game()
frame.start()
