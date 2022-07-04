import random 
import pygame
import math
from QuestonObject import QuestionObject
from tkinter import messagebox

class BasicEnemy():
    def __init__(self, game, pos, walkAnimation, runAnimation, jumpAnimation):
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
        if self.velX < 0:
            self.direction = 1
        elif self.velX > 0:
            self.direction = 0

        self.rect = pygame.Rect(pos, (64, 126))
        self.rect.topleft = pos

        self.walkAnimation = walkAnimation
        self.runAnimation = runAnimation
        self.jumpAnimation = jumpAnimation

        self.frame = 0
        self.animation_cooldown = 30
        self.last_time = pygame.time.get_ticks()
    
    def processImage(self):
        if self.jumping:
            self.image = self.jumpAnimation[self.frame]
        elif self.player_chase:
            self.image = self.runAnimation[self.frame]
        elif not self.jumping:
            self.image = self.walkAnimation[self.frame]

        self.size = self.image.get_size() #Get the size of the image
        self.scaled_image = pygame.transform.scale(self.image, (int(self.size[0]/4), int(self.size[1]/4))) #Rescale it to 25% of the original size
        self.flipped_image = self.scaled_image
        
        if self.direction == 1:
            self.flipped_image = pygame.transform.flip(self.scaled_image, True, False)
    
    def draw(self, screen):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_time >= self.animation_cooldown: #If cooldown is reached
            self.frame += 1 #Go to next frame
            self.last_time = current_time #Set the last time to current time
            if self.frame >= len (self.walkAnimation): #If animation ended repeat it
                self.frame = 0
        
        #pygame.draw.rect(screen, (255, 0, 0), self.rect)

        if not self.game.gameState == 'QUESTIONVIEW' and not self.game.gameState == 'PAUSED':
            self.processImage()

        if self.direction == 1:
            screen.blit(self.flipped_image, (self.rect.x-85, self.rect.y)) #Draw itself onto the screen with the rectangle hitbox as the surface/position for reference
        else:
            screen.blit(self.flipped_image, self.rect) #Draw itself onto the screen with the rectangle hitbox as the surface/position for reference

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
                            self.frame = 0
                    elif self.velX < 0:
                        self.rect.left = i.rect.right
                        if not self.jumping:
                            self.velY = -7.5
                            self.jumping = True
                            self.frame = 0

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

        if self.velX < 0:
            self.direction = 1
        elif self.velX > 0:
            self.direction = 0

        for i in self.game.gamescreen.gameObjects:
            if i.id == 'Player':
                player_x = i.rect.x
                player_y = i.rect.y
                player_dead = i.dead

        if player_dead and self.player_chase:
            self.player_chase = False
            self.velX = random.choice([-1, 1])

        if self.direction_change <= 0:
            self.velX *= -1
            self.direction_change = random.randint(200, 300)
        else:
            self.direction_change -= 1

        if self.rect.x <= -64:
            self.game.gamescreen.gameObjects.remove(self)

        if self.rect.y >= 720:
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
        
        elif (abs(math.sqrt((player_x-self.rect.x)**2 + (player_y-self.rect.y)**2))) <= 200 and not player_dead:
                    self.player_chase = True
        
        self.moveX()
        self.moveY()