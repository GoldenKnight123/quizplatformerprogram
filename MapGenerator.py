import pygame
import random
from tkinter import messagebox

class MapGenerator:
    def __init__(self, game):
        self.game = game

    def generateMap(self, size, height, shiftx):
        self.size = size
        self.x = shiftx
        self.height = height
        self.heightChange = random.randint(10, 15)
        self.tileList = []
        for a in range(self.size):
            self.tileList.append(FloorTile(self.game, (self.x+(a*64), 720-64*self.height), 'GrassMid'))
            for b in range(self.height):
                self.tileList.append(FloorTile(self.game, (self.x+(a*64), 720-64*(self.height-b-1)), 'DirtMid'))
            self.heightChange -= 1
            if self.heightChange <= 0:
                if self.height <= 1: self.height += 1
                elif self.height >= 6: self.height -= 1
                else:
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

        try:
            self.image = pygame.image.load(f'Selected Assets/Tiles/{self.type}.png').convert()
        except FileNotFoundError:
            messagebox.showinfo('Error', 'Game files are missing. Game may crash unexpectedly or not display textures.')
        
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
        if self.rect.x <= -64:
            self.game.gamescreen.gameObjects.remove(self)