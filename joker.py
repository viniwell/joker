import easygui as g
import games, cards
import random
TITLE='Game'
RANKS_W = ["Tуз", "Двойка", "Тройка", "Четверка", "Пятерка", "Шестерка", "Семерка",
             "Восьмерка", "Девятка", "Десятка", "Bалет", "Дама", "Король",'Джокер']
RANKS = ["1", "2", "3", "4", "5", "6", "7",
             "8", "9", "10", "11", "12", "13",'14']
SUITS = ['s','c','h','d']
class J_Card(cards.Card):
    def __str__(self):
        return self.suit+str(int(self.rank)//10)+str(int(self.rank)%10)+'.png'
class Reg_pl:
    def __init__(self,name='',bet=0, money=100, pl_num=None):
        self.bet=bet
        self.money=money
        self.name=name
        self.pl_num=pl_num
    def __str__(self):
        return f'{self.name}-{self.money}'
    def registration(self):
        if self.pl_num:
            self.name=f'Player {self.pl_num}'
        reg=g.multenterbox(f'Registration\n{str(self)}',title=TITLE, fields=['name', 'bet'], values=(self.name, self.bet))
        self.name=reg[0]
        while 2*int(reg[1])>=self.money or int(reg[1])>50:
            reg=g.multenterbox(f'Registration\n{str(self)}',title=TITLE, fields=['name', 'bet'], values=[self.name, self.bet])
        self.bet=int(reg[1])
class Bankomet(Reg_pl):
    def registration(self):
        pass
    def __init__(self, money=100):
        super().__init__()
        self.name='Bankomet'
        self.money=money
    def megawin(self, losers):
        for loser in losers:
            self.money+=loser.bet*2
            loser.money-=2*loser.bet
        g.msgbox("The Bankomet choosed the right card-Joker!\nit's MEGAWIN!", title=TITLE)          
    def win(self, losers):
        for loser in losers:
            self.money+=loser.bet
            loser.money-=loser.bet
            loser.bet=0
        g.msgbox("The Bankomet choosed the right card!\nit's WIN!", title=TITLE)  
    def lose(self, losers):
        for loser in losers:
            self.money-=loser.bet
            loser.money+=loser.bet
        g.msgbox("The Bankomet hasn't choosed the right card:(\nit's lose:(", title=TITLE)  

class J_Deck(cards.Deck):
    def populate(self):
        for rank in RANKS:
            for suit in SUITS:
                if rank=='14':
                    if suit in ('s','h'):
                        self.add(J_Card(rank, suit))
                else:
                    self.add(J_Card(rank, suit))
    def deal(self):
        pass
class Game:
    def __init__(self, num=games.ask_number('Choose amount of players(1-8)', title=TITLE,low=1,high=8)):
        self.num=num
        self.games=1
        self.players=[]
        bank_num=random.randint(0, num-1)
        pl_num=0
        for i in range(self.num):
            if i==bank_num:
                self.bankomet=Bankomet()
                self.bankomet.registration()
            else:
                pl_num+=1
                player=Reg_pl(pl_num=pl_num)
                player.registration()
                self.players.append(player)
        self.deck=J_Deck()
        self.deck.populate()
        self.deck.shuffle()
    def play(self):
        self.games+=1
        if self.games!=2:
            bank_num=random.randint(0, self.num-2)
            for i in range(self.num):
                if i==bank_num:
                    self.bankomet, self.players[i]=Bankomet(self.players[i].money),Reg_pl(pl_num=i,money=self.bankomet.money)
            for pl in self.players:
                pl.registration()
        bank_lose=True
        for i in range(13,0, -1):
            g.msgbox('Bankomet:'+str(RANKS_W[i])+'\nCard:', image=str(self.deck.cards[0]))
            if int(self.deck.cards[0].rank)==i+1:
                bank_lose=False

                if i==13:
                    self.bankomet.megawin(self.players)
                    break
                else:
                    self.bankomet.win(self.players)
                    break
            self.deck.cards.remove(self.deck.cards[0])
        if bank_lose:
            self.bankomet.lose(self.players)
def main():
    game=Game()
    again=True
    while again:
        game.play()
        again=games.ask_yes_no('Do you want to continue game?')
    else:
        g.msgbox('\n'.join(str(pl) for pl in [game.bankomet]+game.players), title='Resaults')
main()