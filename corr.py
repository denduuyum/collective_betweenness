import pandas as pd
import networkx as nx
import sys
import copy
import matplotlib.pyplot as plt

def read_graph(fin):
    n = int(fin.readline())
    G = nx.Graph()
    
    # print("Number of nodes: ", n)
    while True:
        try:
            line = fin.readline()
        except:
            break

        line = line.split()
        if len(line) == 0:
            break

        x = int(line[0][:-1])
        arr = [int(y) for y in line[1:]]
        for y in arr:
            G.add_edge(x, y)

    return G, n

def dfs(G, u, bc, taken, depth):
    if depth < 0:
        return 0
    if depth == 0:
        return bc[u]
    taken[u] = True
    s = bc[u]
    for v in G[u]:
        if taken.get(v) == None:
            s += dfs(G, v, bc, taken, depth - 1)
    return s
    

def collective_bc_sum(G, bc, depth = 1):
    cbc = {}
    for u in G:
        taken = {}
        cbc[u] = dfs(G, u, bc, taken, depth)
    return cbc

if __name__ == '__main__':

    with open(sys.argv[1]) as fin:
        G, n = read_graph(fin)

    bc = nx.algorithms.centrality.betweenness_centrality(G)
    cc = nx.algorithms.centrality.closeness_centrality(G)
    cbc = collective_bc_sum(G, bc, depth = 1)
    deg = nx.algorithms.centrality.degree_centrality(G)

    frame = []
    for u in G:
        # frame.append((bc[u], cbd[u]))
        frame.append((cc[u], cbc[u], deg[u], bc[u]))

    df = pd.DataFrame(frame, columns = ['closeness', 'collective', 'deg', 'betweenness'])
    # df = pd.DataFrame(frame, columns = ['bc', 'cbd'])
    print(df.corr(method = 'spearman'))
