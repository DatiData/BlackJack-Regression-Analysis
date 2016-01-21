# Players including the dealer
import random

def total(hand):
	# A Blackjack is a special case.  It's any card with a value of 10 plus an Ace
	# SO
	if len(hand)==2 and (hand.count(11)==1 and (hand.count(10)==1)):
		return -1	# we'll set -1 to Blackjack
	# how many aces in the hand
	aces = hand.count(11) # aces have a default value of 11
	# What's the sum of the hand
	t = sum(hand)
	# you have gone over 21 but there is an ace
	if t > 21 and aces > 0:
		while aces > 0 and t > 21:
			t -= 10		# Because 1 is 10 less than 11
			aces -= 1	# Because we can convert one less ace
	return t

class Shoe:
	"""Class that creates a shoe full of cards"""
	def __init__(self, num=6):
		"""init method that creates a shoe object with the proper number of cards given the number of decks"""
		self.numDecks=num
		self.cards=[]
		
		for k in range(0, self.numDecks):
			for i in ["diamonds","clubs","hearts","spades"]:  # not relevant to blackjack, so we're not going to store it
															  # just use it for generation
															  # Next line is cards plus their values.  Ace is listed as 1.
															  # Players will know better, of course.  Just a placeholder
				for j in [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]:	# Values are all that matter since I'm not implementing splitting
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
		
		for i in range(0, shuffler.randint(4*self.numDecks, 8*self.numDecks)):	# shuffle random number of times
			shuffler.shuffle(self.cards)
	
	def deal(self, num):
		"""deals num cards from deck"""
		
		# if there aren't enough cards, let's refill the shoe
		if num>len(self.cards):
			self.__init__(self.numDecks)
			self.shuffle()
		
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
		for i in shoe.deal(2):
			self.cards.append(i)
		self.showCard=self.cards[1]
		self.hiddenCard=self.cards[0]
	
	def play(self, shoe):
		"""The dealer plays the standard dealer algorithm.	Hit at 17 or below, otherwise stay"""
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
		
# Players uses progressive betting
		
if __name__=="__main__":
	shoe=Shoe(6)
	dealer=Dealer()
	for i in range(1, 1000):
		dealer.dealToSelf(shoe)
		dealer.play(shoe)
		print dealer.cards
		if dealer.total>21:
			print "Bust!!"
		elif dealer.total==-1:
			print "Blackjack!"
		else:
			# print dealer.total
			pass
		dealer.clearHand()