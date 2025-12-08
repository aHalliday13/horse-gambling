"""
Tools for generating TrueSkill rankings based on equibase data
"""
import equibase
import networkx as nx
import matplotlib.pyplot as plt
import trueskill as ts

"""
generate immediate (depth 1) edges for the race dependency digraph
"""
def get_imm_dep_edges(race: str, data: dict[str,list[equibase.Entry]]):
    r = data[race]
    edges = []
    for e in r:
        if e.last_pp is None:
            continue
        nr = str(e.last_pp)
        if nr not in data.keys():
            continue
        edges.append((race,nr))

    return edges

"""
generate big dependency graph
"""
def gen_dep_graph(data: dict[str,list[equibase.Entry]]):
    edges = []
    G = nx.DiGraph()
    for r in data:
        G.add_node(r)
        e = get_imm_dep_edges(r,data)
        edges += e

    G.add_edges_from(edges)
    return G

"""
search the dep graph with dfs, find order races need to be evaluated in, generate rankings
BEFORE specified race
"""
def gen_rankings(race: str, data: dict[str,list[equibase.Entry]], G: nx.DiGraph):
    horse_ranks = {}
    order = list(nx.dfs_postorder_nodes(G,source=race))[:-1]

    # ensure that every horse in this race has a default rating object
    for e in data[race]:
        horse_ranks[e.horse] = ts.Rating()

    # rate every horse in every race that this race depends on
    for rn in order:
        r = data[rn]
        local_ranks = []
        # remember r is sorted already by place
        for e in r:
            if e.horse not in horse_ranks:
                local_ranks.append(ts.Rating())
            else:
                local_ranks.append(horse_ranks[e.horse])
        # convert to list of single element tuples to feed into rate
        hr = [(h,) for h in local_ranks]
        ratings = ts.rate(hr)
        local_ranks = [h for (h,) in ratings]
        
        # put ratings back into horse_ranks
        for i,e in enumerate(r):
            horse_ranks[e.horse] = local_ranks[i]

    return horse_ranks

"""
generate prerequisite data structures for ranking
"""
def gen_prereq():
    chart = equibase.deserialize()[0]
    data = equibase.handle_all_charts(chart)
    G = gen_dep_graph(data)
    return data,G