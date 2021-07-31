from enum import Enum
from random import shuffle, randrange

class Ranks(Enum):
    Ace = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Jack = 11
    Queen = 12
    King = 13

class Suits(Enum):
    Heart = "Heart"
    Diamond = "Diamond"
    Club = "Club"
    Spade = "Spade"

class Cards:
    def __init__(self, cardName, cardRank, cardSuit):
        self.name = cardName
        self.rank = cardRank
        self.suit = cardSuit
        self.suits = cardSuit + "s"
        if cardRank <= 10 and cardRank > 1:
            self.value = cardRank
            self.intName = str(cardRank)
        elif cardRank == 1: 
            self.value = 1
            self.intName = cardName
        else:
            self.value = 10 
            self.intName = cardName

    def string(self):
        return self.intName + " of " + self.suits

class Deck:
    def __init__(self, game):
        self.deck = []
        self.discard = []
        self.game = game
        self.cutCount = 0
        self.cutPosition = 0
        for suit in Suits:
            for rank in Ranks:
                card = Cards(rank.name, rank.value, suit.name)
                self.deck.append(card)
        shuffle(self.deck)

    def cut(self):
        deckSize = len(self.deck)
        cutRange = int(deckSize / self.game.players)
        maxCut = deckSize - self.game.players - 1
        if self.cutPosition == 0:
            self.cutPosition = randrange(1, cutRange)
            self.cutCount += 1
        else:
            self.cutPosition = randrange(self.cutPosition + 1, maxCut + self.cutCount)
            self.cutCount += 1
        return self.deck[self.cutPosition]

    def cutToStart(self):
        cuts = []
        survivors = list(range(0, self.game.players))
        while len(survivors) != 1:
            self.cutCount = 0
            self.cutPosition = 0
            cuts.clear()

            for player in survivors:
                cut = self.cut()
                cuts.append([player, cut])
            survivors.clear() 

            if self.game.deckSettings.cutHigh:
                winningRank = max(card.rank for p, card in cuts) 
            else:
                winningRank = min(card.rank for p, card in cuts)
            survivors = [player for player, card in cuts if card.rank == winningRank]

            # if self.consoleLogging:
            #     for player, card in cuts:
            #         print(self.game.playerNames[player] + " cuts a " + card.string())
            #     print("  ---")
            #     if len(survivors) == 1:
            #         result = " is the dealer"
            #     else: 
            #         result = " ties \n  ---"
            #     for player in survivors:
            #         print(self.game.playerNames[player] + result)
        return survivors[0]

    def deal(self):
        handsDealt = []
        if self.game.deckSettings.burnCardOnDeal:
            dealTo = range(0, self.game.players + 1)
        else:
            dealTo = range(0, self.game.players)

        for n in dealTo:
            handsDealt.append([])
        for c in range(0, self.game.rules.cardsDealt):
            for player in dealTo:
                dealtCard = self.deck.pop(0)
                handsDealt[player].append(dealtCard)  

        if self.game.deckSettings.burnCardOnDeal:
            for card in handsDealt.pop(0):
                self.discard.append(card)
        sortedHands = []
        for hand in handsDealt:
            sortHand = sorted(hand, key=lambda card: card.rank)
            sortedHands.append(sortHand)

        handOrder = self.game.playOrder()
        orderedHands = [hand for o, hand in sorted(zip(handOrder, sortedHands))]

        return orderedHands     

