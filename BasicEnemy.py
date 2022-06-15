import random 
import pygame
import math
from QuestonObject import QuestionObject

class BasicEnemy():
    def __init__(self, game, pos):
        self.game = game
        self.id = 'Enemy'

        self.question_object = QuestionObject(self.game, self)

        self.velX = random.choice([-1, 1])
        self.velY = 0

        self.gravity = -0.4

        self.player_chase = False
        self.random_jump = random.randint(40, 60)
        self.jumping = False

        self.direction_change = random.randint(200, 300)

        self.rect = pygame.Rect(pos, (64, 64))
        self.rect.topleft = pos
    
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
        self.question_object.draw(screen)

    def moveX(self):
        if self.velX >= 5: self.velX = 5 #Limit right movement speed
        if self.velX <= -5: self.velX = -5 #Limit left movement speed
        self.rect.x += self.velX #Change x position by velX
        for i in self.game.gamescreen.gameObjects: #Loop through all game objects on the screen
            if i.id == 'Floor': #If it is a floor object
                if i.rect.colliderect(self.rect): #If it is colliding with the player
                    #Left to right collision
                    if self.velX > 0:
                        self.rect.right = i.rect.left
                        if not self.jumping:
                            self.velY = -7.5
                            self.jumping = True
                    elif self.velX < 0:
                        self.rect.left = i.rect.right
                        if not self.jumping:
                            self.velY = -7.5
                            self.jumping = True

    def moveY(self):
        if self.velY >= 8 : self.velY = 8 #Limit fall speed
        self.rect.y += self.velY #Change y position by velY
        for i in self.game.gamescreen.gameObjects: #Loop through all game objects on the screen
            if i.id == 'Floor': #If it is a floor object
                if i.rect.colliderect(self.rect): #If it is colliding with the player 
                    #Top to bottom collision
                    if self.velY > 0 : 
                        self.rect.bottom = i.rect.top
                        if self.jumping:
                            self.jumping = False
                            self.random_jump = random.randint(40, 60)
                    #Bottom to top collision
                    elif self.velY < 0 :
                        self.rect.top = i.rect.bottom
    
    def update(self):
        self.question_object.update()
        self.velY -= self.gravity #Constant gravity decrease to velY

        for i in self.game.gamescreen.gameObjects:
            if i.id == 'Player':
                player_x = i.rect.x
                player_y = i.rect.y

        if self.direction_change <= 0:
            self.velX *= -1
            self.direction_change = random.randint(200, 300)
        else:
            self.direction_change -= 1

        if self.rect.x <= -64:
            self.game.gamescreen.gameObjects.remove(self)

        if self.player_chase:
            if player_x - self.rect.x < 0:
                self.velX = -3
            elif player_x - self.rect.x > 0:
                self.velX = 3

            if self.random_jump <= 0 and not self.jumping:
                self.velY = -7.5
                self.jumping = True
            else:
                self.random_jump -= 1
        
        elif (abs(math.sqrt((player_x-self.rect.x)**2 + (player_y-self.rect.y)**2))) <= 200:
                    self.player_chase = True
        
        self.moveX()
        self.moveY()
