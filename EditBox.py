import pygame

class EditBox:
    def __init__(self, game, text, width, height, pos, font_size, id):
        self.game = game
        self.text = text
        self.width = width
        self.height = height
        self.pos = pos

        self.id = f"EditBox_{id}"

        self.color = (255, 255, 255)

        self.selected = False

        self.text_font = pygame.font.Font('Selected Assets/Teko-Regular.ttf', font_size)
        self.rect = pygame.Rect(self.pos, (self.width, self.height))
        self.text_object = self.text_font.render(self.text, True, (0, 0, 0))
        self.text_rect = self.text_object.get_rect()
        self.text_rect.center = self.rect.center 
        self.text_rect.left = self.rect.left + 10

    def draw(self, screen):
        if self.selected: self.color = (128, 128, 128)
        else: self.color = (255, 255, 255)
        
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 3)
        
        screen.blit(self.text_object, self.text_rect)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.selected = True
        else:
            if pygame.mouse.get_pressed()[0]:
                self.selected = False

        self.text_sizew, self.text_sizeh = self.text_font.size(self.text)
        
        if self.selected:
            for event in self.game.events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    elif event.key == pygame.K_RETURN:
                        self.selected = False
                    elif self.text_sizew >= self.width-20: return
                    else:
                        self.text = f'{self.text}{event.unicode}'
                    
                    self.text_object = self.text_font.render(self.text, True, (0, 0, 0))
