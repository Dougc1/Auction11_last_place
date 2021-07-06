from gameEngine import GameEngine, NPCRandomBot

# import your bots here
import importlib

botsToRun = {
    "examples.randomBidder":4,
    "examples.randomAccuser":1,
    "NPC": 4
}

engine = GameEngine()

# Warning: Timeouts are not enforced locally - so if you have an infinite loop, beware!
for b in botsToRun:
    if b=="NPC":
        engine.registerBot(NPCRandomBot(),team="NPC")
    else:
        botClass = importlib.import_module(b)
        for i in range(botsToRun[b]):
            engine.registerBot(botClass.CompetitorInstance(),team=b)
engine.runGame()