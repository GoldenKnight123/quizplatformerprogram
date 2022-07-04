import pygame
from tkinter import messagebox

class Bullet:
    def __init__(self, game, player, direction, answer):
        self.game = game
        self.id = 'Bullet'

        self.font = pygame.font.Font('Selected Assets/Teko-Regular.ttf', 16)

        self.direction = direction
        self.player = player
        self.answer = answer

        try:
            self.image = pygame.image.load(f'Selected Assets/Question/{answer}_bullet.png').convert_alpha()

        #On file not found error give popup message that game may crash
        except FileNotFoundError:
            messagebox.showinfo('Error', 'Game files are missing. Game may crash unexpectedly or not display textures.')

        self.rect = self.image.get_rect()
        self.rect.center = player.rect.center

    def draw(self, screen):
        screen.blit(self.image, self.rect)


    def update(self):
        if self.direction == 0:
            self.rect.x += 10
        elif self.direction == 1:
            self.rect.x -= 10

        if self.rect.x <= -30 or self.rect.x >= 1310:
            self.game.gamescreen.gameObjects.remove(self)