import pygame
from tkinter import messagebox

class QuestionObject:
    def __init__(self, game, enemyObject):
        self.game = game
        self.id = 'Question'

        self.enemyObject = enemyObject

        self.font = pygame.font.Font('Selected Assets/Teko-Regular.ttf', 16)

        self.question_view = False

        self.question_data = self.game.gamescreen.questions[0]
        self.game.gamescreen.questions.pop(0)

        self.question = self.question_data[0]
        self.question_text_surf = self.font.render(self.question, True, (0, 255, 0))
        self.question_text_rect = pygame.Rect((0, 0), (200, 150))

        self.answers = self.question_data[2]
        self.answer = self.question_data[1]

        try:
            self.image = pygame.image.load('Selected Assets/Question/question_block.png').convert_alpha()

        #On file not found error give popup message that game may crash
        except FileNotFoundError:
            messagebox.showinfo('Error', 'Game files are missing. Game may crash unexpectedly or not display textures.')
        
        self.rect = self.image.get_rect()
        self.rect.center = (-100, -100)

        #Attempt to load sound files
        try:
            self.correct_sound = pygame.mixer.Sound('Selected Assets/Game Sounds/EnemyKill.wav')
            self.wrong_sound = pygame.mixer.Sound('Selected Assets/Game Sounds/WrongAnswer.wav')
            self.correct_sound.set_volume(self.game.volume)
            self.wrong_sound.set_volume(self.game.volume)
        
        #On file not found error give popup message that game may crash
        except FileNotFoundError:
            messagebox.showinfo('Error', 'Game files are missing. Game may crash unexpectedly or not display textures.')

    def renderQuestion(self, screen, text, font, colour, x, y, allowed_width):
        words = text.split() #Split full question into words

        lines = [] #Creates lines of words that fit the width
        while len(words) > 0: #While there are still words left
            line_words = [] 
            while len(words) > 0:
                line_words.append(words.pop(0)) #Add the word to the line and remove it from the list
                fw, fh = font.size(' '.join(line_words + words[:1])) #Find the size of the line
                if fw > allowed_width: #If it exceeds the width limit
                    break #Stop and move onto next line

            line = ' '.join(line_words) #Create the line with spaces
            lines.append(line) #Add the line to lines

        #Rendering each of the lines
        y_offset = 0 #Off set of the lines as it shifts down
        for line in lines:
            fw, fh = font.size(line) #find the width of the line

            #(tx, ty) is the top-left of the font surface
            tx = x - fw / 2 #Center the text
            ty = y + y_offset #Move the text down by the required amount

            text_surface = font.render(line, True, colour) #Creating the text surface
            screen.blit(text_surface, (tx, ty)) #Draw it onto the correct position

            y_offset += fh #Added y offset so lines move down

        return y_offset
    
    def renderAnswers(self, screen, answers, font, colour, x, y, allowed_width):
        words_1 = ["A)"] + answers[0].split()
        words_2 = ["B)"] + answers[1].split()
        words_3 = ["C)"] + answers[2].split()
        words_4 = ["D)"] + answers[3].split()

        combined_words = []
        combined_words.append(words_1)
        combined_words.append(words_2)
        combined_words.append(words_3)
        combined_words.append(words_4)

        y_offset = 0 #Off set of the lines as it shifts down

        for i in combined_words:
            lines = [] #Creates lines of words that fit the width
            while len(i) > 0: #While there are still words left
                line_words = [] 
                while len(i) > 0:
                    line_words.append(i.pop(0)) #Add the word to the line and remove it from the list
                    fw, fh = font.size(' '.join(line_words + i[:1])) #Find the size of the line
                    if fw > allowed_width: #If it exceeds the width limit
                        break #Stop and move onto next line

                line = ' '.join(line_words) #Create the line with spaces
                lines.append(line) #Add the line to lines
                
            #Rendering each of the lines
            for line in lines:
                fw, fh = font.size(line) #find the width of the line

                #(tx, ty) is the top-left of the font surface
                tx = x - 75 #Center the text
                ty = y + y_offset #Move the text down by the required amount

                text_surface = font.render(line, True, colour) #Creating the text surface
                screen.blit(text_surface, (tx, ty)) #Draw it onto the correct position

                y_offset += fh + 5 #Added y offset so lines move down

        return y_offset

    def draw(self, screen):
        if not self.game.gameState == 'QUESTIONVIEW':
            screen.blit(self.image, self.rect)

        elif self.game.gameState == 'QUESTIONVIEW':
            pygame.draw.rect(screen, (0, 0, 0), self.question_text_rect)
            y_1 = self.renderQuestion(screen, self.question, self.font, (0, 255, 0), self.enemyObject.rect.centerx, self.question_text_rect.y+5, 190)
            y_2 = self.renderAnswers(screen, self.answers, self.font, (0, 255, 0), self.enemyObject.rect.centerx, self.question_text_rect.y+y_1+40, 190)
            self.question_text_rect.height = y_1 + y_2 + 40
    
    def update(self):
        self.correct_sound.set_volume(self.game.volume)
        self.wrong_sound.set_volume(self.game.volume)
        
        self.rect.center = self.enemyObject.rect.center
        self.rect.top -= 50
        self.question_text_rect.center = self.enemyObject.rect.center
        self.question_text_rect.bottom = self.enemyObject.rect.top

        for i in self.game.gamescreen.gameObjects: #Loop through all game objects on the screen
            if i.id == 'Player': 
                player_object = i

        for i in self.game.gamescreen.gameObjects: #Loop through all game objects on the screen
            if i.id == 'Bullet': 
                if i.rect.colliderect(self.enemyObject.rect): 
                    if i.answer == self.answers.index(self.answer)+1:
                        self.game.gamescreen.gameObjects.remove(i)
                        self.game.gamescreen.gameObjects.remove(self.enemyObject)
                        player_object.shoot_cooldown = 0
                        self.game.gamescreen.question_view_timer += 20
                        self.correct_sound.play()
                    else:
                        self.game.gamescreen.gameObjects.remove(i)
                        player_object.shoot_cooldown = 100
                        self.enemyObject.player_chase = True
                        self.wrong_sound.play()

        mouse_pos = pygame.mouse.get_pos() #Get mouse position
        if self.enemyObject.rect.collidepoint(mouse_pos) and self.game.gameState == 'QUESTIONVIEW' and pygame.mouse.get_pressed()[0]:
            self.game.gamescreen.gameObjects.append(self.game.gamescreen.gameObjects.pop(self.game.gamescreen.gameObjects.index(self.enemyObject)))