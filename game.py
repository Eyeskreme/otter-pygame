import pygame
from pygame.locals import *
import os
import sys
import math
import random

pygame.init()

Width=800
Height = 400 
win = pygame.display.set_mode((Width,Height))
pygame.display.set_caption('otter simulator')

#load background image

bg = pygame.image.load(os.path.join('images','full-bg.png')).convert()
background1 = 0
background2 = bg.get_width()

clock = pygame.time.Clock()
music = pygame.mixer.music.load('action.mp3')
pygame.mixer.music.play(-1)
jumpsound = pygame.mixer.Sound ('jump.wav')


# character animation

class player(object):
    run = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(60,64)]
    
    jump = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(50,53)]
    fall = pygame.image.load(os.path.join('images','F1.png'))
    jumpList = [1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4]
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.falling = False
        self.jumpCount = 0
        self.runCount = 0

        
     # chararcter action screen position
    def draw(self, win):
        if self.falling:
            win.blit(self.fall, (self.x, self.y + 20))
                
        elif self.jumping:
            self.y -= self.jumpList[self.jumpCount] * 1.0
            win.blit(self.jump[self.jumpCount//40], (self.x,self.y))
            self.jumpCount += 1
            if self.jumpCount > 108:
                self.jumpCount = 0
                self.jumping = False
                self.runCount = 0
            # draw hitbox
            self.hitbox = (self.x+80,self.y+40,self.width-30,self.height-35)
                    
        else:
            if self.runCount > 50:
                self.runCount = 0
            win.blit(self.run[self.runCount//13], (self.x,self.y))
            self.runCount += 1
            self.hitbox = (self.x+100,self.y+40,self.width-90,self.height-35)
        



# obstacles

class rock:
    image = pygame.image.load(os.path.join('images', 'boulder.png'))
    
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    #draw hitbox
    def draw(self,win):
        self.hitbox = (self.x +10, self.y +5 ,self.width-15,self.height-20)
        
        win.blit((self.image), (self.x,self.y))
#collison statement
    def collide(self, rect):
        if rect[0] + rect[2] < self.hitbox[0] and rect[0] > self.hitbox[0] + self.hitbox[3]:
            if rect[1]+rect[3] > self.hitbox[1]:
                return True #fall
        return False

# scoresheet    
def updatescore():
    f = open('scores.txt','r')
    file = f.readlines()
    last = int(file[0])

   #update score
    if last < int(score):
        f.close()
        file = open('scores.txt', 'w')
        file.write(str(score))
        file.close()

        return score
               
    return last



def endgame():
    global speed, obstacles,score, pause 
    pause = 0
    speed = 20
    obstacles = []
    
    #main loop               
    running = True
    while running:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
              # to restart game
            if event.type == pygame.MOUSEBUTTONDOWN:
                running = False
                runner.falling = False
                runner.sliding = False
                runner.jumping = False
    #draw the screen
        win.blit(bg, (0,0))
        Font = pygame.font.SysFont('Broadway', 80)
        thisFont = pygame.font.SysFont('Broadway',40)
        lastScore = Font.render('High Score: ' + str(updatescore()),1,(255,255,255))

        currentScore = Font.render('Score: '+ str(score),1,(255,255,255))
        instruction = thisFont.render('Click to play again',1,(225,0,0))


        win.blit(lastScore, (Width/2 - lastScore.get_width()/2,150))
        win.blit(currentScore, (Width/2 - currentScore.get_width()/2, 240))
        win.blit(instruction,(Width/2 - instruction.get_width()/2,320))
        pygame.display.update()
    score = 0

        


def redrawWindow():
    Font = pygame.font.SysFont('Broadway', 25)
    win.blit(bg, (background1, 0))
    win.blit(bg, (background2,0))
    text = Font.render('Score: ' + str(score), 1, (255,255,255))
    runner.draw(win)
    for obstacle in obstacles:
        obstacle.draw(win)

    win.blit(text, (680, 80))
    pygame.display.update()


pygame.time.set_timer(USEREVENT+1, 500)
pygame.time.set_timer(USEREVENT+2, 2500)
speed = 40

score = 0


running = True
#draw player
runner = player(100,315,0,0)

obstacles = []
pause = 0
fallSpeed = 0

while running:
    if pause > 0:
        pause += 1
        if pause > fallSpeed * 2:
            endgame()
        
    score = speed//10 - 3
    
    #character collision

    for obstacle in obstacles:
        if obstacle.collide(runner.hitbox):
            runner.falling = True
            
            if pause == 0:
                pause = 1
                fallSpeed = speed
                
        if obstacle.x < -60:
            obstacles.pop(obstacles.index(obstacle))
        else:
            obstacle.x -= 1.5
    #refresh background
    background1 -= 1.5
    background2 -= 1.5

    if background1 < bg.get_width() * -1:
        background1 = bg.get_width()
    if background2 < bg.get_width() * -1:
        background2 = bg.get_width()
 
    # quit the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
            
        if event.type == USEREVENT+1:
            speed += 2
          #draw obstacle  
        if event.type == USEREVENT+2:
            obstacles.append(rock(800, 310, 70, 70))

            
    # game controls                            
    if runner.falling == False:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            if not(runner.jumping):
                runner.jumping = True
                jumpsound.play()

        
    clock.tick(speed)
    redrawWindow()