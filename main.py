import racetrack
import optimize
import pickle
import betting



with open("prereqs.pickle","rb") as p:
    prereq = pickle.load(p)

races = prereq[0].keys()

          # w     p     s
winloss = [[0,0],[0,0],[0,0]]

for race in races:
    ranks = betting.evaluate_race(race,prereq)
    betting.AbstractBet.set_ranks(ranks) # not safe for parallelism!!!
    odds = optimize.BetProblem.odds_dict(prereq,race)
    b = optimize.BetProblem(ranks,odds)

    stop = False
    while not stop:
        n,stop = b.next_best()
        b.state.append(n)
        b.state = optimize.BetProblem.merge_state(b.state)

    for result in racetrack.winloss(race,b.state,prereq[0]):
        if result[1] == "W":
            i1 = 0 
        elif result[1] == "P":
            i1 = 1
        elif result[1] == "S":
            i1 = 2

        if result[0]:
            i2 = 0
        else:
            i2 = 1

        winloss[i1][i2] += 1

    print(winloss)
