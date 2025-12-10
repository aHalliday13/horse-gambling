"""
functions to test and evaluate bets against known results
like a virtual racetrack (idk man they wouldn't let me call it test)
"""

import betting

def winloss(race,bets,data):
    r = data[race]
    order = tuple(h.horse for h in r)
    
    for b in bets:
        place = order.index(b.horse)
        if type(b) == betting.Win:
            for _ in range(b.bet):
                yield place == 0, "W"
        elif type(b) == betting.Place:
            for _ in range(b.bet):
                yield place <= 1, "P"
        elif type(b) == betting.Show:
            for _ in range(b.bet):
                yield place <= 2, "S"
