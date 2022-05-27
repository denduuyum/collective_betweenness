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

    # bc_dat = [bc[u] for u in G]
    # cbd_dat = [cbd[u] for u in G]
    # cbs_dat = [cbs[u] for u in G]
    # deg_max = max([G.degree(u) for u in G])
    # deg_dat = [G.degree(u) for u in G]
    # plt.subplot('121')
    # plt.scatter(bc_dat, cbd_dat)
    # plt.plot([0, 0.5], [0, 0.5], color = 'black')
    # plt.xlabel('shortest-path betweenness')
    # plt.ylabel('collective BC / degree')
    # plt.subplot('122')
    # plt.scatter(deg_dat, cbd_dat)
    # plt.plot([0, deg_max], [0, 0.5], color = 'black')
    # plt.xlabel('degree')
    # plt.savefig('fig.png')
    # plt.show()

    frame = []
    for u in G:
        # frame.append((bc[u], cbd[u]))
        frame.append((cc[u], cbc[u], deg[u], bc[u]))

    df = pd.DataFrame(frame, columns = ['closeness', 'collective', 'deg', 'betweenness'])
    # df = pd.DataFrame(frame, columns = ['bc', 'cbd'])
    print(df.corr(method = 'spearman'))
