# Players including the dealer
import random

def total(hand):
    # A Blackjack is a special case.  It's any card with a value of 10 plus an Ace
    # SO
    if len(hand)==2 and (hand.count(11)==1 and (hand.count(10)==1)):
        return -1   # we'll set -1 to Blackjack
    # how many aces in the hand
    aces = hand.count(11) # aces have a default value of 11
    # What's the sum of the hand
    t = sum(hand)
    # you have gone over 21 but there is an ace
    if t > 21 and aces > 0:
        while aces > 0 and t > 21:
            t -= 10     # Because 1 is 10 less than 11
            aces -= 1   # Because we can convert one less ace
    return t

def payout(player, dealer):
    # Returns 0 if the player loses
    # 2 if the player wins
    # 3 if the player wins with a natural blackjack and the dealer didn't
    playerBusts=dealerBusts=False
    dealerBlackJack=playerBlackJack=False
    
    if player.total>21:
        playerBusts=True
    if dealer.total>21:
        dealerBusts=True
    if player.total==-1:
        playerBlackJack=True
    if dealer.total==-1:
        dealerBlackJack=True
    
    if dealerBlackJack and not playerBlackJack:
        return 0
    if playerBlackJack and not dealerBlackJack:
        return 3
    if playerBlackJack and dealerBlackJack:
        return 2
    
    if playerBusts:
        return 0
    
    if dealerBusts:
        return 2
    
    if dealer.total>player.total:
        return 0
    else:
        return 2


class Shoe:
    """Class that creates a shoe full of cards"""
    def __init__(self, num=6):
        """init method that creates a shoe object with the proper number of cards given the number of decks"""
        self.numDecks=num
        self.cards=[]
        self.refill=False
        
        for k in range(0, self.numDecks):
            for i in ["diamonds","clubs","hearts","spades"]:  # not relevant to blackjack, so we're not going to store it
                                                              # just use it for generation
                                                              # Next line is cards plus their values.  Ace is listed as 1.
                                                              # Players will know better, of course.  Just a placeholder
                for j in [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]:  # Values are all that matter since I'm not implementing splitting
                    self.cards.append(j)
    
    def getShoe(self):
        """Returns the list of cards left"""
        return self.cards
    
    def shuffle(self):
        """uses the cryptographic quality random number generator to shuffle the cards"""
        # In a six deck shoe, there are 312! permutations
        # The regular random number generator might produce
        # up to 2 to the 64th power pseudorandom numbers
        # before it repeats.  So I have to use the cryptopgraphic
        # quality random generator
        shuffler=random.SystemRandom()
        
        for i in range(0, shuffler.randint(4*self.numDecks, 8*self.numDecks)):  # shuffle random number of times
            shuffler.shuffle(self.cards)
    
    def deal(self, num):
        """deals num cards from deck"""
        
        # if there aren't enough cards, let's refill the shoe
        if num>len(self.cards):
            self.__init__(self.numDecks)
            self.shuffle()
            self.refill=True
        l=[]
        
        for i in range(0,num):
            l.append(self.cards.pop())
        
        return l

class Dealer:
    """"Creates a dealer for playing Blackjack. Doesn't actually deal cards to the players. Simply plays the game"""
    
    def __init__(self):
        self.cards=[]
        self.total=0
    
    def dealToSelf(self, shoe):
        """Dealer gets his 2 cards, one face down"""
        self.cards=shoe.deal(2)
        self.showCard=self.cards[1]
        self.hiddenCard=self.cards[0]
    
    def play(self, shoe):
        """The dealer plays the standard dealer algorithm.  Hit at 17 or below, otherwise stay"""
        while True:
            self.total=total(self.cards)
            if self.total==-1:
                break
            if self.total<17:
                self.cards.append(shoe.deal(1)[0])
            else:
                break
    def clearHand (self):
        self.cards=[]
        self.total=0

# Players using progressive betting
class Player:
    """A standard player who uses progressive betting"""
    
    def __init__(self):
        self.level=1
        self.totalMoney=10000  # The initial amount of cash
        # Dealer Card        A     2    3    4    5    6    7    8    9    10
        self.betPlayMatrix=[["H", "H", "H", "H", "D", "D", "H", "H", "H", "H"],     # player hand 8
                            ["H", "D", "D", "D", "D", "D", "H", "H", "H", "H"],     # player hand 9
                            ["H", "D", "D", "D", "D", "D", "D", "D", "D", "H"],     # player hand 10
                            ["D", "D", "D", "D", "D", "D", "D", "D", "D", "D"],     # player hand 11
                            ["H", "H", "H", "S", "S", "S", "H", "H", "H", "H"],     # player hand 12
                            ["H", "H", "H", "S", "S", "S", "H", "H", "H", "H"],     # player hand 13
                            ["H", "H", "H", "S", "S", "S", "H", "H", "H", "H"],     # player hand 14
                            ["H", "H", "H", "S", "S", "S", "H", "H", "H", "H"],     # player hand 15
                            ["H", "H", "H", "S", "S", "S", "H", "H", "H", "H"]]     # player hand 16
    def dealToSelf(self, shoe):
        self.cards=shoe.deal(2)
    def play(self, shoe, dealerCard):
        self.bet=100*self.level
        self.totalMoney=self.totalMoney-self.bet
        # player will use general strategy without splitting, with Doubling Down allowed
        # on all card combinations.  Soft combinations will be ignored for the sake
        # of simplicity.
        
        # Look at the dealer card.  Then decide to hit, stay, or double down
        # Except for double down, keep doing this until you bust, get 21 or
        # where the odds are against you based on general strategy for a 4-6 deck game
        # See "Optimum Zero-Memory Strategy and Exact Probabilities for 4-Deck Blackjack"
        # by A.R. Manson et al., 1975
        # print "--START PLAYER TURN--"
        whatToDo=""
        while whatToDo!="S":
           self.total=total(self.cards)
           if self.total==-1 or self.total>16:
               whatToDo="S"
           elif self.total<8:
               whatToDo="H"   # hit me
           elif self.total>7:
               if dealerCard==11:
                   x=1
               else:
                   x=dealerCard
               
               whatToDo=self.betPlayMatrix[self.total-8][x-1]
           
           if whatToDo=="D" and len(self.cards)==2:
               self.cards.append(shoe.deal(1)[0])  # Double down, hit me
               self.bet=self.bet*2
               whatToDo="S"
           if whatToDo=="D" and len(self.cards)>2:
               whatToDo="S"
           if whatToDo=="H":
               self.cards.append(shoe.deal(1)[0])

# Thresholds +3, +4, +5 for Hi-Lo

class HiLoPlayer:
    """A Player using High Low Card Counting"""
    
    # All players use the same strategy.  The card counting is about betting
    # not strategy.
    def __init__(self):
        self.level=1
        self.totalMoney=10000  # The initial amount of cash
        self.cardCount=0
        self.actualCount=0   # count when we compensate for number of cards left in the shoe
        # Dealer Card        A     2    3    4    5    6    7    8    9    10
        self.betPlayMatrix=[["H", "H", "H", "H", "D", "D", "H", "H", "H", "H"],     # player hand 8
                            ["H", "D", "D", "D", "D", "D", "H", "H", "H", "H"],     # player hand 9
                            ["H", "D", "D", "D", "D", "D", "D", "D", "D", "H"],     # player hand 10
                            ["D", "D", "D", "D", "D", "D", "D", "D", "D", "D"],     # player hand 11
                            ["H", "H", "H", "S", "S", "S", "H", "H", "H", "H"],     # player hand 12
                            ["H", "H", "H", "S", "S", "S", "H", "H", "H", "H"],     # player hand 13
                            ["H", "H", "H", "S", "S", "S", "H", "H", "H", "H"],     # player hand 14
                            ["H", "H", "H", "S", "S", "S", "H", "H", "H", "H"],     # player hand 15
                            ["H", "H", "H", "S", "S", "S", "H", "H", "H", "H"]]     # player hand 16
    def dealToSelf(self, shoe):
        self.cards=shoe.deal(2)
    
    def countCard(self, cardsTable, shoe):
        """When passed a list of all cards on the table, will count using high/low card counting system"""
        for i in cardsTable:
             if i>1 and i<7:
                 self.cardCount=self.cardCount+1
             if i>9:
                 self.cardCount=self.cardCount-1
        
        # We need to vary this based on the number of dekcs left in the shoe.  Problem is
        # in real life, no one can know the exact number of cards left in the shoe.
        # Real players guess, and then they fudge a bit based on circumstances.  Since
        # the computer can't fudge based on circumstances, we'll let it get the exact
        # number of cards in the shoe to compensate for human intuition.
        
        # There's a slight chance there are no more cards in the shoe.  If so, we shouldn't
        # divide by zero
        if sum(shoe.cards)>0:
             self.actualCount=int(round(self.cardCount/(sum(shoe.cards)/52.0)))
        else:
	         self.cardCount=0  # because if there's no more cards left, we start over anyhow
	         self.actualCount=0
    def play(self, shoe, dealerCard):
        if shoe.refill:
             shoe.refill=False
             self.cardCount=0
             self.actualCount=0
        if self.cardCount<2:
            self.bet=100
        elif self.cardCount==2:
            self.bet=150
        elif self.cardCount==3:
            self.bet=200
        elif self.cardCount>3:
            self.bet=300
        self.totalMoney=self.totalMoney-self.bet
        # print self.cardCount
        #if self.actualCount>1 or self.actualCount<-1:
        #    print self.actualCount

        # player will use general strategy without splitting, with Doubling Down allowed
        # on all card combinations.  Soft combinations will be ignored for the sake
        # of simplicity.
        
        # Look at the dealer card.  Then decide to hit, stay, or double down
        # Except for double down, keep doing this until you bust, get 21 or
        # where the odds are against you based on general strategy for a 4-6 deck game
        whatToDo=""
        while whatToDo!="S":
           self.total=total(self.cards)
           if self.total==-1 or self.total>16:
               whatToDo="S"
           elif self.total<8:
               whatToDo="H"   # hit me
           elif self.total>7:
               if dealerCard==11:
                   x=1
               else:
                   x=dealerCard
               
               whatToDo=self.betPlayMatrix[self.total-8][x-1]
           
           if whatToDo=="D" and len(self.cards)==2:
               self.cards.append(shoe.deal(1)[0])  # Double down, hit me
               self.bet=self.bet*2
               whatToDo="S"
           if whatToDo=="D" and len(self.cards)>2:
               whatToDo="S"
           if whatToDo=="H":
               self.cards.append(shoe.deal(1)[0])

class KOPlayer:
    """A Player using KO Card Counting"""

    # All players use the same strategy.  The card counting is about betting
    # not strategy.
    def __init__(self):
        self.level=1
        self.totalMoney=10000  # The initial amount of cash
        self.cardCount=0
        self.actualCount=0   # count when we compensate for number of cards left in the shoe
        # Dealer Card        A     2    3    4    5    6    7    8    9    10
        self.betPlayMatrix=[["H", "H", "H", "H", "D", "D", "H", "H", "H", "H"],     # player hand 8
                            ["H", "D", "D", "D", "D", "D", "H", "H", "H", "H"],     # player hand 9
                            ["H", "D", "D", "D", "D", "D", "D", "D", "D", "H"],     # player hand 10
                            ["D", "D", "D", "D", "D", "D", "D", "D", "D", "D"],     # player hand 11
                            ["H", "H", "H", "S", "S", "S", "H", "H", "H", "H"],     # player hand 12
                            ["H", "H", "H", "S", "S", "S", "H", "H", "H", "H"],     # player hand 13
                            ["H", "H", "H", "S", "S", "S", "H", "H", "H", "H"],     # player hand 14
                            ["H", "H", "H", "S", "S", "S", "H", "H", "H", "H"],     # player hand 15
                            ["H", "H", "H", "S", "S", "S", "H", "H", "H", "H"]]     # player hand 16
    def dealToSelf(self, shoe):
        self.cards=shoe.deal(2)

    def countCard(self, cardsTable, shoe):
        """When passed a list of all cards on the table, will count using KO card counting system"""
        for i in cardsTable:
             if i>1 and i<8:
                 self.cardCount=self.cardCount+1
             if i>9:
                 self.cardCount=self.cardCount-1

        # We need to vary this based on the number of dekcs left in the shoe.  Problem is
        # in real life, no one can know the exact number of cards left in the shoe.
        # Real players guess, and then they fudge a bit based on circumstances.  Since
        # the computer can't fudge based on circumstances, we'll let it get the exact
        # number of cards in the shoe to compensate for human intuition.

        # There's a slight chance there are no more cards in the shoe.  If so, we shouldn't
        # divide by zero
        if sum(shoe.cards)>0:
             self.actualCount=int(round(self.cardCount/(sum(shoe.cards)/52.0)))
        else:
	         self.cardCount=0  # because if there's no more cards left, we start over anyhow
	         self.actualCount=0
    def play(self, shoe, dealerCard):
        if shoe.refill:
             shoe.refill=False
             self.cardCount=0
             self.actualCount=0
        if self.cardCount<2:
            self.bet=100
        elif self.cardCount==2:
            self.bet=150
        elif self.cardCount==3:
            self.bet=200
        elif self.cardCount>3:
            self.bet=300
        self.totalMoney=self.totalMoney-self.bet
        # print self.cardCount
        #if self.actualCount>1 or self.actualCount<-1:
        #    print self.actualCount

        # player will use general strategy without splitting, with Doubling Down allowed
        # on all card combinations.  Soft combinations will be ignored for the sake
        # of simplicity.

        # Look at the dealer card.  Then decide to hit, stay, or double down
        # Except for double down, keep doing this until you bust, get 21 or
        # where the odds are against you based on general strategy for a 4-6 deck game
        whatToDo=""
        while whatToDo!="S":
           self.total=total(self.cards)
           if self.total==-1 or self.total>16:
               whatToDo="S"
           elif self.total<8:
               whatToDo="H"   # hit me
           elif self.total>7:
               if dealerCard==11:
                   x=1
               else:
                   x=dealerCard

               whatToDo=self.betPlayMatrix[self.total-8][x-1]

           if whatToDo=="D" and len(self.cards)==2:
               self.cards.append(shoe.deal(1)[0])  # Double down, hit me
               self.bet=self.bet*2
               whatToDo="S"
           if whatToDo=="D" and len(self.cards)>2:
               whatToDo="S"
           if whatToDo=="H":
               self.cards.append(shoe.deal(1)[0])

class HiOptPlayer:
    """A Player using High Opt 2 Counting"""

    # All players use the same strategy.  The card counting is about betting
    # not strategy.
    def __init__(self):
        self.level=1
        self.totalMoney=10000  # The initial amount of cash
        self.cardCount=0
        self.actualCount=0   # count when we compensate for number of cards left in the shoe
        # Dealer Card        A     2    3    4    5    6    7    8    9    10
        self.betPlayMatrix=[["H", "H", "H", "H", "D", "D", "H", "H", "H", "H"],     # player hand 8
                            ["H", "D", "D", "D", "D", "D", "H", "H", "H", "H"],     # player hand 9
                            ["H", "D", "D", "D", "D", "D", "D", "D", "D", "H"],     # player hand 10
                            ["D", "D", "D", "D", "D", "D", "D", "D", "D", "D"],     # player hand 11
                            ["H", "H", "H", "S", "S", "S", "H", "H", "H", "H"],     # player hand 12
                            ["H", "H", "H", "S", "S", "S", "H", "H", "H", "H"],     # player hand 13
                            ["H", "H", "H", "S", "S", "S", "H", "H", "H", "H"],     # player hand 14
                            ["H", "H", "H", "S", "S", "S", "H", "H", "H", "H"],     # player hand 15
                            ["H", "H", "H", "S", "S", "S", "H", "H", "H", "H"]]     # player hand 16
    def dealToSelf(self, shoe):
        self.cards=shoe.deal(2)

    def countCard(self, cardsTable, shoe):
        """When passed a list of all cards on the table, will count using Hi-Opt II card counting system"""
        for i in cardsTable:
             if i==4 or i==5:
                 self.cardCount=self.cardCount+2
             if i in [2, 3, 6, 7]:
                 self.cardCount=self.cardCount+1
             if i>9 and i<11:
                 self.cardCount=self.cardCount-2

        # We need to vary this based on the number of decks left in the shoe.  Problem is
        # in real life, no one can know the exact number of cards left in the shoe.
        # Real players guess, and then they fudge a bit based on circumstances.  Since
        # the computer can't fudge based on circumstances, we'll let it get the exact
        # number of cards in the shoe to compensate for human intuition.

        # There's a slight chance there are no more cards in the shoe.  If so, we shouldn't
        # divide by zero
        if sum(shoe.cards)>0:
             self.actualCount=int(round(self.cardCount/(sum(shoe.cards)/52.0)))
        else:
	         self.cardCount=0  # because if there's no more cards left, we start over anyhow
	         self.actualCount=0
    def play(self, shoe, dealerCard):
        if shoe.refill:
             shoe.refill=False
             self.cardCount=0
             self.actualCount=0
        if self.cardCount<2:
            self.bet=100
        elif self.cardCount==2:
            self.bet=150
        elif self.cardCount==3:
            self.bet=200
        elif self.cardCount>3:
            self.bet=300
        self.totalMoney=self.totalMoney-self.bet
        # print self.cardCount
        #if self.actualCount>1 or self.actualCount<-1:
        #    print self.actualCount

        # player will use general strategy without splitting, with Doubling Down allowed
        # on all card combinations.  Soft combinations will be ignored for the sake
        # of simplicity.

        # Look at the dealer card.  Then decide to hit, stay, or double down
        # Except for double down, keep doing this until you bust, get 21 or
        # where the odds are against you based on general strategy for a 4-6 deck game
        whatToDo=""
        while whatToDo!="S":
           self.total=total(self.cards)
           if self.total==-1 or self.total>16:
               whatToDo="S"
           elif self.total<8:
               whatToDo="H"   # hit me
           elif self.total>7:
               if dealerCard==11:
                   x=1
               else:
                   x=dealerCard

               whatToDo=self.betPlayMatrix[self.total-8][x-1]

           if whatToDo=="D" and len(self.cards)==2:
               self.cards.append(shoe.deal(1)[0])  # Double down, hit me
               self.bet=self.bet*2
               whatToDo="S"
           if whatToDo=="D" and len(self.cards)>2:
               whatToDo="S"
           if whatToDo=="H":
               self.cards.append(shoe.deal(1)[0])

class ZenPlayer:
    """A Player using The Zen Counting System found at http://www.blackjackforumonline.com/content/hundred.htm"""

    # All players use the same strategy.  The card counting is about betting
    # not strategy.
    def __init__(self):
        self.level=1
        self.totalMoney=10000  # The initial amount of cash
        self.cardCount=0
        self.actualCount=0   # count when we compensate for number of cards left in the shoe
        # Dealer Card        A     2    3    4    5    6    7    8    9    10
        self.betPlayMatrix=[["H", "H", "H", "H", "D", "D", "H", "H", "H", "H"],     # player hand 8
                            ["H", "D", "D", "D", "D", "D", "H", "H", "H", "H"],     # player hand 9
                            ["H", "D", "D", "D", "D", "D", "D", "D", "D", "H"],     # player hand 10
                            ["D", "D", "D", "D", "D", "D", "D", "D", "D", "D"],     # player hand 11
                            ["H", "H", "H", "S", "S", "S", "H", "H", "H", "H"],     # player hand 12
                            ["H", "H", "H", "S", "S", "S", "H", "H", "H", "H"],     # player hand 13
                            ["H", "H", "H", "S", "S", "S", "H", "H", "H", "H"],     # player hand 14
                            ["H", "H", "H", "S", "S", "S", "H", "H", "H", "H"],     # player hand 15
                            ["H", "H", "H", "S", "S", "S", "H", "H", "H", "H"]]     # player hand 16
    def dealToSelf(self, shoe):
        self.cards=shoe.deal(2)

    def countCard(self, cardsTable, shoe):
        """When passed a list of all cards on the table, will count using zen card counting system"""
        for i in cardsTable:
             if i==11:
                 self.cardCount=self.cardCount-1
             if i in [2, 3, 7]:
                 self.cardCount=self.cardCount+1
             if i in [4, 5, 6]:
                 self.cardCount=self.cardCount+2
             if i==10:
                 self.cardCount=self.cardCount-2
        # We need to vary this based on the number of decks left in the shoe.  Problem is
        # in real life, no one can know the exact number of cards left in the shoe.
        # Real players guess, and then they fudge a bit based on circumstances.  Since
        # the computer can't fudge based on circumstances, we'll let it get the exact
        # number of cards in the shoe to compensate for human intuition.

        # There's a slight chance there are no more cards in the shoe.  If so, we shouldn't
        # divide by zero
        if sum(shoe.cards)>0:
             self.actualCount=int(round(self.cardCount/(sum(shoe.cards)/52.0)))
        else:
	         self.cardCount=0  # because if there's no more cards left, we start over anyhow
	         self.actualCount=0
    def play(self, shoe, dealerCard):
        if shoe.refill:
             shoe.refill=False
             self.cardCount=0
             self.actualCount=0
        if self.cardCount<2:
            self.bet=100
        elif self.cardCount==2:
            self.bet=150
        elif self.cardCount==3:
            self.bet=200
        elif self.cardCount>3:
            self.bet=300
        self.totalMoney=self.totalMoney-self.bet
        # print self.cardCount
        #if self.actualCount>1 or self.actualCount<-1:
        #    print self.actualCount

        # player will use general strategy without splitting, with Doubling Down allowed
        # on all card combinations.  Soft combinations will be ignored for the sake
        # of simplicity.

        # Look at the dealer card.  Then decide to hit, stay, or double down
        # Except for double down, keep doing this until you bust, get 21 or
        # where the odds are against you based on general strategy for a 4-6 deck game
        whatToDo=""
        while whatToDo!="S":
           self.total=total(self.cards)
           if self.total==-1 or self.total>16:
               whatToDo="S"
           elif self.total<8:
               whatToDo="H"   # hit me
           elif self.total>7:
               if dealerCard==11:
                   x=1
               else:
                   x=dealerCard

               whatToDo=self.betPlayMatrix[self.total-8][x-1]

           if whatToDo=="D" and len(self.cards)==2:
               self.cards.append(shoe.deal(1)[0])  # Double down, hit me
               self.bet=self.bet*2
               whatToDo="S"
           if whatToDo=="D" and len(self.cards)>2:
               whatToDo="S"
           if whatToDo=="H":
               self.cards.append(shoe.deal(1)[0])



if __name__=="__main__":
    # So to run these simulations we want a few things
    # first, the y variable is the total amount earned (not total amount)
    # the x variables will be:
    # number of decks in the shoe
    # card counting mechanism used
    #
    # I originally planned on having number of other players.  Turns out, it's not important
    # since blackjack is only about the player vs the dealer.  That simplifies the data too
    # since I can run multiple simulations at the same time (for each of the card counting mechanisms)
    # To make up for the loss of the variable, I've added an extra card counting mechanism (zen counting)
    #
    # Data will be exported in the format
    # amount won, decks, card counting mechanism used
    #
    # Simulation allows for many, many rows.  I've decided not to overtax minitab
    # too much, though, and stick to 100 for each number of decks between 4 and 8
    
    
    for i in range(4, 9):             # a loop for numbers of decks in the shoe between 4 and 8
        for j in range(0, 100):       # a loop for 100 simulations
                
                shoe=Shoe(i)
                dealer=Dealer()
                normPlayer=Player()  # a player using strategy, but no card counting
                hiLo=HiLoPlayer()    # a player using High/Low Counting
                KO=KOPlayer()        # a player using KO Counting
                hiOpt=HiOptPlayer()  # a player using Hi-Opt II Counting
                zen=ZenPlayer()      # a player using Zen Counting
                
                for k in range (0, 200):  # a loop for 200 hands per simulation, about 2-3 hours worth at a table
                    # DEAL
                    normPlayer.dealToSelf(shoe)
                    hiLo.dealToSelf(shoe)
                    KO.dealToSelf(shoe)
                    hiOpt.dealToSelf(shoe)
                    zen.dealToSelf(shoe)
                    dealer.dealToSelf(shoe)
                    
                    # PLAY
                    normPlayer.play(shoe, dealer.showCard)
                    hiLo.play(shoe, dealer.showCard)
                    KO.play(shoe, dealer.showCard)
                    hiOpt.play(shoe, dealer.showCard)
                    zen.play(shoe, dealer.showCard)
                    
                    # RESOLVE HAND
                    normPlayer.totalMoney=normPlayer.totalMoney+normPlayer.bet*payout(normPlayer, dealer)
                    hiLo.totalMoney=hiLo.totalMoney+hiLo.bet*payout(hiLo, dealer)
                    KO.totalMoney=KO.totalMoney+KO.bet*payout(KO, dealer)
                    hiOpt.totalMoney=hiOpt.totalMoney+hiOpt.bet*payout(hiOpt, dealer)
                    zen.totalMoney=zen.totalMoney+zen.bet*payout(zen, dealer)
                    
                    # GRAB A LIST OF CARDS ON TABLE FOR COUNTING
                    tableCards=[]
                    for l in normPlayer.cards:
                        tableCards.append(l)
                    for l in hiLo.cards:
                        tableCards.append(l)
                    for l in KO.cards:
                         tableCards.append(l)
                    for l in hiOpt.cards:
                         tableCards.append(l)
                    for l in zen.cards:
                         tableCards.append(l)
                    for l in dealer.cards:
                        tableCards.append(l)
                    
                    # COUNT CARDS
                    hiLo.countCard(tableCards, shoe)
                    KO.countCard(tableCards, shoe)
                    hiOpt.countCard(tableCards, shoe)
                    zen.countCard(tableCards, shoe)
                # print "Simulation ",j+1," with ", i, "decks in the shoe"
                print normPlayer.totalMoney-10000,",",i,",","none"
                print hiLo.totalMoney-10000,",", i,",","HiLo"
                print KO.totalMoney-10000,",",i,",","KO"
                print hiOpt.totalMoney-10000,",",i,",","hiOpt"
                print zen.totalMoney-10000,",",i,",","Zen"
