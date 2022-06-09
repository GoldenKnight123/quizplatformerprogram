import pygame
from tkinter import messagebox

class Player(): 
    def __init__(self, game, pos):
        self.game = game
        self.id = 'Player' #Allocate player id
        
        self.direction = 0 #Direction value used for animation and flipping

        #Attempt to load sound files
        try:
            self.jump_sound = pygame.mixer.Sound('Selected Assets/Game Sounds/Player Jump.wav')
            self.run_sound = pygame.mixer.Sound('Selected Assets/Game Sounds/Footsteps.wav')
            self.run_sound_cooldown = 20
        
        #On file not found error give popup message that game may crash
        except FileNotFoundError:
            messagebox.showinfo('Error', 'Game files are missing. Game may crash unexpectedly or not display textures.')

        self.velX = 0
        self.velY = 0

        self.gravity = -0.4
        self.jumping = False
        self.jump_cooldown = 3
        self.moving = False

        self.animation_cooldown = 30 #Cooldown for animation ticks
        self.last_time = pygame.time.get_ticks() #Previous tick time
        
        #Attempt to import animation frames
        try:
            self.idleAnimation = []
            for i in range(15):
                self.idleAnimation.append(pygame.image.load(f'Selected Assets/Player/Idle ({i+1}).png').convert_alpha())

            self.jumpAnimation = []
            for i in range(15):
                self.jumpAnimation.append(pygame.image.load(f'Selected Assets/Player/Jump ({i+1}).png').convert_alpha())
            
            self.runAnimation = []
            for i in range(15):
                self.runAnimation.append(pygame.image.load(f'Selected Assets/Player/Run ({i+1}).png').convert_alpha())

        #On file not found error give popup message that game may crash
        except FileNotFoundError:
            messagebox.showinfo('Error', 'Game files are missing. Game may crash unexpectedly or not display textures.')
        
        self.frame = 0

        self.rect = pygame.Rect(pos, (64, 126)) #Create the rectangular hitbox of the player
        self.rect.topleft = pos #Set the top of the rectangle to the given position

        self.processImage()

    def processImage(self): #This function updates the frame the animation is on
        if self.jumping:
            self.image = self.jumpAnimation[self.frame]
        elif self.moving:
            self.image = self.runAnimation[self.frame]
        elif not self.jumping:
            self.image = self.idleAnimation[self.frame] #Sets the image to the frame the animation should be on
        self.size = self.image.get_size() #Get the size of the image
        self.scaled_image = pygame.transform.scale(self.image, (int(self.size[0]/4), int(self.size[1]/4))) #Rescale it to 25% of the original size
        self.flipped_image = self.scaled_image
        
        if self.direction == 1:
            self.flipped_image = pygame.transform.flip(self.scaled_image, True, False)
    
    def draw(self, screen):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_time >= self.animation_cooldown: #If cooldown is reached
            if self.jumping and self.frame == 14:
                pass
            else:
                self.frame += 1 #Go to next frame
            self.last_time = current_time #Set the last time to current time
            if self.frame >= len (self.idleAnimation): #If animation ended repeat it
                self.frame = 0
        self.processImage()
        #pygame.draw.rect(screen, (0, 0, 0), self.rect) #For debugging purposes and seeing hitboxes
        if self.direction == 1:
            screen.blit(self.flipped_image, (self.rect.x-28, self.rect.y), (60, 0, 100, 141)) #Draw itself onto the screen with the rectangle hitbox as the surface/position for reference
        else:
            screen.blit(self.flipped_image, self.rect) #Draw itself onto the screen with the rectangle hitbox as the surface/position for reference

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
                    elif self.velX < 0:
                        self.rect.left = i.rect.right  

    def moveY(self):
        keys = pygame.key.get_pressed()
        if self.velY >= 8 : self.velY = 8 #Limit fall speed
        self.rect.y += self.velY #Change y position by velY
        for i in self.game.gamescreen.gameObjects: #Loop through all game objects on the screen
            if i.id == 'Floor': #If it is a floor object
                if i.rect.colliderect(self.rect): #If it is colliding with the player 
                    #Top to bottom collision
                    if self.velY > 0 : 
                        self.rect.bottom = i.rect.top
                        self.jumping = False
                        if not keys[pygame.K_SPACE]:
                            self.jump_cooldown = 3
                    #Bottom to top collision
                    elif self.velY < 0 :
                        self.rect.top = i.rect.bottom
    
    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]: #Upon left momvement key press
            self.velX -= 0.5 #Accelerate to the left
            self.direction = 1 #Set direction to left
            self.moving = True
        if keys[pygame.K_RIGHT]: #Upon right movement key press
            self.velX += 0.5 #Accelerate to the right
            self.direction = 0 #Set direction to right
            self.moving = True
        if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]: #When no keys are pressed
            if self.velX > 0:
                self.velX -= 0.5
            elif self.velX < 0:
                self.velX += 0.5
            self.moving = False
            self.run_sound_cooldown = 20

        if keys[pygame.K_SPACE] and self.jump_cooldown == 3 and not self.jumping: #If jump key pressed and the player is able to jump
            self.velY = -7.5 #Boost into the air
            self.jump_cooldown -= 1 #Set jump cooldown so the player cannot jump again in the air
            self.jumping = True
            self.frame = 0
            self.jump_sound.play()
            print(self.jump_cooldown)   
        
        if not keys[pygame.K_SPACE] and self.jump_cooldown == 2: #If jump key pressed and the player is able to jump
            self.jump_cooldown = 1
            print(self.jump_cooldown)  

        if keys[pygame.K_SPACE] and self.jump_cooldown == 1: #If jump key pressed and the player is able to jump
            self.velY = -7.5 #Boost into the air
            self.jump_cooldown -= 1 #Set jump cooldown so the player cannot jump again in the air
            self.jumping = True
            self.frame = 0
            self.jump_sound.play()
            print(self.jump_cooldown)

        if self.moving and not self.jumping:
            if self.run_sound_cooldown <= 0:
                self.run_sound.play()
                self.run_sound_cooldown = 20
            else:
                self.run_sound_cooldown -= 1

        self.velY -= self.gravity #Constant gravity decrease to velY

        self.moveX()
        self.moveY()
