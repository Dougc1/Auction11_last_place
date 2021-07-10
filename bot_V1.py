class CompetitorInstance():
    def __init__(self):
        # initialize personal variables
        pass
    
    def onGameStart(self, engine, gameParameters):
        # engine: an instance of the game engine with functions as outlined in the documentation.
        self.engine=engine
        self.t_val_code = (9,16,11,12)
        self.team_code = (15,8,13,12)
        # gameParameters: A dictionary containing a variety of game parameters
        self.gameParameters = gameParameters
        self.players = self.gameParameters['numPlayers']
        
        


    def onAuctionStart(self, index, trueValue):
        # index is the current player's index, that usually stays put from game to game
        # trueValue is -1 if this bot doesn't know the true value 

        #keeps track of last bid
        self.prev_price = 1

        self.round = 0
        self.bids = 0

        #tracks bid difference in players in matrix
        self.bidsdiff = []
        for i in range(self.players):
            self.bidsdiff.append([])
        pass

        self.true_value = trueValue

        if trueValue == -1:
            self.code = self.team_code
        else:
            self.code = self.t_val_code


        self.own_team_list = []
        self.non_npc_list = []
        self.true_value_players = []
        self.t_player = -1
        

    def onBidMade(self, whoMadeBid, howMuch):
        # whoMadeBid is the index of the player that made the bid
        # howMuch is the amount that the bid was
        dif = howMuch - self.prev_price
        if (dif > 23 or dif < 8) and whoMadeBid not in self.non_npc_list:
                self.non_npc_list.append(whoMadeBid)
        
        
        self.bidsdiff[whoMadeBid].append(dif)
        self.prev_price = howMuch

        if len(self.bidsdiff[whoMadeBid]) == 4 and whoMadeBid not in self.non_npc_list:
            if tuple(self.bidsdiff[whoMadeBid]) == self.team_code:
                self.own_team_list.append(whoMadeBid)
                self.non_npc_list.append(whoMadeBid)
            elif tuple(self.bidsdiff[whoMadeBid]) == self.t_val_code:
                self.own_team_list.append(whoMadeBid)
                self.non_npc_list.append(whoMadeBid)
                self.true_value_players.append(whoMadeBid)
                self.t_player = whoMadeBid

        pass

    def standardbid(self,lastBid):
        if (lastBid < self.gameParameters["meanTrueValue"]):
                # But don't bid too high!
                b = lastBid+(8*(1+2*self.engine.random.random()))
                self.engine.makeBid(self.engine.math.floor(b)) 
        pass

    def onMyTurn(self,lastBid):
        # lastBid is the last bid that was made
        if round == 5:
            #choose 1 player if true value not known based on betting position
            #else choose 1 player with no t_value and 1 with no knowlegde based on position
            i = 1

        if self.round < 4:
            self.engine.makeBid(lastBid+self.code[self.round])
        else:
            self.standardbid(lastBid)
           

        self.round += 1       
        pass

    def onAuctionEnd(self):
        # Now is the time to report team members, or do any cleanup.
        """ self.engine.print(self.bidsdiff)
        self.engine.print(self.own_team_list)
        self.engine.print(self.non_npc_list)
        self.engine.print(self.true_value_players) """
        
        self.engine.reportTeams(self.own_team_list,self.non_npc_list,self.true_value_players)
        pass