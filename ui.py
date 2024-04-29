from player import Player
from settings import *
import pygame, random, time

class UI:
    def __init__(self, player):
        self.player = player
        self.display_surface = pygame.display.get_surface()     #dobija povrsinu za prikaz
        try:
            #pokusava da ucita game font
            self.font, self.bet_font = pygame.font.Font(UI_FONT, UI_FONT_SIZE), pygame.font.Font(UI_FONT, UI_FONT_SIZE)
            self.win_font = pygame.font.Font(UI_FONT, WIN_FONT_SIZE)
        except:
            #ako ne uspe, ispisuje se error msg i program se gasi
            print("Error loading font!")
            print(f"Currently, the UI_FONT variable is set to {UI_FONT}")
            print("Does the file exist?")
            quit()
        self.win_text_angle = random.randint(-4, 4)         #random nagib win poruke

    def display_info(self):             #vraca podatke o igracu
        player_data = self.player.get_data()

        # balans racuna i velicinu uloga
        balance_surf = self.font.render("Balans: $" + player_data['balance'], True, TEXT_COLOR, None)
        x, y = 20, self.display_surface.get_size()[1] - 30
        balance_rect = balance_surf.get_rect(bottomleft = (x, y))

        bet_surf = self.bet_font.render("Ulog: $" + player_data['bet_size'], True, TEXT_COLOR, None)
        x = self.display_surface.get_size()[0] - 20
        bet_rect = bet_surf.get_rect(bottomright = (x, y))
        
        #  player data
        pygame.draw.rect(self.display_surface, False, balance_rect)
        pygame.draw.rect(self.display_surface, False, bet_rect)
        self.display_surface.blit(balance_surf, balance_rect)
        self.display_surface.blit(bet_surf, bet_rect)

        # printa last payout ako postoji
        if self.player.last_payout:
            last_payout = float(player_data['last_payout'])
            win_surf = self.win_font.render("Osvojili ste! $" + "{:.2f}".format(last_payout), True, (0, 255, 0))
            x1, y1 = 800, self.display_surface.get_size()[1] - 60
            win_surf = pygame.transform.rotate(win_surf, self.win_text_angle)
            win_rect = win_surf.get_rect(center=(x1, y1))
            self.display_surface.blit(win_surf, win_rect)
            
        if float(player_data['balance']) < float(player_data['bet_size']):
            message_surf = self.win_font.render("Nazalost, nemate vise sredstava za igru!", True, (255, 0, 0))
            x1, y1 = 800, self.display_surface.get_size()[1] - 60
            message_surf = pygame.transform.rotate(message_surf, self.win_text_angle)
            message_rect = message_surf.get_rect(center=(x1, y1))
            self.display_surface.blit(message_surf, message_rect)
            
        print("Vaš Balans iznosi: " + player_data['balance'])
            
    #iscrtava polje u dnu ekrana, poziva display_info kako bi update-ovala informacije
    def update(self):
        pygame.draw.rect(self.display_surface, 'Black', pygame.Rect(0, 900, 1600, 100))
        self.display_info()