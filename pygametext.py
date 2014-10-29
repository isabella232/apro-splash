import os, sys
import pygame
from pygame.locals import *

import TextWidget

class PyGameText:
    """An example class used to illustrate possible ways to work
    with the TextWidget text in a pygame game.
    """
    
    def __init__(self, width=800, height=480):
        """Initialize
        @param width=640 - The width of the pygame window
        @param height=480 - The height of the pygame window.
        """
        
        pygame.init()
        #create the screen
        self.screen = pygame.display.set_mode((width, height), 0) 
        self.background = pygame.Surface(self.screen.get_size(), SWSURFACE)
        self.background = self.background.convert()
        image, rect = self.load_image("background.jpg")
        if (image):
            self.background.blit(image, (0,0))
        else:
            #Just fill with a solid colour
            self.background.fill((124,124,124))
        self.screen.blit(self.background, (0,0))
        
    def main_loop(self):
        """The main Python loop"""
        
        pygame.display.update()
        self.timer = pygame.time.Clock()
        
        # Text Widget list
        self.text_widgets = []
        #Create our Text WIdgets
        self.new_game_text = TextWidget.TextWidget("Q&A Demo", (255,255,255))
        #make this the biggest text
        self.new_game_text.size = 96
        self.new_game_text.rect.center = self.screen.get_rect().center
        self.new_game_text.rect.top = 0;
        self.text_widgets.append(self.new_game_text)
        
        self.high_score_text = TextWidget.TextWidget("Video Demo", (255,255,255), 64)
        self.high_score_text.rect.center = self.screen.get_rect().center
        self.high_score_text.rect.top = self.new_game_text.rect.bottom + 30
        self.text_widgets.append(self.high_score_text)
        
        self.website_text = TextWidget.TextWidget("Website", (255,255,255), 64)
        self.website_text.rect.center = self.screen.get_rect().center
        self.website_text.rect.top = self.high_score_text.rect.bottom + 30
        self.text_widgets.append(self.website_text)
        
        # Different font for the last one, and let's make it increase
        # more
        self.exit_text = TextWidget.TextWidget("Exit", (255,255,255)
                                , 64, 40
                                , pygame.font.match_font("sans", False, True))
        self.exit_text.rect.center = self.screen.get_rect().center
        self.exit_text.rect.top = self.website_text.rect.bottom + 30
        # override the on_mouse_click event
        self.exit_text.on_mouse_click = self.on_exit_clicked
        self.text_widgets.append(self.exit_text)
           
        while 1: 
            #Tick of the timer
            self.timer.tick()
            self.event_loop()
            self.draw()
                
    def event_loop(self):
        """Perform the event loop."""
        
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                sys.exit()
            elif (event.type == ACTIVEEVENT):
                if (event.gain == 1):
                    for text in self.text_widgets:
                        text.dirty = True
                    self.draw()
                elif (event.state ==2): 
                    #We are hidden so wait for the next event
                    pygame.event.post(pygame.event.wait())             
            elif (event.type == pygame.MOUSEMOTION):
                for text in self.text_widgets:
                    text.highlight = text.rect.collidepoint(event.pos)
            elif (event.type == pygame.MOUSEBUTTONDOWN):
                for text in self.text_widgets:
                    text.on_mouse_button_down(event)
            elif (event.type == pygame.MOUSEBUTTONUP):
                for text in self.text_widgets:
                    text.on_mouse_button_up(event)
            elif (event.type == TextWidget.TEXT_WIDGET_CLICK):
                print event.text_widget              
    
    def draw(self):
        """Draw everything"""        
        rects = []
        rects.append(self.timer_update())
        for text in self.text_widgets:
            rect = text.draw(self.screen)
            if (rect):
                rects.append(rect)
        pygame.display.update(rects)        
        
    def timer_update(self):
        """Update the Timer
        returns - pygame.rect - The rect that the timer
        needs to be redrawn, or None on error"""
        
        rect_return = None
        
        if (pygame.font):     
            timer_string = "%.2f" % self.timer.get_fps()
            #basic font
            font = pygame.font.Font(None, 36)
            message = font.render(timer_string, 1, (147, 1, 16))
            if (message):
                rect_return = message.get_rect(left=0)
                rect_return.width += 25
                self.screen.blit(self.background, rect_return)
                self.screen.blit(message, rect_return) 
        
        return rect_return
    
    def load_image(self, name, colorkey=None):
        full_path = os.path.realpath(os.path.dirname(sys.argv[0]))
        full_path = os.path.join(full_path, name)
        try:
            image = pygame.image.load(full_path)
        except pygame.error, message:
            print 'Cannot load image:', full_path
            return None, None
        image = image.convert()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, RLEACCEL)
        return image, image.get_rect()
    
    def on_exit_clicked(self, event):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    text = PyGameText()
    text.main_loop()
