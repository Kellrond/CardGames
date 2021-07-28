from statistics import mean, stdev  
from deck import Deck
from random import randrange
import datetime as dt


class Cribbage:
    def __init__(self, players=2):
        self.rules = self.Rules()
        self.hands = self.Hands()
        self.text = self.Text()
        self.settings = self.Settings()
        self.name = "Cribbage - Dev Edition"
        self.version = "0.0.1"
        self.note = "Full random play. Only score go and " + str(self.rules.countTarget)
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

    class Settings:
        def __init__(self):
            self.difficulty = "random"
            self.consoleLogging = [None]
            self.autoplay = False
            
    class Rules:
        def __init__(self):
            # Game basics
            self.cardsDealt = 6
            self.handSize = 4
            # Game options     
            self.muggins = False
            # Scoring 
            self.startingScore = 0
            self.winningScore = 5
            self.countTarget = 31
            # Deck
            self.cutHigh = False
            self.aceHigh = False
            self.burnCardOnDeal = False

        def listRules(self):
            ruleString = "" 
            for rule, value in vars(Cribbage.Rules()).items():
                ruleString += " -> " + rule + ": " + str(value) + "\n"
            return ruleString[:-1]

    class Hands:
        def __init__(self):
            self.hands = []
            self.crib = []

        def countHands(self):
            # print("Count hands")
            # print("Count crib")
            self.crib.clear()


    class PlayStage:
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

        def checkForPoints(self, player):
            # Check for go
            score = 0
            console = []

            if self.count == 15:
                # score += 1
                console.append("15")
            elif self.count == self.rules.countTarget:
                score += 1
                console.append("31")
            
            if len(self.goList) == self.players:
                score += 1
                console.append("Go")       

            if self.settings.consoleLogging:
                if len(console) == 1:
                    output = console[0]
                else:
                    output = console.pop(0)
                    for line in console:
                        output += " and " + line

                print(self.playerNames[player] + " scores " + str(score) + " for " + output)

            self.PlayStage.scoreCount(self, player, 1)

    class Text:
        def __init__(self) -> None:
            self.titleBumper = "############################# "
            
        def titleSpacing(self, title, bumper):
            titleLength = len(title)
            totalSpaces = len(bumper)
            if titleLength > totalSpaces:
                title = title[:totalSpaces]
            remainingSpaces = totalSpaces - len(title)
            halfSpace = int(remainingSpaces / 2)
            output = " " * halfSpace + title
            while len(output) < totalSpaces:
                output += " "
            return output

        def gameHeader(self):
            output = Cribbage.Text().titleBumper + Cribbage.Text.titleSpacing(self, Cribbage().name, Cribbage.Text().titleBumper) + Cribbage.Text().titleBumper 


            return output
    
        


    # Game functions

    def consoleLog(self, text, type="All"):
        if type in self.settings.consoleLogging or "All" in self.settings.consoleLogging:
            print(text)

    def endGame(self, gameCount, duration):
        self.log['game'].append(gameCount)
        self.log['duration'].append(duration)
        self.log['winner'].append(self.winner)
        self.log['rounds'].append(self.round)
        self.log['scores'].append(list(self.score))
        if self.settings.consoleLogging:
            print("##### End Game #####")
            print("Rounds: " + str(self.round))
            for i, player in enumerate(self.playerNames):
                print(player + ": " + str(self.score[i]))  

    def endRound(self):
        self.play.clear()
        self.goList.clear()
        self.count = 0
        self.round += 1
        if self.dealer == self.players - 1:
            self.dealer = 0
        else:
            self.dealer += 1

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

    def printScore(self):
        print("----- SCORE -----")
        for player in range(0, self.players):
            print(self.playerNames[player] + " - " + str(self.score[player]))

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
        round = Deck(self)
        self.hands.hands = round.deal()
    
        self.consoleLog("===== " + self.playerNames[self.dealer] + " deals")
        for i, hand in enumerate(self.hands.hands):
            self.consoleLog("----- " + self.playerNames[i] + "'s cards -----")
            for card in hand:
                self.consoleLog(card.string())

        # Discard
        self.consoleLog("===== Discard")

        for player in playOrder:
            hand = self.hands.hands[player]
            if player == 0 and not self.settings.autoplay:
                self.consoleLog(self, "INSERT CODE TO ALLOW ME TO PLAY")
            else:
                if self.settings.difficulty == 'random':
                    while len(hand) > self.rules.handSize:
                        pick = randrange(0,len(hand))
                        discard = hand.pop(pick)
                        self.hands.crib.append(discard)

        # if self.settings.consoleLogging:
        #     for i, hand in enumerate(self.hands.hands):
        #         print("----- " + self.playerNames[i] + " keeps")
        #         for card in hand:
        #             print(card.string())
        #     print("----- Crib ")
        #     for card in self.hands.crib:
        #         print(card.string())

        # Play 
        self.consoleLog("===== Play")

        hands = self.hands.hands[:]
        while max(len(hand) for hand in self.hands.hands) > 0 and len(self.goList) < self.players:
            for player in playOrder:
                hand = hands[player]
                self.playableCards = self.PlayStage.playableCards(self, hand, self.count)
                if player not in self.goList:
                    if player == 0 and not self.settings.autoplay:
                        if self.settings.consoleLogging:
                            print("INSERT CODE TO ALLOW ME TO PLAY") # Currently set up for manual Go
                    else:
                        if len(self.playableCards) == 0:
                            self.goList.append(player)

                            if len(self.goList) == self.players:
                                self.PlayStage.checkForPoints(self, player)
                                self.count = 0
                                self.play.clear()
                                self.goList.clear()

                            else:
                                self.consoleLog(self.playerNames[player] + " calls GO" )

                        else:  
                            if self.settings.difficulty == 'random':
                                randPick = randrange(0,len(self.playableCards))
                                pick = self.playableCards[randPick]
                                play = hand.pop(pick)
                                self.playableCards.clear()
                                self.play.append(play)
                                self.count = sum(card.value for card in self.play)    
                                
                                self.consoleLog("Count: " + str(self.count) + " - " + self.playerNames[player] + " plays a " + play.string()) 

            if max(len(hand) for hand in hands) == 0:
                
                if self.count == self.rules.countTarget:
                    self.PlayStage.scoreCount(self, player, 2)
                    if self.settings.consoleLogging:
                        print(self.playerNames[player] + " scores 2 for " + str(self.rules.countTarget) )
                else:
                    self.PlayStage.scoreCount(self, player, 1)   
                    if self.settings.consoleLogging:
                        print(self.playerNames[player] + " scores 1 for GO" )
        # End play 
        self.hands.countHands()
        self.endRound()
        self.consoleLog(self.printScore())

        
        





            
