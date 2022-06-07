import pygame
import random

class MapGenerator:
    def __init__(self, game):
        self.game = game

    def generateMap(self, size):
        self.size = size
        self.x = 0
        self.height = random.randint(2, 5)
        self.heightChange = random.randint(5, 10)
        self.tileList = []
        for a in range(self.size):
            self.tileList.append(FloorTile(self.game, (self.x+(a*64), 720-64*self.height), 'GrassMid'))
            for b in range(self.height):
                self.tileList.append(FloorTile(self.game, (self.x+(a*64), 720-64*(self.height-b-1)), 'DirtMid'))
            self.heightChange -= 1
            if self.heightChange <= 0:
                if self.height <= 1: self.height += 1
                if self.height >= 7: self.height -= 1

                self.height -= random.choice([-1, 1])
                self.heightChange = random.randint(5, 10)

        #Old generation code    
        """for a in range(self.height):
            for b in range(size):
                self.tileList.append(FloorTile(self.game, (self.x+(b*64), 720-64*a), 'DirtMid'))

        for b in range(size):
                self.tileList.append(FloorTile(self.game, (self.x+(b*64), 720-64*self.height), 'GrassMid'))"""

        return self.tileList

class FloorTile:
    def __init__(self, game, pos, type):
        self.game = game
        self.id = 'Floor'

        self.type = type

        self.image = pygame.image.load(f'Selected Assets/Tiles/{self.type}.png').convert()
        
        """if self.type == 'GrassLeft': self.image = pygame.image.load('Selected Assets/Tiles/GrassLeft.png').convert()
        elif self.type == 'GrassMid': self.image = pygame.image.load('Selected Assets/Tiles/GrassMid.png').convert()
        elif self.type == 'GrassRight': self.image = pygame.image.load('Selected Assets/Tiles/GrassRight.png').convert()
        elif self.type == 'DirtLeft': self.image = pygame.image.load('Selected Assets/Tiles/DirtLeft.png').convert()
        elif self.type == 'DirtMid': self.image = pygame.image.load('Selected Assets/Tiles/Dirt.png').convert()
        elif self.type == 'DirtRight': self.image = pygame.image.load('Selected Assets/Tiles/DirtRight.png').convert()"""
        
        self.x = pos[0]
        self.y = pos[1]

        self.size = self.image.get_size()
        self.scaled_image = pygame.transform.scale(self.image, (int(self.size[0]/2), int(self.size[1]/2)))
    
        self.rect = self.scaled_image.get_rect()
        self.rect.topleft = (pos)


    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.rect) #For debugging purposes and seeing hitboxes
        screen.blit(self.scaled_image, self.rect)

    def update(self):
        return