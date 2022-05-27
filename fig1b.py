import sys
import graph_tools
import sir as SR
import networkx as nx
import random
import argparse
import matplotlib
matplotlib.use('TkAgg', force=True)
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
random.seed()


def arg_setup():
    parser = argparse.ArgumentParser(description='SIR model')
    parser.add_argument('-T', '--niteration', dest='T', type = int, required = True,
                    help='number of test iteration')
    parser.add_argument('-o', '--output', dest='output', type = str, required = False,
                    help='output file name')
    parser.add_argument('-n', '--name', dest='name', type = str, required = False,
                    help='test name')

    
    parser.add_argument('file', help = 'The file that contains graph information')
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
    
    with open(args.file) as fin:
        G, n = graph_tools.read_graph(fin)


    # plt.rcParams.update({'figure.figsize': (20, 4)})
    F = get_final_F(G, n, args.T)
    bc = nx.algorithms.centrality.betweenness_centrality(G)
    cc = nx.algorithms.centrality.closeness_centrality(G)
    cbc = collective_bc_sum(G, bc, 1);
    print('------------------------------------')
    nodes = [u for u in G]
    nodes = sorted(nodes, key = lambda x: cbc[x], reverse = True)
    for u in nodes:
        print(u, cbc[u])

    print('------------------------------------')
    nodes = [u for u in G]
    nodes = sorted(nodes, key = lambda x: F[x], reverse = True)
    for u in nodes:
        print(u, F[u])
    print('------------------------------------')
    nodes = [u for u in G]
    nodes = sorted(nodes, key = lambda x: bc[x], reverse = True)
    for u in nodes:
        print(u, bc[u])
    print('------------------------------------')
    nodes = [u for u in G]
    nodes = sorted(nodes, key = lambda x: cc[x], reverse = True)
    for u in nodes:
        print(u, cc[u])
    
    
    
    
    # plt.tight_layout()
    # if args.output:
    #     plt.savefig(args.output)
    #     plt.savefig(args.name + '.png')
    #     plt.savefig(args.name + '.pdf')
    #     plt.savefig(args.name + '.svg')
    #     plt.savefig(args.name + '.eps')
    #     plt.savefig(args.name + '.tiff')
    # plt.show()

if __name__ == '__main__':
    sys.setrecursionlimit(int(1e9))
    main()

