from statistics import mean, stdev  
from deck import Deck, Cards
from random import randrange
import datetime as dt


class Cribbage:
    def __init__(self, players=2):
        self.name = "Cribbage - Dev Edition"
        self.author = "Jordan Kell"
        self.version = "0.0.8b"
        self.date = "2021-08-02"
        self.note = "Best card on play by score alone. All scores in the play. Suggesting run plays"
        self.rules = self.Rules()
        self.hands = self.Hands()
        self.text = self.Text()
        self.deckSettings = self.DeckSettings()
        self.settings = self.Settings()
        self.devSettings = self.DevSettings()
        self.players = players
        self.playerNames = ["Jordan", "The machine"] 
        while len(self.playerNames) < self.players:
            self.playerNames.append("Player " + str(len(self.playerNames) + 1))
        self.dealer = 0
        self.prevScore = []
        self.score = []
        self.count = 0
        for i in range(0, players):
            self.prevScore.append(0)
            self.score.append(0)
        self.play = []
        self.cut = Cards("Ace", 1, "Spades")
        self.playableCards = []
        self.goList = []
        self.round = 1
        self.turn = 0
        self.winner = -1
        self.log = {
            'timestamp': dt.datetime.strftime(dt.datetime.now(), "%Y-%m-%d %H:%M:%S"), 
            'name': self.name,
            'version': self.version,
            'summary': {
                'gamesPlayed': 0,
                'durationAvg': 0.0,
                'durationTotal': 0.0,
                'roundsAvg': 0.0,
                'roundsMin': 0,
                'roundsMax': 0,
                'roundsStd': 0.0,
                'playerWinPerc': [],
                'playerMin': [],
                'playerMax': [],
                'playerAvg': [],
                'playerStd': []
                },
            'notes': self.note,
            'players': self.players,
            'rules': vars(Cribbage.Rules()),
            'settings': vars(Cribbage.Settings()),
            'game': [],
            'duration': [],
            'winner': [],
            'rounds': [],
            'scores': [],  
            }
    class DeckSettings:

        def __init__(self):
            self.cutHigh = False
            self.aceHigh = False
            self.burnCardOnDeal = False

    class DevSettings:
        def __init__(self):
            self.autoplay = False

        def listDevSettings(self):
            settingList = [] 
            for setting, value in vars(self).items():
                settingList.append(setting + ": " + str(value))
            return settingList

    class Settings:
        def __init__(self):
            self.difficulty = "random"
            self.consoleLogging = 0
            self.fileLogging = False
            self.devMode = False
            self.games = 1

        def listSettings(self):
            settingList = [] 
            for setting, value in vars(self).items():
                settingList.append(setting + ": " + str(value))
            return settingList
                   
    class Rules:
        def __init__(self):
            # Game basics
            self.cardsDealt = 6
            self.handSize = 4
            # Game options     
            self.muggins = False
            # Scoring 
            self.startingScore = 0
            self.winningScore = 121
            self.countTarget = 31

        def listRules(self):
            ruleList = [] 
            for rule, value in vars(self).items():
                ruleList.append(rule + ": " + str(value))
            return ruleList

    class Hands:
        def __init__(self):
            self.hands = []
            self.crib = []

        def countHands(self):
            # print("Count hands")
            # print("Count crib")
            self.crib.clear()
        
        def listHand(self, player):
            output = []
            for card in self.hands[player]:
                output.append("├ " + card.string())
            return output

        def listCrib(self):
            output = []
            cribList = []
            for playerDiscard in self.crib:
                cribList += playerDiscard
            
            for card in cribList:
                output.append("├ " + card.string())
            return output           

    class PlayStage:
        def bestCard(self, hand, count):
            output = {
                'score': 0,
                'cardIndex': 0
            }
            evalHand = []
            playableCardIndexes = self.PlayStage.playableCards(self, hand, count)
            for i in playableCardIndexes:
                evalHand.append([i, hand[i]])
            for i, card in evalHand:
                cardScore = 0
                countValue = self.count + card.value
                if countValue == 15:
                    cardScore += 2
                elif countValue == self.rules.countTarget:
                    cardScore += 2
                
                cardScore += self.PlayStage.scorePairs(self, testPairs=True, card=card) 
                cardScore += self.PlayStage.scoreRuns(self, testRuns=True, card=card)

                if cardScore > output['score']:
                    output['score'] = cardScore
                    output['cardIndex'] = i
            
            return output['cardIndex']

        def playableCards(self, hand, count):
            cardList = []
            for i, card in enumerate(hand):
                if card.value + count <= self.rules.countTarget:
                    cardList.append(i)
            return cardList

        def scoreCount(self, player, score):
            self.prevScore[player] = self.score[player]
            self.score[player] += score
            if self.score[player] >= self.rules.winningScore:
                self.winner = player

        def scorePairs(self, testPairs=False, **kwargs):
            score = 0
            cardCount = len(self.play)
            if cardCount == 1 and not testPairs:
                return 0
            elif cardCount == 0:
                return 0
            cardsPlayed = [card.rank for card in self.play[-4:]]
            cardsPlayed.reverse()   

            if testPairs:
                cardsPlayed = [kwargs['card'].rank] + cardsPlayed[:] 
                cardCount = len(cardsPlayed)
                if cardCount > 4:
                    cardsPlayed = cardsPlayed[0:4]

            if len(set(cardsPlayed[0:4])) == 1 and cardCount >= 4:
                score = 12
            elif len(set(cardsPlayed[0:3])) == 1 and cardCount >= 3:
                score = 6
            elif len(set(cardsPlayed[0:2])) == 1:
                score = 2

            return score

        def scoreRuns(self, testRuns=False, **kwargs):
            score = 0 
            runScoreList = [0]
            thePlay = self.play.copy()

            if testRuns:
                thePlay += [kwargs['card']]

            cardsPlayed = len(self.play)
            if cardsPlayed >= 3:
                for i in range(3, cardsPlayed + 1):
                    evalCards = self.play[cardsPlayed - i: cardsPlayed].copy()
                    sortedCards = sorted([card.value for card in evalCards])
                    rangeList = list(range(min(sortedCards), max(sortedCards) + 1))
                    if sortedCards == rangeList:
                        runScoreList.append(i)
            score = max(runScoreList)
            return score


    class Text:
        def __init__(self) -> None:
            self.titleBumper = "░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ "  
            self.innerBumper = "═════════════════════════════ "

    # Text functions

    def centerSpacing(self, title):
        titleLength = len(title)
        totalSpaces = len(self.text.titleBumper)
        if titleLength > totalSpaces:
            title = title[:totalSpaces]
        remainingSpaces = totalSpaces - len(title)
        halfSpace = int(remainingSpaces / 2)
        output = " " * halfSpace + title
        while len(output) < totalSpaces:
            output += " "
        return output

    def columnOutput(self, a="", b="", c="", isList=False, newLine=True):
        totalSpaces = len(self.text.titleBumper)
        colList = [a, b, c]
        output = ""

        if isList:
            if b == "" and c == "":
                colList = list(a)
            while len(colList) % 3 != 0:
                colList.append([])

        if isList:
            maxRows = max(len(l) for l in colList)
            for col in colList:
                while len(col) < maxRows:
                    col.append("")
            for varIndex, col in enumerate(colList):
                for rowIndex, row in enumerate(col):
                    while len(row) < totalSpaces:
                        row += " "
                    colList[varIndex][rowIndex] = row      
            count = 0
            while count < maxRows:
                output += str(colList[0][count]) + colList[1][count] + colList[2][count] + "\n"
                count += 1
                if not newLine:
                    output = output[:-2]
                if count == maxRows and len(colList) > 3:
                    count = 0
                    output += "\n"
                    colList = colList[3:]
            if not newLine:
                output = output[:-2]
        else:
            for col in colList:
                while len(col) < totalSpaces:
                    col += " "
                output += str(col)
        return output
        
    def consoleLog(self, text, logType=8, newLine=False):
        # # Loop for lists needed
        # print(type(text))
        if self.settings.consoleLogging >= logType:
            if newLine:
                print("\n")
            print(text)

    def titleBumper(self, text):
        output = self.columnOutput(self.text.titleBumper, self.centerSpacing(text), self.text.titleBumper)
        return output

    def innerBumper(self, text):
        output = self.columnOutput(self.text.innerBumper, self.centerSpacing(text), self.text.innerBumper)
        return output

    def gameHeader(self):
        output = self.titleBumper(self.name)
        output += "\n"
        output += self.columnOutput("Author: %s" % self.author
                                    ,self.centerSpacing("Version: %s" % self.version)
                                    ,"Date updated: %s" % self.date)
        output += '\n'
        return output       

    def rulesList(self):
        colA, colB, colC = [[],[],[]]
        colA = [self.centerSpacing("Rules:")] + self.rules.listRules()
        colB = [self.centerSpacing("Settings:")] + self.settings.listSettings()
        if self.settings.devMode:
            colC = [self.centerSpacing("DevSettings:")] + self.devSettings.listDevSettings()
        else:
            colC = []
        return colA, colB, colC

    def printScore(self):
        scoreList = []
        output = self.innerBumper("Score") + "\n"
        for n in range(0, self.players):
            scoreList.append(["%s: %s" % (self.playerNames[n], self.score[n])])
        output += self.columnOutput(scoreList, isList=True, newLine=False)
        return output

    def printHand(self, player=0, all=False):
        cribExists = len(self.hands.crib) > 0
        if self.devSettings.autoplay:
            all = True
        if all:
            output = []
            for i in range(0, self.players):
                output.append(["┌─ " + self.playerNames[i]] + self.hands.listHand(i))
            if cribExists:
                output.append(["┌─ " + self.playerNames[self.dealer] + "'s crib"] + self.hands.listCrib())
            output = self.columnOutput(output, isList=True)

        else:
            output = self.columnOutput(["┌─ " + self.playerNames[player]] + self.hands.listHand(player),[],[], isList=True)

        return output

    # Game functions

    def autoDiscard(self, player):
        hand = self.hands.hands[player]
        discard = []
        if self.settings.difficulty == 'random' or self.settings.difficulty == 'bestCard':
            while len(hand) > self.rules.handSize:
                pick = randrange(0,len(hand))
                discard.append(hand.pop(pick))
            self.hands.crib.append(discard)            

    def autoPlayStage(self, player, hand):
        if len(self.playableCards) == 0:
            self.goList.append(player)
            if len(self.goList) != self.players:           
                self.consoleLog(self.columnOutput("",self.centerSpacing(self.playerNames[player] + " calls GO"), "") , 2)   

        else:  
            if self.settings.difficulty == 'random':
                randPick = randrange(0,len(self.playableCards))
                pick = self.playableCards[randPick]
                play = hand.pop(pick)
                self.play.append(play)
                self.count = sum(card.value for card in self.play)
            if self.settings.difficulty == 'bestCard':
                bestCard = self.PlayStage.bestCard(self, hand, self.count)  
                play = hand.pop(bestCard)
                self.play.append(play)
                self.count = sum(card.value for card in self.play)
            self.playableCards.clear()
            self.consoleLog(self.columnOutput(self.playerNames[player], play.string(), "Count: " + str(self.count)),2)        

    def endGame(self, gameCount, duration):
        self.log['game'].append(gameCount)
        self.log['duration'].append(duration)
        self.log['winner'].append(self.winner)
        self.log['rounds'].append(self.round)
        self.log['scores'].append(list(self.score))
        # if self.settings.consoleLogging:
        #     print("##### End Game #####")
        #     print("Rounds: " + str(self.round))
        #     for i, player in enumerate(self.playerNames):
        #         print(player + ": " + str(self.score[i]))  

    def endRound(self):
        self.play.clear()
        self.goList.clear()
        self.count = 0
        self.round += 1
        if self.dealer == self.players - 1:
            self.dealer = 0
        else:
            self.dealer += 1

    def endRoundScoreCheck(self, player, hands):
        score = 0
        console = []
        clear = False
        
        if player not in self.goList:
            pairs = self.PlayStage.scorePairs(self)
            if pairs > 0:
                score += pairs
                console.append("pair")

            runs = self.PlayStage.scoreRuns(self)
            if runs > 0:
                score += runs
                console.append("run")
      
        if self.count == 15:
            score += 2
            console.append("15")
        elif self.count == self.rules.countTarget:
            clear = True
            score += 2
            console.append(str(self.rules.countTarget))
        
        if len(self.goList) == self.players:
            clear = True
            score += 1
            console.append("Go")    

        if max(len(hand) for hand in hands) == 0:
            clear = True
            score += 1
            console.append("Go")   


        if clear:
            self.play.clear()
            self.goList.clear()
            self.count = 0            

        if score > 0:
            if len(console) == 1:
                output = console[0]
            elif len(console) > 1:
                output = console.pop(0)
                for line in console:
                    output += " and " + line
            output = "───  " + self.playerNames[player] + " scores " + str(score) + " for " + output
            self.PlayStage.scoreCount(self, player, score)
        else:
            return False
        return output

    def finalizeLog(self):
        self.log['summary']['gamesPlayed'] = len(self.log['game'])
        self.log['summary']['durationAvg'] = mean(self.log['duration'])
        self.log['summary']['durationTotal'] = sum(self.log['duration'])
        self.log['summary']['roundsAvg'] = mean(self.log['rounds'])
        self.log['summary']['roundsMin'] = min(self.log['rounds'])
        self.log['summary']['roundsMax'] = max(self.log['rounds'])
        if self.log['summary']['gamesPlayed'] == 1:
            self.log['summary']['roundsStd'] = 0
        else:
            self.log['summary']['roundsStd'] = stdev(self.log['rounds'])

        for player in range(0, self.log['players']): 
            winList = []
            for winner in self.log['winner']:
                if player == winner:
                    winList.append(1)
                else:
                    winList.append(0)
            self.log['summary']['playerWinPerc'].append(mean(winList))

            if self.log['summary']['gamesPlayed'] == 1:
                self.log['summary']['playerMin'].append(self.log['scores'][0][player])
                self.log['summary']['playerMax'].append(self.log['scores'][0][player])
                self.log['summary']['playerAvg'].append(self.log['scores'][0][player])
                self.log['summary']['playerStd'].append(0)
            else:
                self.log['summary']['playerMin'].append(min(self.log['scores'][player]))
                self.log['summary']['playerMax'].append(max(self.log['scores'][player]))
                self.log['summary']['playerAvg'].append(mean(self.log['scores'][player]))
                self.log['summary']['playerStd'].append(stdev(self.log['scores'][player]))

    def playOrder(self):
        playOrder = []
        if self.dealer == self.players - 1:
            playOrder = list(range(0, self.players))
        else:
            playOrder = list(range(self.dealer + 1, self.players))
            playOrder += list(range(0, self.dealer + 1))
        return playOrder

    def reset(self):
        self.score.clear()
        self.prevScore.clear()
        self.count = 0
        self.round = 0
        self.winner = -1

        for n in range(0, self.players):
            self.score.append(0)
            self.prevScore.append(0)


    # # GAME PLAY START HERE        

    def playRound(self):
        playOrder = self.playOrder()
        
        # Deal hands
        self.consoleLog(self.innerBumper(self.playerNames[self.dealer] + " deals"), 2)
        round = Deck(self)
        self.hands.hands = round.deal()
        self.consoleLog(self.printHand(), 2)

        # Discard
        self.consoleLog(self.innerBumper("Players discard"), 2)
        for player in playOrder:
            if player == 0 and not self.devSettings.autoplay:
                self.consoleLog(self, "INSERT CODE TO ALLOW ME TO PLAY", 1)
            else:
                self.autoDiscard(player)
        self.consoleLog(self.printHand(), 2)

        # Cut
        self.cut = round.cut()
        self.consoleLog("─── Cut is an %s" % self.cut.string(), 1)
        if self.cut.rank == 11:
            self.score[self.dealer] += 1
            self.consoleLog("%s scores 2 for the jack (nibs)" % self.playerNames[self.dealer], 1)

        # Play 
        self.consoleLog(self.innerBumper("Play"), 1)
        playHands = self.hands.hands[:]
        cardsLeft = max(len(hand) for hand in playHands) > 0

        while cardsLeft:
            for player in playOrder:
                hand = playHands[player]
                if player not in self.goList and cardsLeft:
                    if player == 0 and not self.devSettings.autoplay:
                        if self.settings.consoleLogging:
                            self.consoleLog("INSERT CODE TO ALLOW ME TO PLAY", 1)
                    else:
                        self.playableCards = self.PlayStage.playableCards(self, hand, self.count)
                        self.autoPlayStage(player, hand)
                
                    scored = self.endRoundScoreCheck(player, playHands)
                if scored:
                    self.consoleLog(scored, 1)
                    scored = None
                cardsLeft = max(len(hand) for hand in playHands) > 0

        # End play 
        self.hands.countHands()
        self.endRound()
        self.consoleLog(self.printScore(),1)

        
        





            
