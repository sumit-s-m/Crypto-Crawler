# import packages

import pygame 
from pygame.locals import *
pygame.init()

# Create game window
screen_width = 600
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong Game')


# Initilaize variables
fpsClock = pygame.time.Clock()
fps =60
white = (255,255,255)
bg = (0,0,0)
winner = 0
cpu_score = 0
p_score = 0
font = pygame.font.SysFont('Constantia', 30)
live_ball = False
speed_count=0
run = True
collide_sound = pygame.mixer.Sound('mixkit-player-jumping-in-a-video-game-2043.wav')
restart_sound = pygame.mixer.Sound('mixkit-unlock-game-notification-253.wav')
lost_sound = pygame.mixer.Sound('mixkit-player-boost-recharging-2040.wav')


# define top_border function for drawing border line on game window
def top_border() :
    screen.fill(bg)
    pygame.draw.line(screen, white, (0,50), (screen_width,50))

def add_text_on_screen(text, font, text_color, x, y) :
    img = font.render(text, True, text_color)
    screen.blit(img, (x,y))



# Define class and create objects for paddles 
class paddle() :
        def __init__(self, x, y) :
          self.x = x
          self.y = y 
          self.rect = Rect(self.x, self.y, 20, 100)
          self.speed = 5
        
        # move the paddle with self.speed in y direction up and down using keyboard up and down keys respectively
        def move(self) :
            key = pygame.key.get_pressed()
            if key[pygame.K_UP] and self.rect.top > 50:
                self.rect.move_ip(0, -1 * self.speed)
            if key[pygame.K_DOWN] and self.rect.bottom < screen_height:
                self.rect.move_ip(0, self.speed)   

        # move the cpu paddle with respect to the center of the pong ball 
        def ai(self) :
            if self.rect.centery < p_ball.rect.top and self.rect.bottom < screen_width-100 :
                self.rect.move_ip(0, self.speed)

            if self.rect.centery > p_ball.rect.bottom and self.rect.top > 50 :
                self.rect.move_ip(0, -1 * self.speed)     
        
        # draw the paddles on the game screen
        def draw(self) :
            pygame.draw.rect(screen, white, self.rect)


player_paddle = paddle(screen_width-20, screen_height//2)
cpu_paddle = paddle(0, screen_height//2)



# Define class and create objects for pong ball
class ball() :
    def __init__(self, x, y) :
          self.reset(x,y)
    

    # move the paddle in x and y directions with speeds self.speed_x and self.spped_y respectively 
    def move(self) :
        
        if self.rect.top < 50 :
            self.speed_y *= -1

        if self.rect.bottom > screen_height :
            self.speed_y *= -1 
        
        # Detect if the pong ball collides with the player paddle or cpu paddle and if true invert the x direction speed sign

        if self.rect.colliderect(player_paddle) or self.rect.colliderect(cpu_paddle) :
            collide_sound.play()
            self.speed_x *= -1
        
         # if the pong ball is missed by either cpu or player then return the winner
        if self.rect.left<0 :
            self.winner = 1
        
        if self.rect.right > screen_width :
            self.winner = -1

        # update the position of the pong ball during the play    

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        return self.winner
    
    # draw the ball on the screen according to the updated co-ordinates
    def draw(self) :
        pygame.draw.circle(screen, white, (self.rect.x + self.ball_radius, self.rect.y + self.ball_radius), self.ball_radius)


    # reset the ball cordinates if game restarts
    def reset(self, x, y) :
          self.x = x
          self.y = y 
          self.ball_radius = 8
          self.rect = Rect(self.x, self.y, self.ball_radius*2, self.ball_radius*2)
          self.speed_x = -2
          self.speed_y = 3
          self.winner = 0

p_ball = ball(screen_width-60, screen_height//2 + 50)


# run the game until the player exits the game
while run :

    # draw the required text on the game screen
    fpsClock.tick(fps)
    top_border()
    add_text_on_screen('CPU : ' + str(cpu_score), font, (150,200,220), 10,15)
    add_text_on_screen('You : ' + str(p_score), font, (220,50,150), screen_width-100,15)
    if abs(p_ball.speed_x) < 4 : level_color=(0,255,0)
    elif abs(p_ball.speed_x) >= 4 and abs(p_ball.speed_x) < 6 : level_color = (0,0,255)
    else : level_color = (255,0,0)
    add_text_on_screen('Difficulty Level : ' + str(abs(p_ball.speed_x)), font, level_color, screen_width//2-120 ,15)
    
    player_paddle.draw()
    cpu_paddle.draw()

    if live_ball == True:
        speed_count += 1
        winner = p_ball.move()
        if winner == 0 :
           
           player_paddle.move()
           cpu_paddle.ai()
           p_ball.draw()
        
        else :
            live_ball = False 
            if winner == 1 :
                p_score += 1
                lost_sound.play()
            elif winner == -1 :
                cpu_score+=1
                lost_sound.play()

    # updating the scores and difficulty level of game
    if live_ball == False :
        if winner == 0 :
            p_ball.speed_x=1
            p_ball.speed_y=1    
            add_text_on_screen('Press Space to Start', font, (255,255,255), screen_width//2-120, screen_height//2)
    
        if winner == 1 :
            p_ball.speed_x=1
            p_ball.speed_y=1    
            add_text_on_screen('BRAVO! You Scored', font, (255,255,255), screen_width//2-120, screen_height//2)
            add_text_on_screen('Press Space to continue', font, (255,255,255), screen_width//2-140, screen_height//2+50)

        if winner == -1 :
            p_ball.speed_x=1
            p_ball.speed_y=1
            add_text_on_screen('Alas, You Lost', font, (255,255,255), screen_width//2-80, screen_height//2)
            add_text_on_screen('Press Space to continue', font, (255,255,255), screen_width//2-140, screen_height//2+50)



    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            run = False
         
        # start or restart the game 
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and pygame.K_SPACE and live_ball == False :
            live_ball = True
            restart_sound.play()    
            p_ball.reset(screen_width-60, screen_height//2 + 50)


        # update the speed of the bong ball
        if speed_count > 500 :
            speed_count = 0 
            if p_ball.speed_x < 0 :
                p_ball.speed_x -= 1
            if p_ball.speed_x > 0 :
                p_ball.speed_x += 1
            if p_ball.speed_y < 0 :
                p_ball.speed_y -= 1
            if p_ball.speed_y > 0 :
                p_ball.speed_y += 1


    pygame.display.update()

pygame.quit()            