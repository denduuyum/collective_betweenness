import networkx as nx
import math
import numpy as np
import graph_tools
import sys
import matplotlib.pyplot as plt
import ast

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

def get_size(bc, u):
    mn = min(bc.values())
    mx = max(bc.values())
    return 10 + bc[u] * (1000 - 10) / (mx - mn)

def plot(A, B):
    x = []
    y = []
    for k in A:
        x.append(A[k])
        y.append(B[k])

    plt.plot(x, y, '.', markersize=2, color='black')
    m, b = np.polyfit(x, y, 1)
    plt.plot(x, [m*_x+b for _x in x], '--', linewidth = 1)
    # plt.plot([min(x), max(x)], [min(y), max(y)], '--', linewidth = 1)


datasets = [("net.txt", "netscience"), ("email_converted.txt", "email")]
plt.rcParams.update({'figure.figsize': (20, 10)})
i = 0
for fname, name in datasets:
    with open(fname) as fin:
        G, n = graph_tools.read_graph(fin)

    bc = nx.algorithms.centrality.betweenness_centrality(G)
    cbc = collective_bc_sum(G, bc, 1);
    cc = nx.algorithms.centrality.closeness_centrality(G)
    deg = {}
    for u in G:
        deg[u] = G.degree(u)
    id = len(datasets) * 100 + 30 + i * 3 + 1
    ax = plt.subplot(id)
    plot(cc, cbc)
    ax.set_title(name + '  ', loc = 'right', y = 0)
    ax.set_xlabel('closeness')
    id = len(datasets) * 100 + 30 + i * 3 + 2
    ax = plt.subplot(id)
    plot(deg, cbc)
    ax.set_xlabel('degree')
    ax.set_title(name + '  ', loc = 'right', y = 0)
    id = len(datasets) * 100 + 30 + i * 3 + 3
    ax = plt.subplot(id)
    plot(bc, cbc)
    ax.set_xlabel('betweenness')
    ax.set_title(name + '  ', loc = 'right', y = 0)
    i += 1

# ax.set_title('   sawmill', loc = 'left', y = 0)
# plt.savefig('sawmill.png')
# plt.savefig('sawmill.eps')
# plt.savefig('sawmill.tiff')
# plt.savefig('sawmill.pdf')
# plt.savefig('sawmill.svg')
plt.tight_layout()
plt.savefig('figure3.png')
plt.savefig('figure3.eps')
plt.savefig('figure3.tiff')
plt.savefig('figure3.pdf')
plt.savefig('figure3.svg')

plt.show()
