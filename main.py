from QuestionGenerator import QuestionGenerator
import pygame, time
import sys
from tkinter import messagebox
from BasicEnemy import BasicEnemy
from Buttons import Button
from Player import Player
from MapGenerator import *
import random

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

    def initObjects(self):
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
        
        #if self.game.fading != 'RUNNING': #If fade is running we do need not need to update the screen an extra time
        #    pygame.display.update()

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

        self.question_view_timer = 200

        self.mapHeight = random.randint(2, 4)

    def initObjects(self):
        self.mapgenerator = MapGenerator(self.game)
        self.questiongenerator = QuestionGenerator(self)
        self.questions = []
        for i in range(10):
            self.questions.append(self.questiongenerator.generateQuestions())
        print(self.questions)
        self.time_bar = pygame.Rect((1000, 5), (self.question_view_timer, 30))

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
        for i in range(3):
            self.gameObjects.append(BasicEnemy(self.game, (random.randint(1000, 3000), 300)))
    
    def draw(self): #Main draw function
        self.screen.blit(self.background_surf, self.background_rect) #Blit (place), the background image onto the screen
        self.screen.blit(self.background_surf2, self.background_rect2) #Blit (place), the background image onto the screen
        for i in self.gameObjects: #Loop each object in list of gameObjects and draw them
            i.draw(self.screen)
         
        if self.game.fading == 'OUT': #Detect when fading state is set to OUT and run the fade function.
            self.fade('OUT')
        elif self.game.fading == 'IN': #Detect when fading state is set to IN and run the fade function.
            self.fade('IN')
        
        self.time_bar.width = self.question_view_timer
        pygame.draw.rect(screen, (0, 0, 0), self.time_bar)
        
        #if self.game.fading != 'RUNNING': #If fade is running we do need not need to update the screen an extra time
        #    pygame.display.update()

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
        enemies_on_screen = 0
        for i in self.gameObjects:
            if i.id == 'Floor':
                if i.rect.x >= 1280:
                    generate = False
                else:
                    generate = True
        if generate:
            print('new chunk generated')
            for i in self.mapgenerator.generateMap(20, self.mapHeight, 1280):
                self.gameObjects.append(i)
                self.mapHeight = self.mapgenerator.height
    
        for i in self.gameObjects:
            if i.id == 'Enemy':
                enemies_on_screen += 1

        if enemies_on_screen <= 2:
            print('new enemy created')
            self.gameObjects.append(BasicEnemy(self.game, (random.randint(1300, 2000), 300)))

class Game:
    def __init__(self):
        self.mainmenuscreen = MainMenuScreen(screen, self)
        self.gamescreen = GameScreen(screen, self)
        self.clock = pygame.time.Clock()
        self.gameState = 'MAINMENU'
        self.fading = 'NONE'
        self.worldShift = -2
        self.circle_radius = 0
        self.gray_surface = pygame.Surface((1280, 720), pygame.SRCALPHA, 32).convert()
        self.gray_surface.set_alpha(100) 
        self.gray_surface.set_colorkey((0, 0, 0))

        try:
            self.time_stop_sound = pygame.mixer.Sound('Selected Assets/Game Sounds/TimeStop.wav')
            self.clock_tick_sound = pygame.mixer.Sound('Selected Assets/Game Sounds/ClockTick.wav')
            self.time_start_sound = pygame.mixer.Sound('Selected Assets/Game Sounds/TimeStart.wav')
            self.time_stop_sound.set_volume(0.25)
            self.clock_tick_sound.set_volume(0.25)
            self.time_start_sound.set_volume(0.25)
        
        except FileNotFoundError:
            messagebox.showinfo('Error', 'Game files are missing. Game may crash unexpectedly or not display textures.')

        self.tick_sound_cooldown = 15

    def initObjects(self):
        self.gamescreen.initObjects()
        self.mainmenuscreen.initObjects()
    
    def draw(self):
        if self.gameState == 'MAINMENU':
            self.mainmenuscreen.draw()
            self.mainmenuscreen.update()
            #print('main drawn')
        elif self.gameState == 'GAME':
            self.gamescreen.draw()
            self.gamescreen.update()
            #print('game draw')
        elif self.gameState == 'QUESTIONVIEW':
            self.gamescreen.draw()
            for i in self.gamescreen.gameObjects:
                if i.id == 'Enemy':
                    i.question_object.draw(screen)
                    i.question_object.update()

        fps_text = gui_font.render(f"FPS: {int(self.clock.get_fps())}", True, (0, 0, 0))
        screen.blit(fps_text, (10, 5))

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LCTRL] and self.gameState == 'GAME' and self.gamescreen.question_view_timer > 0:
            self.gameState = 'QUESTIONVIEW'
            self.time_stop_sound.play()
        elif not keys[pygame.K_LCTRL] and self.gameState == 'QUESTIONVIEW':
            self.gameState = 'GAME'
            self.time_start_sound.play()
        elif self.gamescreen.question_view_timer <= 0 and self.gameState == 'QUESTIONVIEW':
            self.gameState = 'GAME'
            self.time_start_sound.play()

        if self.gameState == 'QUESTIONVIEW':
            self.gamescreen.question_view_timer -= 0.5
            if self.tick_sound_cooldown <= 0:
                self.clock_tick_sound.play()
                self.tick_sound_cooldown = 15
            else:
                self.tick_sound_cooldown -= 1
            self.circle_radius += 200
            if self.circle_radius >= 1300: self.circle_radius = 1300
        elif not keys[pygame.K_LCTRL]:
            self.gamescreen.question_view_timer += 0.25
            if self.gamescreen.question_view_timer > 200:
                self.gamescreen.question_view_timer = 200
            self.circle_radius -= 200
            if self.circle_radius <= 0: self.circle_radius = 0
        else:
            self.circle_radius -= 100
            if self.circle_radius <= 0: self.circle_radius = 0

        for i in self.gamescreen.gameObjects:
                if i.id == 'Player':
                    player_x = i.rect.center[0]
                    player_y = i.rect.center[1]
        
        self.gray_surface.fill((0, 0, 0))
        pygame.draw.circle(self.gray_surface, (128, 128, 128), (player_x, player_y), self.circle_radius)
        screen.blit(self.gray_surface, (0, 0))
        
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
game.initObjects()
game.run()