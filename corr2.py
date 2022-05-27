import pandas as pd
import networkx as nx
import sys
import copy

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


if __name__ == '__main__':

    with open(sys.argv[1]) as fin:
        G, n = read_graph(fin)

    bc = nx.algorithms.centrality.betweenness_centrality(G)
    cbc = collective_bc(G, bc)

    frame = []
    for u in G:
        frame.append((bc[u], cbc[u]))

    df = pd.DataFrame(frame, columns = ['bc', 'cbc'])
    print(df.corr(method = 'spearman'))
