from machine import Machine
from settings import *
import ctypes, pygame, sys
from player import Player

ctypes.windll.user32.SetProcessDPIAware()

class Game:
    def __init__(self):         #konstruktor pokrece pygame
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) #  postavlja display window
        pygame.display.set_caption('Slot Machine')
        self.clock = pygame.time.Clock()
        self.close_btn = pygame.image.load(CLOSE_BTN).convert_alpha()
        self.bg_image = pygame.image.load(BG_IMAGE_PATH).convert_alpha()
        self.grid_image = pygame.image.load(GRID_IMAGE_PATH).convert_alpha()        #ucitava slike
        self.machine = Machine()                                                #pokrece masinu
        self.delta_time = 0
        self.running = True                                                     # Flag kontrolise game loop
        
        
        #Zvuk
        main_sound = pygame.mixer.Sound('audio/track.mp3')
        main_sound.play(loops = -1)
        
                
    def check_button_click(self, button_rect, pos):
        # Proverava da li se desio klik u okviru button_rect
        return button_rect.collidepoint(pos)

    def run(self):              #main game loop

        self.start_time = pygame.time.get_ticks()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # proverava da li se desio levi klik
                        mouse_pos = pygame.mouse.get_pos()
                        # Definise oblast Close dugmeta, i proverava da li se klik desio u toj oblasti
                        close_button_rect = self.close_btn.get_rect(topleft=(0, 0))
                        if self.check_button_click(close_button_rect, mouse_pos):
                            pygame.quit()
                            sys.exit()

            self.delta_time = (pygame.time.get_ticks() - self.start_time) / 1000
            self.start_time = pygame.time.get_ticks()

            pygame.display.update()         #screen update - nanovo iscrtava elemente na ekranu. Pozadinu, update masine, grid i close button
            self.screen.blit(self.bg_image, (0, 0))     #crta pozadinu
            self.machine.update(self.delta_time)        #machine update
            self.screen.blit(self.grid_image, (0, 0))   #crta grid
            self.screen.blit(self.close_btn, (0, 0))    #crta close button
            self.clock.tick(FPS)                        #pauzira igru taman toliko da se odrzi Frame rate. 

if __name__ == '__main__':
    game = Game()
    game.run()