from settings import *
from welcome_screen import *

class Player():
    def __init__(self):         #poziva se kad je objekat kreiran iz klase, i dozvoljava klasi da inicijalizuje atribute
        self.balance = number1
        self.bet_size = number2
        self.last_payout = 0.00
        self.total_won = 0.00
        self.total_wager = 0.00

    def get_data(self):
        player_data = {}        #pravi dict koji sadrzi podatke o igracu
        player_data['balance'] = "{:.2f}".format(self.balance)
        player_data['bet_size'] = "{:.2f}".format(self.bet_size)
        player_data['last_payout'] = "{:.2f}".format(self.last_payout) if self.last_payout else "N/A"
        player_data['total_won'] = "{:.2f}".format(self.total_won)
        player_data['total_wager'] = "{:.2f}".format(self.total_wager)
        return player_data

    def place_bet(self):        #simulira postavljanje uloga
        bet = self.bet_size
        self.balance -= bet         #sa balansa skida visinu uloga i oduzima vrednost ukupne opklade
        self.total_wager += bet     #dodaje vrednost opklade u ukupno ulozenu sumu