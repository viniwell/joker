import easygui as g
import games, cards
import random
TITLE='Game'

RANKS_W = ["Двойка", "Тройка", "Четверка", "Пятерка", "Шестерка", "Семерка",
             "Восьмерка", "Девятка", "Десятка", "Bалет", "Дама", "Король","Tуз",'Джокер']
RANKS = ["1", "2", "3", "4", "5", "6", "7",
             "8", "9", "10", "11", "12", "13",'14']
SUITS = ['s','c','h','d']
class J_Card(cards.Card):
    def __str__(self):
        return 'assets/'+self.suit+str(int(self.rank)//10)+str(int(self.rank)%10)+'.png'
class Reg_pl:
    def __init__(self,name='',bet=50, money=100, pl_num=None):
        self.bet=bet
        self.money=money
        self.name=name
        self.pl_num=pl_num
    def __str__(self):
        return f'{self.name}-{self.money}'
    def registration(self):
        if not self.name:
            self.name=f'Player {self.pl_num}'
        reg=g.multenterbox(f'Registration\n{str(self)}',title=TITLE, fields=['name', 'bet'], values=(self.name, self.bet))
        self.name=reg[0]
        while 2*int(reg[1])>self.money or int(reg[1])>50:
            reg=g.multenterbox(f'Registration\n{str(self)}',title=TITLE, fields=['name', 'bet'], values=[self.name, self.bet])
        self.bet=int(reg[1])
class Bankomet(Reg_pl):
    def registration(self):
        self.name=g.enterbox('Enter your name(you are bankomet)',title='Registration', default=self.name)
    def __str__(self):
        return self.name+'(Bankomet)-'+"self.money"
    def __init__(self, name='',money=100,pl_num=None):
        self.name=name
        if not self.name:
            self.name=f'Player {pl_num}'
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
        for i in range(self.num):
            if i==bank_num:
                self.bankomet=Bankomet(pl_num=i+1)
                self.bankomet.registration()
            else:
                player=Reg_pl(pl_num=i+1)
                player.registration()
                self.players.append(player)
        self.deck=J_Deck()
        self.deck.populate()
        self.deck.shuffle()
    def check(self):
        poor_pl=[]
        for pl in self.players+[self.bankomet]:
            if pl.money<=0:
                self.players.remove(pl)
                self.num-=1
                poor_pl.append(pl)
        if poor_pl:
            AGAIN=g.ynbox('Players '+','.join(player.name for player in poor_pl)+'were removed from the table:(\nContinue?')


    def play(self):
        self.deck.clear()
        self.deck.populate()
        self.deck.shuffle()
        self.games+=1
        if self.games!=2:
            bank_num=random.randint(0, self.num-1)
            for i in range(self.num):
                if i==bank_num:
                    self.bankomet, self.players[i]=Bankomet(name=self.players[i].name,money=self.players[i].money),Reg_pl(pl_num=i,money=self.bankomet.money,name=self.bankomet.name)
            self.bankomet.registration()
            for pl in self.players:
                pl.registration()
        bank_lose=True
        for i in range(13,-1, -1):
            g.msgbox('Bankomet:'+str(RANKS_W[i])+'\nCard:', image=str(self.deck.cards[0]))
            if int(self.deck.cards[0].rank)==i+2:
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
        self.check()
def main():
    g.msgbox("Welcome into the 'Joker' game!",)
    game=Game()
    AGAIN=True
    while AGAIN:
        game.play()

        AGAIN=games.ask_yes_no('Do you want to continue game?')
    else:
        g.msgbox('\n'.join(str(pl) for pl in [game.bankomet]+game.players)+'\nThanks for playing!', title='Resaults')
main()