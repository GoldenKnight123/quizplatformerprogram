import pygame

class Button():
    def __init__(self, game, text, width, height, pos, elevation, gui_font, colors, function):
        self.game = game #importing game so it can modify crucial variables

        self.function = function

        self.pressed = False #Pressed state, prevents buttons from activating multiple times in one click
        self.elevation = elevation #The fixed elevation for the top rect
        self.dynamic_elevation = elevation #The changable elevation for the top rect, sets to 0 when clicked to create clicking effect
        self.origin_y_pos = pos[1] #The initial y position of button, shifted up by elevation when drawn

        self.colors = colors #Lists of colors (0 = Top Rect, 1 = Bottom Rect, 2 = Hover Top Rect)
        
        self.top_rect = pygame.Rect(pos, (width, height)) #Top rectangle of the bottom, this is the one that changes color and moves when interacted with
        self.top_color = self.colors[0] #Color of top rectangle

        self.bottom_rect = pygame.Rect(pos, (width, elevation)) #Bottom rectangle, does not move, stationary.
        self.bottom_color = self.colors[1] #Color of bottom rectangle

        self.text_surf = gui_font.render(text, True, '#FFFFFF') #Text surface
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center) #Text rectangle

        self.top_rect.center = pos #Setting position of the button as the center

    def draw(self, screen):
        self.top_rect.y = self.origin_y_pos - self.dynamic_elevation #Setting the y of top rect by elevation amount
        self.text_rect.center = self.top_rect.center #Centering the text with the top rect

        self.bottom_rect.midtop = self.top_rect.midtop #Matching the poition of bottom rect with top rect
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation #Adding height to the bottom rect to create 3d effect
        
        pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=12)
        screen.blit(self.text_surf, self.text_rect) #Rendering text surfaces

    def update(self):
        mouse_pos = pygame.mouse.get_pos() #Get mouse position
        if self.top_rect.collidepoint(mouse_pos): #If mouse if over button
            self.top_color = self.colors[2] #Change color
            if pygame.mouse.get_pressed()[0]: #If left key is pressed
                self.dynamic_elevation = 0 #Set elevation back to 0 making the top rect move down to the bottom rect creaing a 3d effect
                self.pressed = True #Pressed boolean to prevent multiple iterations of the click loop running in one click
            else:
                self.dynamic_elevation = self.elevation #Set elevation back when key is released
                if self.pressed == True:
                    self.function(self.game) #Run the assigned function with main game as the parameter
                    self.pressed = False

        else:
            self.dynamic_elevation = self.elevation #Set elevation back when mouse is no longer hovering over button
            self.top_color = self.colors[0] #Change color backs
