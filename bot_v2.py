from gameEngine import NPCnormalX, NPCnormalY2, linterp
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
        self.minp = gameParameters["minimumBid"]
        self.players = self.gameParameters['numPlayers']
        self.ph2 = self.gameParameters["phase"] == "phase_2"

        #a bunch of math stuff used by the NPC's
        self.NPCnormalX = list(map(lambda x: x/50, range(0,214)))
        self.NPCnormalY = list(map(lambda x: (self.engine.math.e **(-x**2/2))/self.engine.math.sqrt(2*self.engine.math.pi), self.NPCnormalX))
        _sum=0
        self.NPCnormalY2=[]
        for y in self.NPCnormalY:
            self.NPCnormalY2.append(_sum)
            _sum+=y
        self.NPCnormalY2 = list(map(lambda x: x/_sum, self.NPCnormalY2))
        
    
    def onAuctionStart(self, index, trueValue):
        # index is the current player's index, that usually stays put from game to game
        # trueValue is -1 if this bot doesn't know the true value 

        #keeps track of last bid
        self.prev_price = 1
        self.round = 0
        self.bids = 0

        self.who_am_i = index
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
        self.own_team_list = []
        self.non_npc_list = []
        self.true_value_players = []
        self.found_true_values = [-1,-1,-1]
        self.fake_value_players = []
        self.team_t_player = []
        self.t_player = -1
        self.not_penalty_bot = False

        if trueValue == -1:
            self.code = self.team_code
        else:
            self.code = self.t_val_code
        

    def onBidMade(self, whoMadeBid, howMuch):
        # whoMadeBid is the index of the player that made the bid
        # howMuch is the amount that the bid was

        # if bid outside range then they are not an npc
        dif = howMuch - self.prev_price
        if self.ph2:
            if (dif > 239 or dif < 8) and whoMadeBid not in self.non_npc_list:
                    self.non_npc_list.append(whoMadeBid)
        else:
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

        #updates latest bidder
        self.latest_bidder = whoMadeBid
        pass

    #creates a bid simulating a npc's random bid
    def random_bid_phase1(self,lastBid):
        b = lastBid+(8*(1+2*self.engine.random.random()))
        self.engine.makeBid(self.engine.math.floor(b)) 
        pass

    def linterp(self,x,y,x1):
        for i,xn in enumerate(x):
            if x1<xn:
                if (i==0):
                    return y[0]
                else:
                    return y[i-1] + (y[i]-y[i-1]) * (x1-x[i-1]) / (xn - x[i-1])
        return y[len(y)-1]

    def random_bid_phase2(self,lastBid):
        self.engine.makeBid(lastBid + int((1+7 * self.linterp(self.NPCnormalY2,self.NPCnormalX, random.random())) * self.minp))
        pass

    #bidding when no bot knows the true value
    def standard_bid(self,lastBid):
        if (lastBid < self.gameParameters["meanTrueValue"]):
                self.random_bid_phase1(lastBid)
        pass

    #bidding for a bot which doesn't know the true value in phase 1
    def normal_player_bid_p1(self,lastBid):

        if len(self.bids_diff[self.t_player]) == 8:
            self.true_value = 0
            for i in range(4):
                self.true_value += pow(16,3-i)*(self.bids_diff[self.t_player][4+i] - 8)

        if len(self.bids_diff[self.t_player]) > 7:
            dif = self.true_value - lastBid
            if dif > 23:
                    self.random_bid_phase1(lastBid)
            elif dif > 8 and dif <= 23:
                    self.engine.makeBid(dif+lastBid)
        else:
            self.random_bid_phase1(lastBid)

        pass

    def normal_player_bid_p2(self,lastBid):
        dif = self.true_value - lastBid
        if dif > 239:
                self.random_bid_phase1(lastBid)
        elif dif > 8 and dif <= 239:
                self.engine.makeBid(dif+lastBid)
        pass

    #bidding for bots who are given a true value 
    #true value info is sent through bids made
    def t_player_bid(self,lastBid):

        if self.code_pos < 4 and len(self.bids_diff[self.who_am_i]) >= 4:
            code = self.engine.math.floor(self.true_value/pow(16,3-self.code_pos))
            self.true_value %= pow(16,3-self.code_pos) 
            self.engine.makeBid(lastBid + code + 8)
            self.code_pos += 1

        if len(self.bids_diff[self.who_am_i]) == 8:
            self.random_bid_phase1(lastBid)

    #searches to see if a bids made from our own teams reaches eight for any of the bots
    #if so then it decrypts the true value given to that bot and appends it to a list of
    #found true values
    def find_other_t_val(self):

        for index in range(len(self.own_team_list)):
            auction_index = self.own_team_list[index]
            if len(self.bids_diff[auction_index]) == 8:
                found_value = 0
                for i in range(4):
                    found_value += pow(16,3-i)*(self.bids_diff[auction_index][4+i] - 8)
                self.found_true_values[index] = found_value

    #checks the different possiblilties and finds the fake values out of the values given  
    def find_fake_true_value(self):
        if self.found_true_values[0] == self.found_true_values[1]:
            self.true_value = self.found_true_values[0]
            self.fake_value_players.append(self.own_team_list[2])
        elif self.found_true_values[0] == self.found_true_values[2]:
            self.true_value = self.found_true_values[0]
            self.fake_value_players.append(self.own_team_list[1])
        elif self.found_true_values[1] == self.found_true_values[2]:
            self.true_value = self.found_true_values[1]
            self.fake_value_players.append(self.own_team_list[0])

        #appends to change length so function is only run once
        self.found_true_values.append(-1)
        pass


    def onMyTurn(self,lastBid):
        # lastBid is the last bid that was mad
        
        """ if self.round == 5:
            #choose 1 player if true value not known based on betting position
            #else choose 1 player with no t_value and 1 with no knowlegde based on position
            i = 1 """
        
        #the first 4 rounds bots send there code
        if self.round < 4:
                self.engine.makeBid(lastBid+self.code[self.round])
        else:
            if self.ph2 == True:
                #while the true values aren't found then bots are communicating by bidding them
                if len(self.found_true_values) != 4:
                    self.t_player_bid(lastBid) 
                    self.find_other_t_val()
                    #when all values from the bots are found the real true value is found
                    if self.found_true_values[0] != -1 and self.found_true_values[1] != -1 and self.found_true_values[2] != -1:
                        self.find_fake_true_value()
                else:
                    #player who was given the fake value bids accordingly
                    #(players who have the actual true incur a penalty in phase 2 for bidding)
                    if self.who_am_i in self.fake_value_players:
                        self.normal_player_bid_p2(lastBid)

            else:     
                #bidding for phase 1     
                if self.who_am_i == self.t_player:
                    self.t_player_bid(lastBid) 
                else:
                    self.normal_player_bid_p1(lastBid) 

        self.round += 1       
        pass

    def onAuctionEnd(self):
        self.randomness = []
        # Now is the time to report team members, or do any cleanup.
        #self.engine.print(self.bids_diff)
        # go through each bots bids which stores the difference from their current to previous bid
        # calculate the mean
        # standard dev = sqrt(sum(x-mean)^2/n-1)
        """ for l in self.bids_diff:
            for x in range(len(l)):
                l[x] -= 16

        # runsTest function
        for bot in self.bids_diff:
            if len(bot) > 0:
                bot.sort()
                middle_value = int(len(bot)/2)
                med = bot[middle_value]
                self.randomness.append(self.runsTest(bot,med)) """
        
        #self.engine.print(self.own_team_list)
        #self.engine.print(self.non_npc_list)
        #self.engine.print([self.found_true_values])
        #self.engine.print("The current phase is:", self.gameParameters["phase"])
        #self.engine.print([self.true_value])
        #self.engine.print(self.randomness)
        if self.ph2 == False:
            self.engine.reportTeams(self.own_team_list,self.non_npc_list,self.true_value_players)
        else:
            self.engine.reportTeams(self.own_team_list,self.non_npc_list,self.fake_value_players)
        

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
