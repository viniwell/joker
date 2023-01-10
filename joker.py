import easygui as g
import games, cards
import random
import os
TITLE='Game'

RANKS_W = ["Двойка", "Тройка", "Четверка", "Пятерка", "Шестерка", "Семерка",
             "Восьмерка", "Девятка", "Десятка", "Bалет", "Дама", "Король","Tуз",'Джокер']
RANKS = ['1',"2", "3", "4", "5", "6", "7",
             "8", "9", "10", "11", "12", "13",'14']
SUITS = ['s','c','h','d']
class J_Card(cards.Card):
    def __str__(self):
        return 'assets/'+os.path.join(self.suit+str((int(self.rank))//10)+str((int(self.rank))%10)+'.png')
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
        return self.name+'(Bankomet)-'+str(self.money)
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
        for pl in self.players:
            if pl.money<=0:
                self.players.remove(pl)
                self.num-=1
                poor_pl.append(pl)
        if self.bankomet.money<=0:
            poor_pl.append(self.bankomet)
            self.num-=1
            rand_pl=self.players[random.randint(0,self.num)]
            last_bankomet=self.bankomet
            self.bankomet, self.players[self.players.index(rand_pl)]=Bankomet(name=rand_pl.name, pl_num=rand_pl.pl_num), self.bankomet
            self.players.remove(last_bankomet)
        for i in poor_pl:
            if i in self.players:
                self.players.remove(i)
        if poor_pl:
            AGAIN=g.ynbox('Players '+','.join(player.name for player in poor_pl)+' were removed from the table:(\nContinue?')
        else:
            AGAIN=games.ask_yes_no('Do you want to continue game?')
        return AGAIN


    def play(self):
        self.deck.clear()
        self.deck.populate()
        self.deck.shuffle()
        self.num=int(len(self.players))
        self.games+=1
        if self.games!=2:
            bank_num=random.randint(0, self.num-1)
            for i in range(self.num):
                if i==bank_num:
                    if self.bankomet:
                        self.bankomet, self.players[i]=Bankomet(name=self.players[i].name,money=self.players[i].money),Reg_pl(pl_num=i,money=self.bankomet.money,name=self.bankomet.name)
                    else:
                        self.bankomet=Bankomet(name=self.players[i].name, money=self.players[i].money)
                        self.players.remove(self.players[i])
                        self.num-=1
            self.bankomet.registration()
            for pl in self.players:
                pl.registration()
        bank_lose=True
        for i in range(14,0, -1):
            g.msgbox('Bankomet:'+str(RANKS_W[i-1])+'!'+'\nCard:', image=str(self.deck.cards[0]))
            if i==RANKS.index(self.deck.cards[0].rank):
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
    g.msgbox("Welcome into the 'Joker' game!",image='assets/joker.png')
    rules=g.ynbox('Would you like to read rules of the game?', title=TITLE)
    if rules:
        g.msgbox('''Количество колод: 1
Количество карт в колоде: 52 и 2 джокера
Количество игроков: любое
Старшинство карт: 2, 3, 4, 5, 6, 7, 8, 9, 10, В, Д, К, Т, Джокер.
Цель игры: в роли банкомета угадать карту и забрать все ставки.
Правила игры. Сдатчик он же банкомет определяется следующим образом. Каждому игроку предлагается вытащить по одной карте из колоды, игрок, у которого карта старше, становится банкометом. После этого банкомет карты тщательно тасует, снимает и предлагает всем игрокам сделать ставки. Игроки заранее договариваются о потолке ставки, что больше определенной суммы ставить нельзя, например 10 рублей. После того, как все ставки были сделаны, банкомет начинает игру. С верхней части колоды он снимает и открывает по одной 14 карт. Одновременно с открытием карты он называет ее по достоинству. Называть он должен строго по порядку, начинать должен с джокера, а заканчивать двойкой. Например: джокер, туз, король, дама, валет и так до двойки. Если банкомет угадывает хоть одну карту, то весь банк (все ставки) достаются ему и он выигрывает. Если банкомет угадывает первую карту, то есть джокера, то ставки удваиваются и каждый игрок должен доложить банкомету ту сумму денег, которую он ставил. После этого игра начинается заново. Банкомет, который не угадал ни одной карты из четырнадцати, платит всем игрокам их объявленные ставки и передает карты для банкования следующему игроку по часовой стрелке, то есть слева.''')
    game=Game()
    AGAIN=True
    while AGAIN:
        game.play()
        AGAIN=game.check()
    else:
        g.msgbox('\n'.join(str(pl) for pl in [game.bankomet]+game.players)+'\nThanks for playing!', title='Resaults')
main()