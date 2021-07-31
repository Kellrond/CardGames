import time
import json
from deck import Deck
from games import cribbage

devMode = True

if __name__ == "__main__":
    game = cribbage.Cribbage(players=2)
    gameCount = 0
# Dev settings
    if devMode:
        game.settings.devMode = True
        game.settings.consoleLogging = 0
        game.devSettings.autoplay = True
        game.settings.fileLogging = True
        game.settings.games = 100

    
# Initial load screen for game 
    if game.settings.consoleLogging == 0:
        print("Please wait, playing games...")
    game.consoleLog(game.gameHeader(), 1)
    game.consoleLog("Notes: %s \n" % game.note, 2)
    game.consoleLog(game.columnOutput(game.rulesList(), isList=True, newLine=True), 2)
    game.consoleLog(game.titleBumper("Begin game"), 1)
   
    while gameCount < game.settings.games:
        START = time.time()

        game.reset()
        game.dealer = Deck(game).cutToStart()

        if not game.devSettings.autoplay:
            input("<enter>")

# Game round    
        while game.winner < 0:
        # while game.round < 3:

            game.consoleLog(game.titleBumper("Round %s" % (game.round + 1)), 1)
         
# Start gameplay 
            game.playRound()

        gameCount += 1 
        END = time.time()
        duration = END - START
        game.endGame(gameCount, duration)

    game.finalizeLog()

    if game.settings.fileLogging:
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


        

    



        
            
