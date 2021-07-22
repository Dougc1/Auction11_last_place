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
        self.ph2 = gameParameters["phase"] == "phase_2"
        
    
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
        self.fake_value_players = []
        self.team_t_player = []
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
                if self.ph2 == False:
                    self.true_value_players.append(whoMadeBid)
                    self.t_player = whoMadeBid
                else:
                    self.team_t_player.append(whoMadeBid)

        #updates latest bidder
        self.latest_bidder = whoMadeBid
        pass

    #creates a bid simulating a npc's random bid
    def random_bid_phase1(self,lastBid):
        b = lastBid+(8*(1+2*self.engine.random.random()))
        self.engine.makeBid(self.engine.math.floor(b)) 
        pass

    #bidding when no bot knows the true value
    """ def standard_bid(self,lastBid):
        if (lastBid < self.gameParameters["meanTrueValue"]):
                self.random_bid_phase1(lastBid)
        pass """

    #bidding for a bot which doesn't know the 
    def normal_player_bid(self,lastBid):

        if len(self.bids_diff[self.t_player]) == 8:
            self.true_value = 0
            for i in range(4):
                self.true_value += pow(16,3-i)*(self.bids_diff[self.t_player][4+i] - 8)

        if len(self.bids_diff[self.t_player]) > 7:
            if (lastBid + 8 < self.true_value):
                self.random_bid_phase1(lastBid)
        else:
            self.random_bid_phase1(lastBid)
        pass


    def t_player_bid(self,lastBid):


        if self.code_pos < 4 and len(self.bids_diff[self.who_am_i]) >= 4:
            code = self.engine.math.floor(self.true_value/pow(16,3-self.code_pos))
            self.true_value %= pow(16,3-self.code_pos) 
            self.engine.makeBid(lastBid + code + 8)
            self.code_pos += 1

        if len(self.bids_diff[self.t_player]) == 8:
            self.random_bid_phase1(lastBid)
        
        

    def onMyTurn(self,lastBid):
        # lastBid is the last bid that was mad
        
        if self.round == 5:
            #choose 1 player if true value not known based on betting position
            #else choose 1 player with no t_value and 1 with no knowlegde based on position
            i = 1

        if self.round < 4:
            self.engine.makeBid(lastBid+self.code[self.round])

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
        self.randomness = []
        # Now is the time to report team members, or do any cleanup.
        #self.engine.print(self.bids_diff)
        # go through each bots bids which stores the difference from their current to previous bid
        # calculate the mean
        # standard dev = sqrt(sum(x-mean)^2/n-1)
        for l in self.bids_diff:
            for x in range(len(l)):
                l[x] -= 16

        # runsTest function
        for bot in self.bids_diff:
            bot.sort()
            middle_value = len(bot)//2
            med = bot[middle_value]
            self.randomness.append(self.runsTest(bot,med))
        
        #self.engine.print(self.own_team_list)
        #self.engine.print(self.non_npc_list)
        #self.engine.print(self.true_value_players)
        #self.engine.print([self.true_value])
        self.engine.print(self.randomness)
       # self.engine.reportTeams(self.own_team_list,self.non_npc_list,self.true_value_players)

    # Check randomness 
    def runsTest(self,l, l_median):
        runs, n1, n2 = 0, 0, 0
        
        # Checking for start of new run
        for i in range(len(l)):
            
            # no. of runs
            if (l[i] >= l_median and l[i-1] < l_median) or \
                    (l[i] < l_median and l[i-1] >= l_median):
                runs += 1  
            
            # no. of positive values
            if(l[i]) >= l_median:
                n1 += 1   
            
            # no. of negative values
            else:
                n2 += 1   
    
        runs_exp = ((2*n1*n2)/(n1+n2))+1
        stan_dev = self.engine.math.sqrt((2*n1*n2*(2*n1*n2-n1-n2))/ \
                        (((n1+n2)**2)*(n1+n2-1)))
    
        z = (runs-runs_exp)/stan_dev
        return z
