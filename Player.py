import pygame

class Player():
    def __init__(self, game, pos):
        self.game = game
        
        self.x = pos[0]
        self.y = pos[1]

        self.velX = 0
        self.velY = 0

        self.gravity = -0.2
        self.jumping = False

        self.animation_cooldown = 40 #Cooldown for animation ticks
        self.last_time = pygame.time.get_ticks() #Previous tick time
        
        #Importing animation frames
        self.sprite = []
        self.sprite.append(pygame.image.load('Selected Assets/Player/Idle (1).png'))
        self.sprite.append(pygame.image.load('Selected Assets/Player/Idle (2).png'))
        self.sprite.append(pygame.image.load('Selected Assets/Player/Idle (3).png'))
        self.sprite.append(pygame.image.load('Selected Assets/Player/Idle (4).png'))
        self.sprite.append(pygame.image.load('Selected Assets/Player/Idle (5).png'))
        self.sprite.append(pygame.image.load('Selected Assets/Player/Idle (6).png'))
        self.sprite.append(pygame.image.load('Selected Assets/Player/Idle (7).png'))
        self.sprite.append(pygame.image.load('Selected Assets/Player/Idle (8).png'))
        self.sprite.append(pygame.image.load('Selected Assets/Player/Idle (9).png'))
        self.sprite.append(pygame.image.load('Selected Assets/Player/Idle (10).png'))
        self.sprite.append(pygame.image.load('Selected Assets/Player/Idle (11).png'))
        self.sprite.append(pygame.image.load('Selected Assets/Player/Idle (12).png'))
        self.sprite.append(pygame.image.load('Selected Assets/Player/Idle (13).png'))
        self.sprite.append(pygame.image.load('Selected Assets/Player/Idle (14).png'))
        self.sprite.append(pygame.image.load('Selected Assets/Player/Idle (15).png'))
        self.frame = 0

        self.processImage()

    def processImage(self): #This function updates the frame the animation is on
        self.image = self.sprite[self.frame] #Sets the image to the frame the animation should be on
        self.size = self.image.get_size() #Get the size of the image
        self.scaled_image = pygame.transform.scale(self.image, (int(self.size[0]/4), int(self.size[1]/4))) #Rescale it to 25% of the original size
        self.flipped_image = self.scaled_image
        
        #if self.velX < 0:
        #    self.flipped_image = pygame.transform.flip(self.scaled_image, True, False)
        
        self.rect = self.image.get_rect() #Get the rectangle of the image
        self.rect.center = (self.x, self.y) #Set the top of the rectangle to the given position
    
    def draw(self, screen):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_time >= self.animation_cooldown: #If cooldown is reached
            self.frame += 1 #Go to next frame
            self.last_time = current_time #Set the last time to current time
            if self.frame >= len (self.sprite): #If animation ended repeat it
                self.frame = 0
        self.processImage()
        screen.blit(self.flipped_image, self.rect) #Draw itself onto the screen

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.velX -= 1.00
        if keys[pygame.K_RIGHT]:
            self.velX += 1.00
        if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.velX = 0

        if keys[pygame.K_SPACE]:
            self.velY = -7.5
            self.jumping = True
            print('jumping')   

        self.velY -= self.gravity

        if self.velX >= 5: self.velX = 5
        if self.velX <= -5: self.velX = -5
        if self.velY >= 5 : self.velY = 5

        self.x += self.velX
        self.y += self.velY
        
