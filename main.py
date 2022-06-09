import pygame, time
import sys
from tkinter import messagebox
from Buttons import Button
from Player import Player
from MapGenerator import *

def initiate():
    pygame.init()

screen = pygame.display.set_mode([1280, 720], pygame.DOUBLEBUF, 8)

running = True 

def startButtonFunction(game):
    game.fading = 'OUT'
    game.mainmenuscreen.draw()

    game.gameState = 'GAME'

    game.fading = 'IN'
    game.gamescreen.draw()
    
def quitButtonFunction(game):
    running = False
    pygame.quit()
    sys.exit()

class MainMenuScreen:
    def __init__(self, screen, game):
        self.x = 0
        self.y = 0
        self.screen = screen
        self.game = game
        self.gameObjects = []

        try:
            self.background_surf = pygame.image.load('Selected Assets/Background.png').convert_alpha() #Load background image
        except FileNotFoundError:
            messagebox.showinfo('Error', 'Game files are missing. Game may crash unexpectedly or not display textures.')

        #Initialising Game Objects
        self.gameObjects.append(Button(self.game, 'Start', 300, 60, (640, 300), 20, gui_font, ('#475F77', '#354B5E', '#D74B4B'), startButtonFunction))
        self.gameObjects.append(Button(self.game, 'Quit', 300, 60, (640, 500), 20, gui_font, ('#475F77', '#354B5E', '#D74B4B'), quitButtonFunction))

    def draw(self): #Main draw function
        self.screen.blit(self.background_surf, (0, 0)) #Blit (place), the background image onto the screen
        for i in self.gameObjects: #Loop each object in list of gameObjects and draw them
            i.draw(self.screen)
         
        if self.game.fading == 'OUT': #Detect when fading state is set to OUT and run the fade function.
            self.fade('OUT')
        elif self.game.fading == 'IN': #Detect when fading state is set to IN and run the fade function.
            self.fade('IN')
        
        if self.game.fading != 'RUNNING': #If fade is running we do need not need to update the screen an extra time
            pygame.display.update()

    def fade(self, mode): #Transition function for fade effect
        fade = pygame.Surface((1280, 720)) #Creating new surface that covers screen
        fade.fill((0, 0, 0)) #Fill it black
        self.game.fading = 'RUNNING' #Set fading state to RUNNING so game main draw function new longer updates display
        for alpha in range(0, 51): #Loop for each alpha level
            if mode == 'OUT': fade.set_alpha(alpha*5) #Fade out mode: black becomes strongers over time
            elif mode == 'IN': fade.set_alpha(255-alpha*5) #Fade in mode: black becomes weaker over time
            self.draw() #Run the main draw function of the screen to keep objects on screen
            self.screen.blit(fade, (0, 0)) #Draw fade surface on screen
            pygame.display.update() #Update display
            pygame.time.delay(5) #Delay so it does not all run at once and creates a slow fade effect
        self.game.fading = 'NONE' #Reset fading state to NONE
        
    def update(self):
        for i in self.gameObjects:
            i.update()
        
class GameScreen:
    def __init__(self, screen, game):
        self.x = 0
        self.y = 0
        self.screen = screen
        self.game = game
        self.gameObjects = []

        self.mapHeight = random.randint(2, 4)

        self.mapgenerator = MapGenerator(self.game)

        try:
            self.background_surf = pygame.image.load('Selected Assets/Background.png').convert_alpha() #Load background image
            self.background_rect = self.background_surf.get_rect()
            self.background_rect.topleft = (0, 0)
            self.background_surf2 = pygame.image.load('Selected Assets/Background.png').convert_alpha() #Load background image
            self.background_rect2 = self.background_surf2.get_rect()
            self.background_rect2.topleft = (1280, 0)
        except FileNotFoundError:
            messagebox.showinfo('Error', 'Game files are missing. Game may crash unexpectedly or not display textures.')

        #Initialising Game Objects
        for i in self.mapgenerator.generateMap(20, self.mapHeight, 2):
            self.gameObjects.append(i)
        self.mapHeight = self.mapgenerator.height
        self.gameObjects.append(Player(self.game, (300, 300)))

    def draw(self): #Main draw function
        self.screen.blit(self.background_surf, self.background_rect) #Blit (place), the background image onto the screen
        self.screen.blit(self.background_surf2, self.background_rect2) #Blit (place), the background image onto the screen
        for i in self.gameObjects: #Loop each object in list of gameObjects and draw them
            i.draw(self.screen)
         
        if self.game.fading == 'OUT': #Detect when fading state is set to OUT and run the fade function.
            self.fade('OUT')
        elif self.game.fading == 'IN': #Detect when fading state is set to IN and run the fade function.
            self.fade('IN')
        
        if self.game.fading != 'RUNNING': #If fade is running we do need not need to update the screen an extra time
            pygame.display.update()

    def fade(self, mode): #Transition function for fade effect
        fade = pygame.Surface((1280, 720)) #Creating new surface that covers screen
        fade.fill((0, 0, 0)) #Fill it black
        self.game.fading = 'RUNNING' #Set fading state to RUNNING so game main draw function new longer updates display
        for alpha in range(0, 51): #Loop for each alpha level
            if mode == 'OUT': fade.set_alpha(alpha*5) #Fade out mode: black becomes strongers over time
            elif mode == 'IN': fade.set_alpha(255-alpha*5) #Fade in mode: black becomes weaker over time
            self.draw() #Run the main draw function of the screen to keep objects on screen
            self.screen.blit(fade, (0, 0)) #Draw fade surface on screen
            pygame.display.update() #Update display
            pygame.time.delay(5) #Delay so it does not all run at once and creates a slow fade effect
        self.game.fading = 'NONE' #Reset fading state to NONE
        
    def update(self):
        for i in self.gameObjects:
            i.update()
            i.rect.x += game.worldShift
        self.background_rect.x += game.worldShift/2
        self.background_rect2.x += game.worldShift/2
        if self.background_rect.x <= -1280:
            self.background_rect.x += 2560
        if self.background_rect2.x <= -1280:
            self.background_rect2.x += 2560
        for i in self.gameObjects:
            if i.rect.x >= 1280:
                generate = False
            else:
                generate = True
        if generate:
            print('new chunk generated')
            for i in self.mapgenerator.generateMap(20, self.mapHeight, 1280):
                self.gameObjects.append(i)
                self.mapHeight = self.mapgenerator.height

class Game:
    def __init__(self):
        self.mainmenuscreen = MainMenuScreen(screen, self)
        self.gamescreen = GameScreen(screen, self)
        self.clock = pygame.time.Clock()
        self.gameState = 'MAINMENU'
        self.fading = 'NONE'
        self.worldShift = -2

    def cutSprite(self, spriteSheet, width, height, frame):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(spriteSheet, (0, 0), ((frame*width), 0, width, height))
        image.set_colorkey((0, 0, 0))
        
        return image

    def draw(self):
        
        if self.gameState == 'MAINMENU':
            self.mainmenuscreen.draw()
            self.mainmenuscreen.update()
            #print('main drawn')
        elif self.gameState == 'GAME':
            self.gamescreen.draw()
            self.gamescreen.update()
            #print('game draw')

        fps_text = gui_font.render(f"FPS: {int(self.clock.get_fps())}", True, (0, 0, 0))
        screen.blit(fps_text, (10, 5))
        
        self.clock.tick(60)
        pygame.display.update()
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            self.draw()

initiate()
gui_font = pygame.font.Font(None, 30)
game = Game()
game.run()