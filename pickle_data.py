"""
pickle the prereqs so I don't have to wait 5 mins every time I run the program
"""

import pickle
import equibase
import rank
import networkx as nx
import matplotlib.pyplot as plt

print("parsing and deserializing")
# tuple of data dict + graph
prereqs =rank.gen_prereq()

print("pickling")

with open("prereqs.pickle","wb") as p:
    pickle.dump(prereqs,p)