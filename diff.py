import sys
import graph_tools
import networkx as nx
import random
import argparse
import matplotlib
matplotlib.use('TkAgg', force=True)
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor

def arg_setup():
    parser = argparse.ArgumentParser(description='SIR model')
    parser.add_argument('-o', '--output', dest='output', type = str, required = False,
                    help='output file name')
    parser.add_argument('-n', '--name', dest='name', type = str, required = False,
                    help='test name')
    
    parser.add_argument('file', help = 'The file that contains graph information')
    return parser

def dfs(G, u, bc, taken, depth):
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
    parser = arg_setup()
    args = parser.parse_args()
    with open(args.file) as fin:
        G, n = graph_tools.read_graph(fin)

    bc = nx.algorithms.centrality.betweenness_centrality(G, normalized = True)
    cbc = collective_bc_sum(G, bc, 2)
    r1 = [u for u in G]
    r2 = [u for u in G]
    r1 = sorted(r1, key = lambda x : bc[x])
    r2 = sorted(r2, key = lambda x : cbc[x])
    
    node_size = []
    node_col = []
    min_cbc = min([y for x, y in cbc.items()])
    max_cbc = max([y for x, y in cbc.items()])
    print(min_cbc)
    print(max_cbc)
    for u in G:
        node_size.append(int(10 + (cbc[u] - min_cbc) * (1000 - 10) / (max_cbc - min_cbc)))
        i = r1.index(u)
        j = r2.index(u)
        if abs(j - i) >= n / 3:
            node_col.append('red')
        else:
            node_col.append('white')
    print(node_size)
    pos = nx.spring_layout(G)
    with open(args.name + 'pos.out', 'w') as fout:
        fout.write(str(pos))

    nx.draw_networkx_edges(G, pos = pos,
                  edge_color = 'gray',
                  alpha = 0.3,
    )
    nx.draw_networkx_nodes(G, pos = pos,
                           node_size = node_size,
                           node_color = node_col,
                           edgecolors = 'black',
                           label = None
    )
    plt.savefig(args.name + '.png')
    plt.show()

