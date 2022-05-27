import networkx as nx
import copy
import sys

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

    return G, max([u for u in G])

def read_graph2(fin):
    G = nx.Graph()
    
    while True:
        try:
            line = fin.readline()
        except:
            break

        line = line.split()
        if len(line) == 0:
            break

        x = int(line[0])
        y = int(line[1])
        G.add_edge(x, y)

    return G, max([u for u in G]) + 1
