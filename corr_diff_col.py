import pandas as pd
import networkx as nx
import sys
import copy
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

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

def collective_bc(G, bc):
    cbc = {}
    for u in G:
        s = 0
        for v in G[u]:
            s += bc[v]
        cbc[u] = s * bc[u]
    return cbc

def collective_bc_deg(G, bc):
    cbc = {}
    for u in G:
        s = 0
        for v in G[u]:
            s += bc[v]
        cbc[u] = s * G.degree(u)
    return cbc

def find_bdc(G, bc):
    bdc = {}
    for u in G:
        bdc[u] = bc[u] / G.degree(u)
    return bdc



if __name__ == '__main__':

    with open(sys.argv[1]) as fin:
        G, n = read_graph(fin)

    bc = nx.algorithms.centrality.betweenness_centrality(G)
    # cbc = collective_bc(G, bc)
    cbd = collective_bc_deg(G, bc)
    # cbd = collective_bc(G, bc)
    # bdc = find_bdc(G, bc)
    bc_dat = [bc[u] for u in G]
    cbd_dat = [cbd[u] for u in G]
    norm = Normalize()
    diffs = [abs(bc[u] - cbd[u]) for u in G]
    log_dat = norm(diffs)
    cols = [(1 - x, 1 - x, 1, 1) for x in log_dat]
    labels = {}
    for u in G:
        labels[u] = G.degree(u)
    print(cols)
    nx.draw(G, node_color = cols, labels = labels)
    ax = plt.gca()
    ax.collections[0].set_edgecolor("#000000")

    plt.savefig('graph.png')
    plt.show()
