import configparser
import datetime
import pygame, time
import sys
import os
from tkinter import messagebox
from BasicEnemy import BasicEnemy
from Buttons import Button
from Player import Player
from MapGenerator import *
from EditBox import EditBox
from QuestionGenerator import QuestionGenerator
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

def settingButtonFunction(game):
    game.gameState = 'SETTING'

def backButtonFunction(game):
    game.gameState = 'MAINMENU'
    config = configparser.RawConfigParser()
    config.read('settings.ini')
    config.set('Volume', 'allsound', game.volume)

    with open('settings.ini', 'w') as settingfile:
                config.write(settingfile)
    
def quitButtonFunction(game):
    pygame.quit()
    sys.exit()

def mainmenuButtonFunction(game):
    game.gameState = 'MAINMENU'
    game.gamescreen.gameObjects.clear()
    game.gamescreen.initObjects()
    game.gamescreen.question_view_timer = 200
    game.gamescreen.distance_travelled = 0
    game.finishscreen.gameObjects.clear()
    game.finishscreen.saved = False

def changeKey(game, key):
    game.keyPressed = False
    game.key = key
    game.gameState = 'KEYCHANGE'

def resetKey(game):
    config = configparser.RawConfigParser()
    config.read('settings.ini')
    config.set('Controls', 'left', pygame.K_LEFT)
    config.set('Controls', 'right', pygame.K_RIGHT)
    config.set('Controls', 'jump', pygame.K_SPACE)
    config.set('Controls', 'shoota', pygame.K_q)
    config.set('Controls', 'shootb', pygame.K_w)
    config.set('Controls', 'shootc', pygame.K_e)
    config.set('Controls', 'shootd', pygame.K_r)
    config.set('Controls', 'timestop', pygame.K_LCTRL)

    try:
        with open('settings.ini', 'w') as settingfile:
                    config.write(settingfile)
    except PermissionError:
        messagebox.showinfo('Warning', 'Permission to modify settings was denied.')

    game.left_key = int(config.get('Controls', 'left'))
    game.right_key = int(config.get('Controls', 'right'))
    game.jump_key = int(config.get('Controls', 'jump'))
    game.shoota_key = int(config.get('Controls', 'shoota'))
    game.shootb_key = int(config.get('Controls', 'shootb'))
    game.shootc_key = int(config.get('Controls', 'shootc'))
    game.shootd_key = int(config.get('Controls', 'shootd'))
    game.timestop_key = int(config.get('Controls', 'timestop'))

def restartFunction(game):
    game.gameState = 'GAME'
    game.gamescreen.gameObjects.clear()
    game.gamescreen.initObjects()
    game.gamescreen.question_view_timer = 200
    game.gamescreen.distance_travelled = 0
    game.restart_sound.play()
    game.finishscreen.gameObjects.clear()
    game.finishscreen.saved = False

def hasNumbers(string):
    return any(i.isdigit() for i in string)

def saveScore(game):
    for i in game.finishscreen.gameObjects:
        if i.id == 'EditBox_name':
            name = i.text
        if i.id == 'EditBox_age':
            age = i.text
    
    if hasNumbers(name):
        messagebox.showinfo('Warning', 'Name should not contain numbers.')
        return

    if name.strip() == '':
        messagebox.showinfo('Warning', 'Please enter a name.')
        return

    try:
        age = int(age.strip())
    except ValueError:
        messagebox.showinfo('Warning', 'Age should only contain numbers.')
        return

    if age < 0:
        messagebox.showinfo('Warning', 'Please enter a valid age.')
        return
    elif age < 8:
        messagebox.showinfo('Warning', 'You are too young to save a score.')
        return
    elif age > 80:
        messagebox.showinfo('Warning', 'You are too old to save a score.')
        return

    file = open("saved_scores.txt", "a")

    file.write(f"{datetime.datetime.now()}: \n")
    file.write(f'{name.strip()} of age {age} travelled {game.gamescreen.distance_travelled} meters! \n\n')
    file.close()

    game.finishscreen.gameObjects.clear()
    game.finishscreen.saved = True
    game.finishscreen.gameObjects.append(Button(game, 'Retry', 200, 60, (640, 550), 15, gui_font, ('#475F77', '#354B5E', '#D74B4B'), restartFunction))
    game.finishscreen.gameObjects.append(Button(game, 'Menu', 200, 60, (640, 650), 15, gui_font, ('#475F77', '#354B5E', '#D74B4B'), mainmenuButtonFunction))

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
        self.gameObjects.append(Button(self.game, 'Settings', 300, 60, (640, 400), 20, gui_font, ('#475F77', '#354B5E', '#D74B4B'), settingButtonFunction))
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

        title_font = pygame.font.Font('Selected Assets/Teko-Regular.ttf', 128)
        screen.blit(title_font.render("Timeless Trivia", True, (0, 0, 0)), (360, 50))

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
        self.distance_travelled = 0

        self.question_view_timer = 200

        self.mapHeight = random.randint(2, 4)

        try:
            self.enemyWalkAnimation = []
            for i in range(15):
                self.enemyWalkAnimation.append(pygame.image.load(f'Selected Assets/Enemy/Walk ({i+1}).png').convert_alpha())

            self.enemyRunAnimation = []
            for i in range(15):
                self.enemyRunAnimation.append(pygame.image.load(f'Selected Assets/Enemy/Run ({i+1}).png').convert_alpha())

            self.enemyJumpAnimation = []
            for i in range(15):
                self.enemyJumpAnimation.append(pygame.image.load(f'Selected Assets/Enemy/Jump ({i+1}).png').convert_alpha())

        #On file not found error give popup message that game may crash
        except FileNotFoundError:
            messagebox.showinfo('Error', 'Game files are missing. Game may crash unexpectedly or not display textures.')

    def initObjects(self):
        self.mapgenerator = MapGenerator(self.game)
        self.questiongenerator = QuestionGenerator(self)
        self.questiongenerator.requestQuestions()
        self.questions = []
        for i in range(50):
            self.questions.append(self.questiongenerator.generateQuestions())
        self.time_bar = pygame.Rect((1050, 5), (200, 30))
        self.time_bar_border = pygame.Rect((1050, 5), (200, 30))

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
        for i in self.mapgenerator.generateMap(40, self.mapHeight, 2):
            self.gameObjects.append(i)
        self.mapHeight = self.mapgenerator.height
        self.gameObjects.append(Player(self.game, (300, 300)))
        for i in range(3):
            self.gameObjects.append(BasicEnemy(self.game, (random.randint(1000, 2000), 100), self.enemyWalkAnimation, self.enemyRunAnimation, self.enemyJumpAnimation))
    
    def draw(self): #Main draw function
        self.screen.blit(self.background_surf, self.background_rect) #Blit (place), the background image onto the screen
        self.screen.blit(self.background_surf2, self.background_rect2) #Blit (place), the background image onto the screen
        for i in self.gameObjects: #Loop each object in list of gameObjects and draw them
            i.draw(self.screen)
         
        if self.game.fading == 'OUT': #Detect when fading state is set to OUT and run the fade function.
            self.fade('OUT')
        elif self.game.fading == 'IN': #Detect when fading state is set to IN and run the fade function.
            self.fade('IN')
        
        travel_text = gui_font.render(f"Distance Travelled: {self.distance_travelled:.2f}m", True, (0, 0, 0))
        screen.blit(travel_text, (10, 25))
        
        self.time_bar.width = self.question_view_timer
        pygame.draw.rect(screen, (128, 128, 128), self.time_bar)
        pygame.draw.rect(screen, (0, 0, 0), self.time_bar_border, 3)

        screen.blit(gui_font.render("Time Energy: ", True, (0, 0, 0)), (930, 0))

        screen.blit(gui_font.render(f"Distance Travelled: {self.distance_travelled:.2f}m", True, (0, 0, 0)), (10, 25))
        
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
                if i.rect.x >= 2560:
                    generate = False
                else:
                    generate = True
        if generate:
            print('new chunk generated')
            for i in self.mapgenerator.generateMap(20, self.mapHeight, 2560):
                self.gameObjects.append(i)
                self.mapHeight = self.mapgenerator.height
    
        for i in self.gameObjects:
            if i.id == 'Enemy':
                enemies_on_screen += 1

        if enemies_on_screen <= 2:
            print('new enemy created')
            self.gameObjects.append(BasicEnemy(self.game, (random.randint(1300, 2000), 300), self.enemyWalkAnimation, self.enemyRunAnimation, self.enemyJumpAnimation))

        if not self.game.gameover:
            self.distance_travelled += (2/64)

        if len(self.questions) <= 0:
            request_font = pygame.font.Font('Selected Assets/Teko-Regular.ttf', 64)
            screen.blit(request_font.render("Retrieving more questions. Please wait.", True, (0, 0, 0)), (200, 200))
            pygame.display.update()
            self.questiongenerator.requestQuestions()
            for i in range(50):
                self.questions.append(self.questiongenerator.generateQuestions())

class FinishScreen:
    def __init__(self, screen, game):
        self.x = 0
        self.y = 0
        self.screen = screen
        self.game = game
        self.gameObjects = []

        self.saved = False

        try:
            self.background_surf = pygame.image.load('Selected Assets/Background.png').convert_alpha() #Load background image
        except FileNotFoundError:
            messagebox.showinfo('Error', 'Game files are missing. Game may crash unexpectedly or not display textures.')

    def initObjects(self):
        #Initialising Game Objects
        self.gameObjects.append(EditBox(self.game, '', 300, 30, (600, 300), 32, 'name'))
        self.gameObjects.append(EditBox(self.game, '', 300, 30, (600, 400), 32, 'age'))
        self.gameObjects.append(Button(self.game, 'Retry', 200, 60, (120, 650), 15, gui_font, ('#475F77', '#354B5E', '#D74B4B'), restartFunction))
        self.gameObjects.append(Button(self.game, 'Save Score', 200, 60, (1160, 650), 15, gui_font, ('#475F77', '#354B5E', '#D74B4B'), saveScore))
        self.gameObjects.append(Button(self.game, 'Menu', 200, 60, (640, 650), 15, gui_font, ('#475F77', '#354B5E', '#D74B4B'), mainmenuButtonFunction))
    
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

        if not self.saved:
            title_font = pygame.font.Font('Selected Assets/Teko-Regular.ttf', 90)
            score_font = pygame.font.Font('Selected Assets/Teko-Regular.ttf', 36)
            screen.blit(title_font.render("Results:", True, (0, 0, 0)), (500, 50))
            screen.blit(score_font.render(f"You travelled {self.game.gamescreen.distance_travelled:.2f} meters!", True, (0, 0, 0)), (500, 150))
            screen.blit(gui_font.render("Name: ", True, (0, 0, 0)), (500, 295))
            screen.blit(gui_font.render("Age: ", True, (0, 0, 0)), (500, 395))

        if self.saved:
            title_font = pygame.font.Font('Selected Assets/Teko-Regular.ttf', 90)
            score_font = pygame.font.Font('Selected Assets/Teko-Regular.ttf', 36)
            screen.blit(title_font.render("Score Saved!", True, (0, 0, 0)), (450, 250))
            screen.blit(score_font.render("Use the 'Retry' button below to try again.", True, (0, 0, 0)), (400, 350))

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

class SettingScreen:
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
        button_font = pygame.font.Font('Selected Assets/Teko-Regular.ttf', 16)
        reset_font = pygame.font.Font('Selected Assets/Teko-Regular.ttf', 24)
        self.gameObjects.append(Button(self.game, 'Back', 200, 40, (120, 650), 13, gui_font, ('#475F77', '#354B5E', '#D74B4B'), backButtonFunction))
        self.gameObjects.append(Button(self.game, 'Change Key', 75, 30, (950, 200), 8, button_font, ('#475F77', '#354B5E', '#D74B4B'), changeKey, 'left'))
        self.gameObjects.append(Button(self.game, 'Change Key', 75, 30, (950, 250), 8, button_font, ('#475F77', '#354B5E', '#D74B4B'), changeKey, 'right'))
        self.gameObjects.append(Button(self.game, 'Change Key', 75, 30, (950, 300), 8, button_font, ('#475F77', '#354B5E', '#D74B4B'), changeKey, 'jump'))
        self.gameObjects.append(Button(self.game, 'Change Key', 75, 30, (950, 350), 8, button_font, ('#475F77', '#354B5E', '#D74B4B'), changeKey, 'shoota'))
        self.gameObjects.append(Button(self.game, 'Change Key', 75, 30, (950, 400), 8, button_font, ('#475F77', '#354B5E', '#D74B4B'), changeKey, 'shootb'))
        self.gameObjects.append(Button(self.game, 'Change Key', 75, 30, (950, 450), 8, button_font, ('#475F77', '#354B5E', '#D74B4B'), changeKey, 'shootc'))
        self.gameObjects.append(Button(self.game, 'Change Key', 75, 30, (950, 500), 8, button_font, ('#475F77', '#354B5E', '#D74B4B'), changeKey, 'shootd'))
        self.gameObjects.append(Button(self.game, 'Change Key', 75, 30, (950, 550), 8, button_font, ('#475F77', '#354B5E', '#D74B4B'), changeKey, 'timestop'))
        self.gameObjects.append(Button(self.game, 'Reset to Default', 150, 60, (800, 600), 8, reset_font, ('#475F77', '#354B5E', '#D74B4B'), resetKey))

        self.volume_rect = pygame.Rect((200, 250), (int(300*self.game.volume), 30))
    
    def draw(self): #Main draw function
        self.screen.blit(self.background_surf, (0, 0)) #Blit (place), the background image onto the screen
        for i in self.gameObjects: #Loop each object in list of gameObjects and draw them
            i.draw(self.screen)
         
        if self.game.fading == 'OUT': #Detect when fading state is set to OUT and run the fade function.
            self.fade('OUT')
        elif self.game.fading == 'IN': #Detect when fading state is set to IN and run the fade function.
            self.fade('IN')
        
        screen.blit(gui_font.render(f"Move Left: {pygame.key.name(self.game.left_key)}", True, (0, 0, 0)), (650, 190))
        screen.blit(gui_font.render(f"Move Right: {pygame.key.name(self.game.right_key)}", True, (0, 0, 0)), (650, 240))
        screen.blit(gui_font.render(f"Jump: {pygame.key.name(self.game.jump_key)}", True, (0, 0, 0)), (650, 290))
        screen.blit(gui_font.render(f"Shoot A: {pygame.key.name(self.game.shoota_key)}", True, (0, 0, 0)), (650, 340))
        screen.blit(gui_font.render(f"Shoot B: {pygame.key.name(self.game.shootb_key)}", True, (0, 0, 0)), (650, 390))
        screen.blit(gui_font.render(f"Shoot C: {pygame.key.name(self.game.shootc_key)}", True, (0, 0, 0)), (650, 440))
        screen.blit(gui_font.render(f"Shoot D: {pygame.key.name(self.game.shootd_key)}", True, (0, 0, 0)), (650, 490))
        screen.blit(gui_font.render(f"Time Stop: {pygame.key.name(self.game.timestop_key)}", True, (0, 0, 0)), (650, 540))
        title_font = pygame.font.Font('Selected Assets/Teko-Regular.ttf', 72)
        screen.blit(title_font.render("Keybinds:", True, (0, 0, 0)), (700, 75))
        screen.blit(title_font.render("Volume:", True, (0, 0, 0)), (200, 75))
        volume_font = pygame.font.Font('Selected Assets/Teko-Regular.ttf', 24)
        screen.blit(volume_font.render(f"Current Volume: {self.game.volume*100:.0f}%", True, (0, 0, 0)), (200, 175))
        pygame.draw.rect(screen, (0, 0, 255), self.volume_rect)

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

        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] >= 190 and mouse_pos[0] <= 510 and mouse_pos[1] >= 250 and mouse_pos[1] <= 280:
            if pygame.mouse.get_pressed()[0]:
                volume = mouse_pos[0]-200
                if volume < 0: volume = 0
                if volume > 300: volume = 300
                self.game.volume = (volume/300)

        self.volume_rect = pygame.Rect((200, 250), (int(300*self.game.volume), 30))


class Game:
    def __init__(self):
        self.mainmenuscreen = MainMenuScreen(screen, self)
        self.gamescreen = GameScreen(screen, self)
        self.settingscreen = SettingScreen(screen, self)
        self.finishscreen = FinishScreen(screen, self)
        self.clock = pygame.time.Clock()
        self.gameState = 'MAINMENU'
        self.gameover = False
        self.fading = 'NONE'
        self.worldShift = -2
        self.circle_radius = 0
        self.gray_surface = pygame.Surface((1280, 720), pygame.SRCALPHA, 32).convert()
        self.gray_surface.set_alpha(100) 
        self.gray_surface.set_colorkey((0, 0, 0))

        #Getting settings:
        try:
            config = configparser.RawConfigParser()
            config.read('settings.ini')
            config.get('Controls', 'left')
        except configparser.NoSectionError:
            config.add_section('Controls')
            config.set('Controls', 'left', pygame.K_LEFT)
            config.set('Controls', 'right', pygame.K_RIGHT)
            config.set('Controls', 'jump', pygame.K_SPACE)
            config.set('Controls', 'shoota', pygame.K_q)
            config.set('Controls', 'shootb', pygame.K_w)
            config.set('Controls', 'shootc', pygame.K_e)
            config.set('Controls', 'shootd', pygame.K_r)
            config.set('Controls', 'timestop', pygame.K_LCTRL)
            config.add_section('Volume')
            config.set('Volume', 'allsound', 1.00)

            with open('settings.ini', 'w') as settingfile:
                config.write(settingfile)

        self.left_key = int(config.get('Controls', 'left'))
        self.right_key = int(config.get('Controls', 'right'))
        self.jump_key = int(config.get('Controls', 'jump'))
        self.shoota_key = int(config.get('Controls', 'shoota'))
        self.shootb_key = int(config.get('Controls', 'shootb'))
        self.shootc_key = int(config.get('Controls', 'shootc'))
        self.shootd_key = int(config.get('Controls', 'shootd'))
        self.timestop_key = int(config.get('Controls', 'timestop'))

        self.volume = float(config.get('Volume', 'allsound'))
        print(self.volume)

        try:
            self.time_stop_sound = pygame.mixer.Sound('Selected Assets/Game Sounds/TimeStop.wav')
            self.clock_tick_sound = pygame.mixer.Sound('Selected Assets/Game Sounds/ClockTick.wav')
            self.time_start_sound = pygame.mixer.Sound('Selected Assets/Game Sounds/TimeStart.wav')
            self.restart_sound = pygame.mixer.Sound('Selected Assets/Game Sounds/Restart.wav')
            self.time_stop_sound.set_volume(self.volume)
            self.clock_tick_sound.set_volume(self.volume)
            self.time_start_sound.set_volume(self.volume)
        
        except FileNotFoundError:
            messagebox.showinfo('Error', 'Game files are missing. Game may crash unexpectedly or not display textures.')

        self.tick_sound_cooldown = 15
    
    def initObjects(self):
        self.gamescreen.initObjects()
        self.mainmenuscreen.initObjects()
        self.settingscreen.initObjects()
    
    def draw(self):
        self.time_stop_sound.set_volume(self.volume)
        self.clock_tick_sound.set_volume(self.volume)
        self.time_start_sound.set_volume(self.volume)
        
        if self.gameState == 'MAINMENU':
            self.mainmenuscreen.draw()
            self.mainmenuscreen.update()
            #print('main drawn')
        elif self.gameState == 'GAME':
            self.gamescreen.draw()
            self.gamescreen.update()
            for event in self.events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.gameState = 'PAUSED'
            #print('game draw')
        elif self.gameState == 'PAUSED':
            self.gamescreen.draw()
            pygame.draw.rect(self.gray_surface, (64, 64, 64), (0, 0, 1280, 720))
            big_font = pygame.font.Font('Selected Assets/Teko-Regular.ttf', 128)
            screen.blit(big_font.render("PAUSED", True, (0, 0, 0)), (480, 100))
            instruction_font = pygame.font.Font('Selected Assets/Teko-Regular.ttf', 36)
            screen.blit(instruction_font.render("Pressed 'escape' to unpause.", True, (0, 0, 0)), (470, 240))
            screen.blit(self.gray_surface, (0, 0))
            for event in self.events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.gameState = 'GAME'
        elif self.gameState == 'SETTING':
            self.settingscreen.draw()
            self.settingscreen.update()
        elif self.gameState == 'QUESTIONVIEW':
            self.gamescreen.draw()
            for i in self.gamescreen.gameObjects:
                if i.id == 'Enemy':
                    i.question_object.draw(screen)
                    i.question_object.update()
        elif self.gameState == 'KEYCHANGE':
            self.settingscreen.draw()
            instruction_font = pygame.font.Font('Selected Assets/Teko-Regular.ttf', 24)
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((440, 310), (400, 100)))
            screen.blit(instruction_font.render("Press the key you want to bind to this action.", True, (0, 255, 0)), (450, 350))
            for event in self.events:
                if event.type == pygame.KEYDOWN:
                    config = configparser.RawConfigParser()
                    config.read('settings.ini')
                    config.set('Controls', self.key, event.key)

                    try:
                        with open('settings.ini', 'w') as settingfile:
                                    config.write(settingfile)
                    except PermissionError:
                        messagebox.showinfo('Warning', 'Permission to modify settings was denied.')

                    self.left_key = int(config.get('Controls', 'left'))
                    self.right_key = int(config.get('Controls', 'right'))
                    self.jump_key = int(config.get('Controls', 'jump'))
                    self.shoota_key = int(config.get('Controls', 'shoota'))
                    self.shootb_key = int(config.get('Controls', 'shootb'))
                    self.shootc_key = int(config.get('Controls', 'shootc'))
                    self.shootd_key = int(config.get('Controls', 'shootd'))
                    self.timestop_key = int(config.get('Controls', 'timestop'))

                    self.gameState = 'SETTING'
        
        elif self.gameState == 'FINISHED':
            self.finishscreen.draw()
            self.finishscreen.update()

            """if not self.keyPressed:
                keys = pygame.key.get_pressed()
                for i in keys:
                    if i:
                        self.keyPressed = True
                        config = configparser.RawConfigParser()
                        config.read('settings.ini')
                        config.set('Controls', self.key, i.key_code())

                        with open('settings.ini', 'w') as settingfile:
                            config.write(settingfile)

                        self.gameState = 'SETTING'"""

        for i in self.gamescreen.gameObjects:
            if i.id == 'Player':
                player_x = i.rect.center[0]
                player_y = i.rect.center[1]
        
        fps_text = gui_font.render(f"FPS: {int(self.clock.get_fps())}", True, (0, 0, 0))
        screen.blit(fps_text, (10, 0))

        keys = pygame.key.get_pressed()

        if keys[self.timestop_key] and self.gameState == 'GAME' and self.gamescreen.question_view_timer > 0 and not self.gameover:
            self.gameState = 'QUESTIONVIEW'
            self.gamescreen.question_view_timer -= 5
            self.time_stop_sound.play()
        elif not keys[self.timestop_key] and self.gameState == 'QUESTIONVIEW':
            self.gameState = 'GAME'
            self.time_start_sound.play()
        elif self.gamescreen.question_view_timer <= 0 and self.gameState == 'QUESTIONVIEW':
            self.gameState = 'GAME'
            self.time_start_sound.play()

        if self.gameState == 'QUESTIONVIEW':
            self.gamescreen.question_view_timer -= 0.25
            if self.tick_sound_cooldown <= 0:
                self.clock_tick_sound.play()
                self.tick_sound_cooldown = 15
            else:
                self.tick_sound_cooldown -= 1
            self.circle_radius += 200
            if self.circle_radius >= 1300: self.circle_radius = 1300
        elif not keys[self.timestop_key] and self.gameState != 'PAUSED':
            self.gamescreen.question_view_timer += 0.25
            if self.gamescreen.question_view_timer > 200:
                self.gamescreen.question_view_timer = 200
            self.circle_radius -= 200
            if self.circle_radius <= 0: self.circle_radius = 0
        else:
            self.circle_radius -= 100
            if self.circle_radius <= 0: self.circle_radius = 0
        
        self.gray_surface.fill((0, 0, 0))
        pygame.draw.circle(self.gray_surface, (128, 128, 128), (player_x, player_y), self.circle_radius)
        screen.blit(self.gray_surface, (0, 0))

        if self.gameover:
            screen.blit(gameover_font.render("GAME OVER!", True, (0, 0, 0)), (380, 130))
            screen.blit(gui_font.render(f"You travelled {self.gamescreen.distance_travelled:.2f} meters!", True, (0, 0, 0)), (520, 300))
            screen.blit(restart_font.render("""Press any key to continue.""", True, (0, 0, 0)), (550, 350))
            for event in self.events:
                if event.type == pygame.KEYDOWN:
                    self.gameState = 'FINISHED'
                    self.finishscreen.initObjects()
                    self.gameover = False

        if self.gameState == 'QUESTIONVIEW':
            for i in self.gamescreen.gameObjects:
                if i.id == 'Enemy':
                    i.question_object.draw(screen)
                    i.question_object.update()
        
        self.clock.tick(60)
        pygame.display.update()
    
    def run(self):
        while True:
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT:
                    return

            self.draw()

initiate()
gui_font = pygame.font.Font('Selected Assets/Teko-Regular.ttf', 30)
gameover_font = pygame.font.Font('Selected Assets/Teko-Regular.ttf', 144)
restart_font = pygame.font.Font('Selected Assets/Teko-Regular.ttf', 24)
game = Game()
game.initObjects()
game.run()