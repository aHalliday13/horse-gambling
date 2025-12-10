"""
Functions for creating an optimized portfolio of bets
"""

import betting
import pickle

class BetProblem():
    RISK = 0.50
    def __init__(self,ranks,odds):
        self.ranks = ranks
        self.odds = odds
        self.state = []

    def next_moves(self):
        b = []
        for Bet in [betting.Win,betting.Place,betting.Show]:
            for horse in self.ranks.keys():
                b.append(Bet(horse,self.odds[horse]))
        return b
    
    @staticmethod
    def odds_dict(prereq,race):
        odds = {}
        for e in prereq[0][race]:
            odds[e.horse] = e.odds
        return odds

    @staticmethod
    def merge_state(state: list):
        for i, b in enumerate(state):
            if i is None:
                continue
            for j, ob in enumerate(state[i+1:],i+1):
                if type(b) == type(ob):
                    if b.horse == ob.horse:
                        # same bet type and same horse
                        b.bet += ob.bet
                        state[j] = None
        nb = []
        for b in state:
            if b is not None:
                nb.append(b)
        return nb
    
    @staticmethod
    def heuristic_payout(state: list):
        state = BetProblem.merge_state(state)
        payout = 0
        for b in state:
            payout += b.dimm_payout()
        return payout
    
    @staticmethod
    def cur_investment(state: list):
        investment = 0
        for b in state:
            investment += b.bet
        return investment

    def next_best(self):
        scores = []
        goal = BetProblem.cur_investment(self.state)*BetProblem.RISK
        nm = self.next_moves()
        for b in nm:
            t_state = self.state + [b]
            t_state = BetProblem.merge_state(t_state)
            p = BetProblem.heuristic_payout(t_state)
            if p < 0:
                # no actual payout will be negative, but the diminishing returns function will cause negative payouts
                continue 
            d = goal-p
            scores.append(d)
        if len(scores) == 0:
            return None,True
        i = scores.index(min(scores))
        return (nm[i], (i<0))
