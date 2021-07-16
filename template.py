from random import random


class CompetitorInstance():
    def __init__(self):
        # initialize personal variables
        pass
    
    def onGameStart(self, engine, gameParameters):
        # engine: an instance of the game engine with functions as outlined in the documentation.
        self.engine=engine
        self.t_val_code = (9,10,11,12)
        self.team_code = (15,14,13,12)
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

        self.who_am_i = -1
        self.latest_bidder = -1

        #tracks bid difference of players in list of list
        #bid difference difference in bid between a bid made a player
        #and the last/highest bid made
        self.bids_diff = []
        for i in range(self.players):
            self.bids_diff.append([])
        pass

        self.code_pos = 0


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

        # if bid outside range then they are not an npc
        dif = howMuch - self.prev_price
        if (dif > 23 or dif < 8) and whoMadeBid not in self.non_npc_list:
                self.non_npc_list.append(whoMadeBid)
        
        #adds bids to matrix of bids differences and updates previous price
        self.bids_diff[whoMadeBid].append(dif)
        self.prev_price = howMuch

        # checks to see if the person making the bid is following a team code
        if len(self.bids_diff[whoMadeBid]) == 4 and whoMadeBid not in self.non_npc_list:
            if tuple(self.bids_diff[whoMadeBid]) == self.team_code:
                self.own_team_list.append(whoMadeBid)
                self.non_npc_list.append(whoMadeBid)
            elif tuple(self.bids_diff[whoMadeBid]) == self.t_val_code:
                self.own_team_list.append(whoMadeBid)
                self.non_npc_list.append(whoMadeBid)
                self.true_value_players.append(whoMadeBid)
                self.t_player = whoMadeBid

        #updates latest bidder
        self.latest_bidder = whoMadeBid
        pass

    #creates a bid simulating a npc's random bid
    def random_bid(self,lastBid):
        b = lastBid+(8*(1+2*self.engine.random.random()))
        self.engine.makeBid(self.engine.math.floor(b)) 
        pass

    #bidding when no bot knows the true value
    def standard_bid(self,lastBid):
        if (lastBid < self.gameParameters["meanTrueValue"]):
                self.random_bid(lastBid)
        pass

    #bidding for a bot which doesn't know the 
    def normal_player_bid(self,lastBid):
        if len(self.bids_diff[self.t_player]) == 8:
            self.true_value = 0
            for i in range(4):
                self.true_value += pow(16,3-i)*(self.bids_diff[self.t_player][4+i] - 8)

        if len(self.bids_diff[self.t_player]) > 7:
            if (lastBid + 8 < self.true_value):
                self.random_bid(lastBid)
        else:
            self.random_bid(lastBid)
        pass


    def t_player_bid(self,lastBid):


        if self.code_pos < 4 and len(self.bids_diff[self.who_am_i]) >= 4:
            code = self.engine.math.floor(self.true_value/pow(16,3-self.code_pos))
            self.true_value %= pow(16,3-self.code_pos) 
            self.engine.makeBid(lastBid + code + 8)
            self.code_pos += 1

        if len(self.bids_diff[self.t_player]) == 8:
            self.random_bid(lastBid)
        
        

    def onMyTurn(self,lastBid):
        # lastBid is the last bid that was mad
        
        if self.round == 5:
            #choose 1 player if true value not known based on betting position
            #else choose 1 player with no t_value and 1 with no knowlegde based on position
            i = 1

        if self.round < 4:
            self.engine.makeBid(lastBid+self.code[self.round])
        else:
            if self.t_player == -1:
                self.standard_bid(lastBid)
                
            else:
                if self.who_am_i == self.t_player:
                    self.t_player_bid(lastBid)
                else:
                    self.normal_player_bid(lastBid) 

        if self.round == 0:
            self.who_am_i = self.latest_bidder

        self.round += 1       
        pass

    def onAuctionEnd(self):
        # Now is the time to report team members, or do any cleanup.
        """ self.engine.print(self.bids_diff)
        self.engine.print(self.own_team_list)
        self.engine.print(self.non_npc_list)
        self.engine.print(self.true_value_players)
        self.engine.print([self.true_value]) """
        
        self.engine.reportTeams(self.own_team_list,self.non_npc_list,self.true_value_players)

        

        pass