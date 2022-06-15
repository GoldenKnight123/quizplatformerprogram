import pygame

class QuestionObject:
    def __init__(self, game, enemyObject):
        self.game = game
        self.id = 'Question'

        self.enemyObject = enemyObject

        self.font = pygame.font.Font(None, 16)

        self.question_view = False

        self.question_data = self.game.gamescreen.questions[0]
        self.game.gamescreen.questions.pop(0)
        print(self.question_data)
        self.question = self.question_data[0]
        self.question_text_surf = self.font.render(self.question, True, (0, 255, 0))
        self.question_text_rect = pygame.Rect((0, 0), (200, 100))
        print(self.question_text_rect)

        self.rect = pygame.Rect((0, 0), (24, 24))
        print(self.rect)

    def renderTextCenteredAt(self, screen, text, font, colour, x, y, allowed_width):
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
    
    def draw(self, screen):
        if not self.question_view:
            pygame.draw.rect(screen, (0, 255, 0), self.rect, 3)
            screen.blit(pygame.font.Font(None, 28).render(' ?', True, (0, 255, 0)), self.rect) #Rendering text surfaces

        elif self.question_view:
            pygame.draw.rect(screen, (0, 0, 0), self.question_text_rect)
            self.renderTextCenteredAt(screen, self.question, self.font, (0, 255, 0), self.enemyObject.rect.centerx, self.enemyObject.rect.centery-100, 190)
    
    def update(self):
        self.rect.center = self.enemyObject.rect.center
        self.question_text_rect.center = self.enemyObject.rect.center
        self.question_text_rect.bottom = self.enemyObject.rect.top

        if self.game.gameState == 'QUESTIONVIEW':
            self.question_view = True
        else:
            self.question_view = False