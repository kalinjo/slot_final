from settings import *
import pygame, random

class Reel:
    def __init__(self, pos):
        self.symbol_list = pygame.sprite.Group()        #pokrece reel objekat sa listom simbola
        self.shuffled_keys = list(symbols.keys())
        random.shuffle(self.shuffled_keys)              # radi shuffle i selektuje prvih 5
        self.shuffled_keys = self.shuffled_keys[:5] #Ima veze tek kada ima 5 simbola

        self.reel_is_spinning = False       #postavlja pocetno stanje reelsa na NE okrece se

        for idx, item in enumerate(self.shuffled_keys):
            self.symbol_list.add(Symbol(symbols[item], pos, idx))
            pos = list(pos)
            pos[1] += 300
            pos = tuple(pos)

    def animate(self, delta_time):
        if self.reel_is_spinning:
            self.delay_time -= (delta_time * 1000)
            self.spin_time -= (delta_time * 1000)           #koriste se da smanje delay i spin time, za onoliko vremena koliko je proslo od poslednje ucitanog frejma
            reel_is_stopping = False

            if self.spin_time < 0:
                reel_is_stopping = True

            #Delay reel animacije
            if self.delay_time <= 0:

                #Prolazi kroz svih 5 simbola u reelu; kruni; dodaje novi random simbol na vrh steka.
                for symbol in self.symbol_list:
                    symbol.rect.bottom += 100       #pomera simbol nadole za 100px

                    #Tacan spacing zavisi od iznad dodatog koji eventualno pogadja 1200
                    if symbol.rect.top == 1200:     #proverava da li je gornja strana na Y osi 1200
                        if reel_is_stopping:
                            self.reel_is_spinning = False           #zaustavlja reel nakon spina
                            

                        symbol_idx = symbol.idx
                        symbol.kill()               #brise simbol iz svih grupa
                        #Stvara random simbol na mestu iznad
                        self.symbol_list.add(Symbol(symbols[random.choice(self.shuffled_keys)], ((symbol.x_val), -300), symbol_idx))        #dodaje novi simbol u simbol listu, na odredjenu poziciju, random type 

    def start_spin(self, delay_time):
        self.delay_time = delay_time
        self.spin_time = 1000 + delay_time          #postavljaju delay i spin time za reel
        self.reel_is_spinning = True                #startuje spinovanje

    def reel_spin_result(self):
        #Uzima i vraca tekstualnu prezentaciju simbola u datom reel-u
        spin_symbols = []
        for i in GAME_INDICES:
            spin_symbols.append(self.symbol_list.sprites()[i].sym_type)         #hvata tip simbola sa indeksom i u simbol listi
        return spin_symbols[::-1]

class Symbol(pygame.sprite.Sprite):
    def __init__(self, pathToFile, pos, idx):
        super().__init__()

        # Friendly name
        self.sym_type = pathToFile.split('/')[3].split('.')[0]

        self.pos = pos
        self.idx = idx
        self.image = pygame.image.load(pathToFile).convert_alpha()      #ucitava sliku iz fajla i konvertuje pixel format u onaj koji ukljucuje per-pixel alpha
        self.rect = self.image.get_rect(topleft = pos)                  #oznacava pravougaonu oblast koju pokriva simbol
        self.x_val = self.rect.left                                     #uzima x koordinate leve strane pravougaonika

        #Koristi se za Win animaciju
        self.size_x = 300
        self.size_y = 300
        self.alpha = 255
        self.fade_out = False           #flag
        self.fade_in = False            #flag

    def update(self):
        #Povecava velicinu pobednickih simbola
        if self.fade_in:
            if self.size_x < 320:
                self.size_x += 1
                self.size_y += 1                #povecavaju simbole
                self.image = pygame.transform.scale(self.image, (self.size_x, self.size_y))     #resize image na novu rezoluciju
        
        #Fade out NE pobednickih simbola
        elif not self.fade_in and self.fade_out:
            if self.alpha > 115:
                self.alpha -= 7                 #smanjuje alfu simbola
                self.image.set_alpha(self.alpha)        #postavalja transparentnost za sliku