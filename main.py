import time
import json
from deck import Deck
from games import cribbage

fileLogging = False
devMode = True

if __name__ == "__main__":
    game = cribbage.Cribbage(players=2)
    games = 1
    gameCount = 0
# Dev settings
    if devMode:
        games = 1
        game.settings.consoleLogging = ["Major"]
        game.settings.autoplay = True
    
# Initial load screen for game 
    game.consoleLog(game.text.gameHeader(), "Major")

    if game.settings.autoplay:
        game.consoleLog(" >>>> Autoplay enabled ", "Major")
    game.consoleLog(game.Rules().listRules(), "Minor")
    game.consoleLog("-----------------------------", "Major")
    game.consoleLog("######## Start Game  ########", "Major")
  
  
    while gameCount < games:
        START = time.time()

        game.reset()
        game.dealer = Deck(game).cutToStart()

        if not game.settings.autoplay:
            input("<enter>")

# Game round    
        while game.winner < 0:

            game.consoleLog("######## Round " + str(game.round) + "   ##########")
         
# Start gameplay 
            game.playRound()

        gameCount += 1
        END = time.time()
        duration = END - START
        game.endGame(gameCount, duration)

    game.finalizeLog()

    if fileLogging:
        with open("log.json", "a") as fp:
            jsonLog = json.dumps(game.log)
            fp.write(jsonLog + "\n")

    if devMode:
        print("\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ Game log $$$$$$$$$$$$$$$$$$$$$$$$$4$$$$$$")
        for k,v in game.log.items():
            if k == 'summary':
                print("$$$ Summary $$$")
                for k,v in v.items():
                    print(k, end=": ")
                    print(v)

            else:
                print(k, end=": ")
                print(v)


        

    



        
            
