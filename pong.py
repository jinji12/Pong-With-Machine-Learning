import pygame
import time 
pygame.init()

# SETTING CONSTANTS 

WIDTH = 700
HEIGHT = 500

PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
BALL_RADIUS = 7 

WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # setting the window
pygame.display.set_caption("Pong") # caption of display

FPS = 60 # caps fps to 60

# colors that the game uses 
WHITE = (255,255,255)
BLUE = (0,0,255)
BLACK = (0,0,0)


SCORE_FONT = pygame.font.SysFont("IMPACT", 50)
PAUSE_FONT = pygame.font.SysFont("IMPACT", 100)
WINNER_FONT = pygame.font.SysFont("IMPACT", 60)

WINNING_SCORE = 10 # first to 10 to win 


# creating paddle object 
class Paddle: 
    COLOR = WHITE
    VEL = 4

    def __init__(self, x, y, width, height): # constuctor
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height
    
    def draw(self, win): # drawing paddles
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))
    
    def move(self, up=True): # adding movement for paddles 
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL
    
    def reset_paddle(self): # moves the paddles to thier original position 
        self.x = self.original_x
        self.y = self.original_y

# functions for paddles 
def handle_paddle_movement(keys, left_paddle, right_paddle): # this will handle paddle movement 
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0: # w and s for the left paddle 
        left_paddle.move(up = True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL <= HEIGHT - PADDLE_HEIGHT: # checking for collision with top and bottom of screen
        left_paddle.move(up = False)

    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0: # arrow up and arrow down for the right paddle 
        right_paddle.move(up = True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL <= HEIGHT - PADDLE_HEIGHT: # checking for collision with top and bottom of screen
        right_paddle.move(up = False)

def resetpaddles(left_paddle, right_paddle): # this will reset the both paddles to thier original position 
    left_paddle.reset_paddle()
    right_paddle.reset_paddle()


# creating the ball object 
class Ball:
    MAX_VEL = 6 # constants for balls 
    COLOR = WHITE

    def __init__(self, x, y, radius): # ball constructor 
        self.x = self.original_x = x
        self.y = self.origial_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win): # drawing the ball drawing 
        pygame.draw.circle(win, self.COLOR, (self.x, self.y),self.radius)

    def move(self): # movement for the ball
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self): # resets the ball to the center 
        self.x = self.original_x
        self.y = self.origial_y
        self.y_vel = 0 
        self.x_vel *= -1 # redirecting the ball for the person who loss the points serve 


#this function will handle ball collision 
def handle_collision(ball, left_paddle, right_paddle): 
    # this will compare ball position with bottom and top of the screen and redirect the ball inversely with how it collided 
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1
    
    if ball.x_vel < 0: # this is the logic for the ball hitting the left paddle
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1
                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL # this calculates the angle that the ball should be shot out porportial to where it was hit on the position of the paddle 
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = y_vel * -1
    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1
                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = y_vel * -1

def draw(win, paddles, ball , left_score, right_score, game_pause, pause_start_time): # draw function 

    win.fill(BLACK)

    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE) # for score board 
    right_score_text = SCORE_FONT.render(f"{right_score}", 1 , WHITE)
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width() // 2, 20))
    win.blit(right_score_text, (WIDTH * (3/4) - right_score_text.get_width() // 2, 20))


    for paddle in paddles: # drawing the paddles
        paddle.draw(win)

    for i in range(10, HEIGHT, HEIGHT // 20): # this creates a dotted line directly down the middle of the screen 
        pygame.draw.rect(win, WHITE, (WIDTH // 2 - 5, i, 10, HEIGHT // 40))


    ball.draw(win) # draws the ball

    if game_pause: # logic for pausing the game and starting it once the timer is over to give a sort of round break 
        elapsed_time = time.time() - pause_start_time
        if elapsed_time < 3:
            timer = 3 - int(elapsed_time)
            timer_text = PAUSE_FONT.render(str(timer), 1, BLUE)
            timer_pos = (WIDTH // 2 - timer_text.get_width() // 2, HEIGHT // 2 - timer_text.get_height() // 2) # displays the count down timer 
            win.blit(timer_text, timer_pos)

    pygame.display.update()


# main function 
def main():
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT) # creating the paddle objects 
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS) # creating the ball object 

    left_score = 0 # for scoring 
    right_score = 0

    game_pause = False # for round pauses 
    pause_start_time = 0


    while run: # draw loop 
        clock.tick(FPS)
        draw(WIN, [left_paddle,right_paddle], ball, left_score, right_score , game_pause , pause_start_time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed() # handeling user key input 
        handle_paddle_movement(keys, left_paddle, right_paddle)

        if not game_pause: # keeps the movement of the ball when game isnt paused 
            handle_collision(ball, left_paddle, right_paddle)
            ball.move()



        if ball.x < 0: # when the right player scores 
            right_score += 1
            ball.reset()
            resetpaddles(left_paddle, right_paddle)
            game_pause = True
            pause_start_time = time.time()
        elif ball.x > WIDTH: # when the left player scores 
            left_score += 1
            ball.reset()
            resetpaddles(left_paddle, right_paddle)
            game_pause = True
            pause_start_time = time.time()

        won = False
        if left_score >= WINNING_SCORE: # checking for winner 
            won = True
            win_text = "Left Player Won!"
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "Right Player Won!"

        if won: # will display the winner and reset the game 
            text = WINNER_FONT.render(win_text, 1 , WHITE)
            WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset
            resetpaddles(left_paddle, right_paddle)
            left_score = 0
            right_score = 0

        if game_pause: # stops the game for 3 seconds once someone scores 
            elapsed_time = time.time() - pause_start_time
            if elapsed_time >= 3:
                game_pause = False

    pygame.quit()

if __name__ == '__main__':
    main()