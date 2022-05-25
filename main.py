import pygame, time
from enum import Enum

def initiate():
    pygame.init()

screen = pygame.display.set_mode([640, 480])

running = True

class gameState(Enum):
    MAINMENU = 'mainMenu'
    GAME = 'game'
    PAUSED = 'paused'
    OPTIONMENU = 'optionMenu'

class MainMenuScreen:
    def __init__(self, screen):
        self.x = 0
        self.y = 0
        self.screen = screen

    def draw(self):
        self.screen.fill((0, 0, 255))
        #Draw all start up elements here
        
    def update(self, game):
        self.screen.fill((0, 0, 255))
        pygame.display.update()

class GameScreen:
    def __init__(self, screen):
        self.x = 0
        self.y = 0
        self.screen = screen

    def draw(self):
        self.screen.fill((0, 255, 0))
        #Draw all start up elements here
        
    def update(self, game):
        self.screen.fill((0, 255, 0))
        pygame.display.update()

class Game:
    def __init__(self, mainmenuscreen, gamescreen):
        self.mainmenuscreen = mainmenuscreen
        self.gamescreen = gamescreen
        self.clock = pygame.time.Clock()
        self.gameState = gameState.MAINMENU

    def run(self):
        self.mainmenuscreen.draw()
        self.gamescreen.draw()
        self.timer = 0
        while True:
            dt = self.clock.tick(60)
            self.timer += 1
            if self.timer > 100:
                self.timer = 0
                print('tick')
                self.gameState = gameState.GAME
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            if self.gameState == gameState.MAINMENU:
                self.mainmenuscreen.update(self)
                print("MAINMENU")
            elif self.gameState == gameState.GAME:
                self.gamescreen.update(self)
                print("GAME")

initiate()
gui_font = pygame.font.Font(None, 30)
game = Game(MainMenuScreen(screen), GameScreen(screen))
game.run()