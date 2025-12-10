"""
tools for representing bets made on horses
"""

import math
import trueskill as ts
import itertools
import rank
import pickle

def evaluate_race(race: str, prereq):
    data,Q= prereq
    r = rank.gen_rankings(race,data,Q)
    ranks = { k.horse:r[k.horse] for k in data[race]}
    ranks = list(ranks.items())
    ranks.sort(key=lambda h: h[1],reverse=True)
    ranks = dict(ranks)
    return ranks

# abstract class to hold bet functions
class AbstractBet():
    DIMINISH = 0.2 # diminishing factor for repeated bets
    # https://trueskill.org/#win-probability
    # modified for 1v1
    @staticmethod
    def __win_probability_1v1(p1, p2):
        delta_mu = p1.mu - p2.mu
        sum_sigma = sum(r.sigma ** 2 for r in itertools.chain((p1,), (p2,)))
        size = 2
        denom = math.sqrt(size * (ts.BETA * ts.BETA) + sum_sigma)
        tsenv = ts.global_env()
        return tsenv.cdf(delta_mu / denom)

    """
    It is quite likely that nothing here is statistically sound and I am pulling
    this shit out of thin air
    """

    def __init__(self, horse: str, dollarodds: int = 0, bet: int = 1) -> None:
        self.horse = horse
        self.odds = float(dollarodds)
        self.bet = bet
        return None

    ranks = None

    @staticmethod
    def set_ranks(ranks: dict[str,ts.Rating]) -> None:
        AbstractBet.ranks = ranks
        return None
    
    def prob(self):
        # must be re-implemented by subclasses!
        return 0
    
    def payout(self):
        return self.odds*self.bet + self.bet
    
    def prob_payout(self):
        return float(self.payout())*self.prob()
    
    def dimm_payout(self):
        return self.prob_payout()-(AbstractBet.DIMINISH*(self.bet**2))
    
class Win(AbstractBet):
    def prob(self):
        # odds of winning first place
        odds = 1
        for h,r in AbstractBet.ranks.items():
            if h == self.horse:
                continue
            odds *= AbstractBet._AbstractBet__win_probability_1v1(AbstractBet.ranks[self.horse],r)
        return odds

class Place(AbstractBet):
    def prob(self):
        # odds of winning first place
        odds = 1
        for h,r in AbstractBet.ranks.items():
            if h == self.horse:
                continue
            odds *= AbstractBet._AbstractBet__win_probability_1v1(AbstractBet.ranks[self.horse],r)
        return odds*2 # not true, fix this!
    
    def payout(self):
        # estimated payout not based on reality
        return (self.odds*(2/3))*self.bet + self.bet

class Show(AbstractBet):
    def prob(self):
        # odds of winning first place
        odds = 1
        for h,r in AbstractBet.ranks.items():
            if h == self.horse:
                continue
            odds *= AbstractBet._AbstractBet__win_probability_1v1(AbstractBet.ranks[self.horse],r)
        return odds*3   # not true, fix this!
    
    def payout(self):
        # estimated payout not based on reality!
        return (self.odds*(1/3))*self.bet + self.bet