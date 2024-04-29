from player import Player
from reel import *
from settings import *
from ui import UI
from win import *
import pygame

class Machine:
    def __init__(self):                     #konstrkt - pokrece masinu i kreita objekte
        self.display_surface = pygame.display.get_surface()     #display povrsina
        self.machine_balance = 100.00
        self.reel_index = 0
        self.reel_list = {}                 
        self.can_toggle = True              #Control flag
        self.spinning = False               
        self.can_animate = False            
        self.win_animation_ongoing = False  

        #Rezultati
        self.prev_result = {0: None, 1: None, 2: None, 3: None, 4: None}
        self.spin_result = {0: None, 1: None, 2: None, 3: None, 4: None}

        self.spawn_reels()
        self.currPlayer = Player()          #Player object  
        self.ui = UI(self.currPlayer)       #UI object
        

    def cooldowns(self):
        #Dozvoljava igracu da spinuje, samo ako se reel NE okrece!
        for reel in self.reel_list:
            if self.reel_list[reel].reel_is_spinning:
                self.can_toggle = False
                self.spinning = True

        #Ako se ne okrecu, dozvoljava pokretanje spina
        if not self.can_toggle and [self.reel_list[reel].reel_is_spinning for reel in self.reel_list].count(False) == 5:
            self.can_toggle = True
            self.spin_result = self.get_result()

            #nakon spina proverava ishod zbog pogodaka
            if self.check_wins(self.spin_result):
                self.win_data = self.check_wins(self.spin_result)
                self.pay_player(self.win_data, self.currPlayer)
                self.win_animation_ongoing = True
                self.ui.win_text_angle = random.randint(-4, 4)


    def input(self):
        keys = pygame.key.get_pressed()

        #Proverava da li pritisnut Space key, dok ima dovoljno na balansu i ako se masina NE okrece, pokrece spin
        if keys[pygame.K_SPACE] and self.can_toggle and self.currPlayer.balance >= self.currPlayer.bet_size:
            self.toggle_spinning()
            self.spin_time = pygame.time.get_ticks()
            self.currPlayer.place_bet()
            self.machine_balance += self.currPlayer.bet_size        #uklanja visinu uloga sa igracevog balansa i dodaje na balans masine
            self.currPlayer.last_payout = None
            
            
    #stvara animaciju vrtenja
    def draw_reels(self, delta_time):
        for reel in self.reel_list:
            self.reel_list[reel].animate(delta_time)


    #kreira reels u slot masini po X i Y koordinatama
    def spawn_reels(self):
        if not self.reel_list:
            x_topleft, y_topleft = 10, -300
        while self.reel_index < 5:
            if self.reel_index > 0:
                x_topleft, y_topleft = x_topleft + (300 + X_OFFSET), y_topleft
            
            self.reel_list[self.reel_index] = Reel((x_topleft, y_topleft)) # za kreiranje reel obj
            self.reel_index += 1


    def toggle_spinning(self):          #Kontrolise start&stop spinovanja reelsa #flag - da li se reelsi pokrecu. Ako se okrecu ili nema dovoljno novca, postavlja se False i ne ide dalje
        if self.can_toggle:
            self.spin_time = pygame.time.get_ticks()
            self.spinning = not self.spinning        #pokrece spin ako se spinovanje ne desava, i zaustavlja ih ako se spinovanje desava
            self.can_toggle = False                  #sprecava ponovno okretanje dok se svi reelsi ne zaustave    

            for reel in self.reel_list:         #prolazi kroz svaki reel u listi i poziva start spin metodu
                self.reel_list[reel].start_spin(int(reel) * 200)
                self.win_animation_ongoing = False      #sprecava ponavljanje win animacije od prethodnoh vrtenja


    def get_result(self):           #uzima rez svakog spina i cuva u spin_result listi
        for reel in self.reel_list:
            self.spin_result[reel] = self.reel_list[reel].reel_spin_result()
        return self.spin_result     
    

    def check_wins(self, result):
        hits = {}
        horizontal = flip_horizontal(result)
        for row in horizontal:
            for sym in row:
                if row.count(sym) > 2: #potencijalni pogodak
                    possible_win = [idx for idx, val in enumerate(row) if sym == val]

                    #Proverava possible_win za sekvencu duzu od 2 i dodaje u pogotke
                    if len(longest_seq(possible_win)) > 2:
                        hits[horizontal.index(row) + 1] = [sym, longest_seq(possible_win)]
        if hits:
            self.can_animate = True
            return hits


    def pay_player(self, win_data, curr_player):            #kalkulise isplate igracu
        multiplier = 0
        spin_payout = 0
        for v in win_data.values():
            multiplier += len(v[1])
        spin_payout = (multiplier * curr_player.bet_size)
        curr_player.balance += spin_payout                  #dodaje isplatu na balans
        self.machine_balance -= spin_payout                 #oduzima visinu isplate od balansa masine
        curr_player.last_payout = spin_payout               #update-uje igracevu poslednju isplatu
        curr_player.total_won += spin_payout                #update-uje ukupno osvojeni iznos


    def win_animation(self):
        if self.win_animation_ongoing and self.win_data:        
            for k, v in list(self.win_data.items()):        #postavlja animaciju reda baziranu na kljucu
                if k == 1:
                    animationRow = 3
                elif k == 3:
                    animationRow = 1
                else:
                    animationRow = 2
                animationCols = v[1]                        #postavlja animaciju kolone baziranu na vrednosti
                for reel in self.reel_list:
                    if reel in animationCols and self.can_animate:      #prolazi kroz svaki reel
                        self.reel_list[reel].symbol_list.sprites()[animationRow].fade_in = True     #ako je reel u animationcols i self.can.animate je True, aktivira fade in
                    for symbol in self.reel_list[reel].symbol_list:
                        if not symbol.fade_in:                                                         #ako reel nije u animationcols, aktivira fade out
                            symbol.fade_out = True


    def update(self, delta_time):       #update-uje stanje igre - poziva se jednom po frejmu u gameloop.
        self.cooldowns()                #poziva metode
        self.input()
        self.draw_reels(delta_time)
        for reel in self.reel_list:
            self.reel_list[reel].symbol_list.draw(self.display_surface)        #crta simbole na svakom reelu
            self.reel_list[reel].symbol_list.update()                          
        self.ui.update()                                                #update-uje user interface
        self.win_animation()