#!/usr/bin/python

# Implementation of classic arcade game Pong

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
ball_pos = [WIDTH//2, HEIGHT//2]
ball_vel = [1,1]
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
paddle1_pos = HEIGHT//2
paddle2_pos = HEIGHT//2
paddle1_vel = 0
paddle2_vel = 0
paddle_vel = 5
score1 = 0
score2 = 0
LEFT = False
RIGHT = True        

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    
    #initialize required values
    score1 = 0
    score2 = 0
    paddle1_pos = HEIGHT//2
    paddle2_pos = HEIGHT//2
    #spawn a new game if horizontal component of velocity is greater than zero
    spawn_ball(ball_vel[0] > 0 or ball_vel[0] < 0)

# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    global WIDTH, HEIGHT
    ball_pos = [WIDTH//2,HEIGHT//2]
    if direction == RIGHT:
        ball_vel[0] = random.randrange(2, 4)
        ball_vel[1] = random.randrange(1,3)
    elif direction == LEFT:
        ball_vel[0] = random.randrange(-4,-2)
        ball_vel[1] = random.randrange(1,3)

#draw the canvas
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel
    
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # draw paddles
    #paddle1
    canvas.draw_polygon([(0,paddle1_pos-HALF_PAD_HEIGHT),(PAD_WIDTH,paddle1_pos-HALF_PAD_HEIGHT),(PAD_WIDTH,paddle1_pos+HALF_PAD_HEIGHT),(0,paddle1_pos+HALF_PAD_HEIGHT)],2,"White","White")
    #paddle2
    canvas.draw_polygon([(WIDTH-PAD_WIDTH,paddle2_pos-HALF_PAD_HEIGHT),(WIDTH,paddle2_pos-HALF_PAD_HEIGHT),(WIDTH,paddle2_pos+HALF_PAD_HEIGHT),(WIDTH-PAD_WIDTH,paddle2_pos+HALF_PAD_HEIGHT)],2,"White","White")
     
    # update paddle's vertical position, keep paddle on the screen
    if (paddle1_pos <= HEIGHT - HALF_PAD_HEIGHT and  paddle1_vel > 0) or (paddle1_pos - HALF_PAD_HEIGHT >= 0 and paddle1_vel < 0):
        paddle1_pos += paddle1_vel
    if (paddle2_pos <= HEIGHT - HALF_PAD_HEIGHT and paddle2_vel > 0) or (paddle2_pos - HALF_PAD_HEIGHT >= 0 and paddle2_vel < 0):
        paddle2_pos += paddle2_vel
   
    #draw ball
    canvas.draw_circle(ball_pos,BALL_RADIUS,2,"White","White")
    
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    #if the ball meets the edge of paddle or exceeds it
    if (ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS) or (ball_pos[0] <= PAD_WIDTH + BALL_RADIUS):
        #reflecting the ball off the paddle1
        if (paddle1_pos - HALF_PAD_HEIGHT  <= ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT) and ball_vel[0] < 0:
            ball_vel[0] = -1.05 * ball_vel[0]  #multiplied by -1.05 so as to increase velocity with bounces
            ball_vel[1] = 1 * ball_vel[1]   #the vertical component of velocity is not changed
        #reflecting the ball off the paddle2
        elif (paddle2_pos - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT) and ball_vel[0] > 0:
            ball_vel[0] = -1.05 * ball_vel[0]
            ball_vel[1] = 1 * ball_vel[1] 
        #else if the paddle fails to meet the ball
        else:
            #if the ball crashes into the right gutter
            if (ball_vel[0] > 0):
                score1 += 1  #provide score to player 1
                ball_vel[0] = -ball_vel[0]
                spawn_ball(ball_vel[0] > 0)
            #otherwise the ball crashes into the left gutter
            else:
                score2 += 1  #provide score to player 2
                ball_vel[0] = - ball_vel[0]
                spawn_ball(ball_vel[0] > 0 )
    #else if the ball meets upper wall of the canvas
    #not increasing velocity if it crashes into the wall
    if (ball_pos[1] <= BALL_RADIUS):
        ball_vel[1] = -1 * ball_vel[1]
        ball_vel[0] = 1 * ball_vel[0]
    #not increasing velocity if it crashes into the wall
    #else if the ball meets the lower wall of the canvas 
    elif (ball_pos[1] >= HEIGHT - BALL_RADIUS):
        ball_vel[1] = -1 * ball_vel[1]
        ball_vel[0] = 1 * ball_vel[0]
    
   
   # draw scores 
    canvas.draw_text(str(score1),[150,100],24,"Red")
    canvas.draw_text(str(score2),[450,100],24,"Red")    
    
    
def keydown(key):
    global paddle1_vel, paddle2_vel, paddle2_pos, paddle1_pos, paddle_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= paddle_vel
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel += paddle_vel
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= paddle_vel
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel += paddle_vel
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
def restart():
    new_game()

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart",restart, 100)


# start frame
new_game()
frame.start()
