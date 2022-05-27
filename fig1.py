import sys
import graph_tools
import sir as SR
import networkx as nx
import random
import argparse
import ast
import matplotlib
matplotlib.use('TkAgg', force=True)
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
random.seed()


def arg_setup():
    parser = argparse.ArgumentParser(description='SIR model')
    # parser.add_argument('-T', '--niteration', dest='T', type = int, required = True,
    #                 help='number of test iteration')
    # parser.add_argument('-o', '--output', dest='output', type = str, required = False,
    #                 help='output file name')
    parser.add_argument('-n', '--name', dest='name', type = str, required = False,
                    help='test name')

    
    # parser.add_argument('file', help = 'The file that contains graph information')
    return parser


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
        # nodes = nx.descendants_at_distance(G, u, depth) 
        # s = 0
        # for v in nodes:
        #     s += bc[v]
        # cbc[u] = #len(nodes)#G.degree(u) 
    return cbc

def get_F(G, n, T, u, max_step = None):
    F = []
    I = []
    for i in range(T):
        sir = SR.SIR(G, n, u, max_step)
        while not sir.done:
            sir.step()
        F.append(sir.F)
        I.append(sir.Itime)
    return F, I

def get_final_F(G, n, T):
    res = {}
    for u in G:
        F, I = get_F(G, n, T, u)
        res[u] = sum([f[-1] for f in F]) / T
    return res

def plot(A, B):
    x = []
    y = []
    for k in A:
        x.append(B[k])
        y.append(A[k])

    plt.plot(x, y, '.', markersize=1, color='black')
    # plt.scatter(x, y, s=1, color='black')

def main():
    parser = arg_setup()
    args = parser.parse_args()
    
    # with open(args.file) as fin:
    #     G, n = graph_tools.read_graph(fin)


    plt.rcParams.update({'figure.figsize': (6, 1.8)})
    edges = [(1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (4, 5), (4, 6), (6, 5), (5, 7), (5, 8), (7, 8), (7, 9), (8, 9)]
    G = nx.Graph(edges)
    bc = nx.algorithms.centrality.betweenness_centrality(G)
    cbc = collective_bc_sum(G, bc, 1)
    for u in G:
        print(u, round(bc[u], 2), round(cbc[u], 2))
    # pos = nx.spring_layout(G)
    # with open('fig1_pos.out', 'w') as fout:
    #     fout.write(str(pos))
    with open('fig1a_pos.out') as fin:
        pos = ast.literal_eval(fin.read())

    ax = plt.subplot(121)
    nx.draw_networkx(G, pos = pos, node_color = 'black', edge_color = 'black', node_size = 40, alpha = 0.8, with_labels = False)
    nx.draw_networkx_nodes(G, pos = {1: (-1, 0.58)}, nodelist = [1], node_color='white')
    labels = {4: 'A', 5: 'B', 6: 'C'}
    lpos = {}
    for x in labels:
        lpos[x] = (pos[x][0], pos[x][1] + 0.015)
    nx.draw_networkx_labels(G, pos = lpos, labels = labels)
    ax.set_title('  a)', loc = 'left', y = 0.8)
    #################################################################
    edges = [(1, 2), (2, 3), (3, 4), (4, 1), (5, 1), (6, 2), (7, 3), (8, 4), (1, 9), (2, 9), (3, 9), (4, 9)]
    G = nx.Graph(edges)
    print('-----------------------------------')
    bc = nx.algorithms.centrality.betweenness_centrality(G)
    cbc = collective_bc_sum(G, bc, 1)
    for u in G:
        print(u, round(bc[u], 2), round(cbc[u], 2))

    with open('fig1b_pos.out') as fin:
        pos = ast.literal_eval(fin.read())

    ax = plt.subplot(122)
    nx.draw_networkx(G, pos = pos, node_color = 'black', edge_color = 'black', node_size = 40, alpha = 0.8, with_labels = False)
    nx.draw_networkx_nodes(G, pos = {1: (-0.2, 0.3)}, nodelist = [1], node_color='white')
    labels = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 9: 'E'}
    lpos = {1: [-0.095, 0.14], 2: [0.095, 0.14], 3: [0.095, -0.15], 4: [-0.095, -0.15], 9: [0. , 0.04]}
    nx.draw_networkx_labels(G, pos = lpos, labels = labels)
    ax.set_title('  b)', loc = 'left', y = 0.8)
    plt.tight_layout()
    # plt.show()
    # F = get_final_F(G, n, args.T)
    # bc = nx.algorithms.centrality.betweenness_centrality(G)
    # cc = nx.algorithms.centrality.closeness_centrality(G)
    # cbc = collective_bc_sum(G, bc, 1);
    # print('------------------------------------')
    # nodes = [u for u in G]
    # nodes = sorted(nodes, key = lambda x: cbc[x], reverse = True)
    # for u in nodes:
    #     print(u, cbc[u])

    # print('------------------------------------')
    # nodes = [u for u in G]
    # nodes = sorted(nodes, key = lambda x: F[x], reverse = True)
    # for u in nodes:
    #     print(u, F[u])
    # print('------------------------------------')
    # nodes = [u for u in G]
    # nodes = sorted(nodes, key = lambda x: bc[x], reverse = True)
    # for u in nodes:
    #     print(u, bc[u])
    # print('------------------------------------')
    # nodes = [u for u in G]
    # nodes = sorted(nodes, key = lambda x: cc[x], reverse = True)
    # for u in nodes:
    #     print(u, cc[u])
    
    
    
    
    # plt.tight_layout()
    if args.name:
        plt.savefig(args.name + '.png')
        plt.savefig(args.name + '.pdf')
        plt.savefig(args.name + '.svg')
        plt.savefig(args.name + '.eps')
        plt.savefig(args.name + '.tiff')


if __name__ == '__main__':
    sys.setrecursionlimit(int(1e9))
    main()

