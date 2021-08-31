import random
class CompetitorInstance():
    def __init__(self):
        # initialize personal variables
        pass
    
    def onGameStart(self, engine, gameParameters):
        # engine: an instance of the game engine with functions as outlined in the documentation.
        self.engine=engine
        self.gameParameters = gameParameters
    
    def onAuctionStart(self, index, trueValue):
        self.round = 0
        pass

    def onBidMade(self, whoMadeBid, howMuch):
        pass

    def onMyTurn(self,lastBid):
        
        """ if self.round > :
            return """
            

        if self.round == 3:
            self.engine.makeBid(15000)
            


        """ if self.engine.random.randint(0,100)<50:
            self.engine.makeBid(lastBid+8) """
        
        self.round += 1
        pass

    def onAuctionEnd(self):
        # Now is the time to request a swap, if you want
        # engine.swapTo(12)
        pass