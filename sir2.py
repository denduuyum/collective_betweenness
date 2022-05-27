import sys
import graph_tools
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

def collective_bc_sum2(G, bc, depth = 1):
    cbc = {}
    for u in G:
        taken = {}
        nodes = nx.descendants_at_distance(G, u, depth) 
        s = 0
        for v in nodes:
            s += bc[v]
        cbc[u] = s
    return cbc


def collective_bc_deg(G, bc, depth = 1):
    cbc = {}
    for u in G:
        taken = {}
        cbc[u] = (dfs(G, u, bc, taken, depth) - bc[u]) / G.degree(u)
    return cbc


class SIR:
    def __init__(self, G, n, x, max_step = None):
        self.G = G
        self.N = n
        self.k = sum([G.degree(u) for u in G]) // n
        self.time = 0
        self.I = [x]
        self.S = [True] * (n + 1)
        self.Itime = [n] * (n + 1)
        self.Itime[x] = 0
        self.R = []
        self.nS = n - 1
        self.F = []
        self.done = False
        self.max_step = max_step

    def step(self):
        self.time += 1
        infected = False
        for u in self.I[:]:
            nodes = []
            for v in self.G[u]:
                # nodes.append(v)
                if self.S[v]:
                    nodes.append(v)
            v = random.randint(1, self.k)
            if v == 1:
                self.I.remove(u)
                self.R.append(u)
            elif len(nodes) > 0:
                v = random.choice(nodes)
                if self.S[v]:
                    infected = True
                    self.Itime[v] = self.time
                    self.S[v] = False
                    self.I.append(v)
                    self.nS -= 1

        assert len(self.I) + len(self.R) + self.nS == self.N
        self.F.append(len(self.I) + len(self.R))
        self.done = len(self.I) == 0
        if self.max_step and len(self.F) > self.max_step:
            self.done = True
        # self.done = infected == False

    def susceptible(G, n, T):
        score = [0] * (n + 1)
        for u in G:
            tmp = [0] * (n + 1)
            for i in range(T):
                sir = SIR(G, n, u)
                while not sir.done:
                    sir.step()
                for i in range(n+1):
                    tmp[i] += sir.Itime[i]
            for i in range(n+1):
                score[i] += tmp[i] / T
                
        return score

def get_F(G, n, T, u, max_step = None):
    F = []
    I = []
    for i in range(T):
        sir = SIR(G, n, u, max_step)
        while not sir.done:
            sir.step()
        F.append(sir.F)
        I.append(sir.Itime)
    return F, I

def calc_f10(G, n, T):
    f10 = {}
    sus = {}

    res_future = []    
    with ThreadPoolExecutor() as executor:
        i = 0
        for u in G:
            f10[u] = 0
            sus[u] = 0
            future = executor.submit(get_F, G, n, T, u, 10)
            res_future.append((u, future))
            i += 1
            if i % 50 == 0:
                for u, res in res_future:
                    F, I = res.result()
                    f10[u] = sum([dat[-1] for dat in F]) / T
                    sus[u] = sum([dat[u] for dat in I]) / T
                res_future.clear()
    
    for u, res in res_future:
        F, I = res.result()
        f10[u] = sum([dat[-1] for dat in F]) / T
        sus[u] = sum([dat[u] for dat in I]) / T
        
    return f10, sus
# def get_F(G, n, T):
#     F = {}
#     F10 = {}
#     for u in G:
#         s = 0
#         F10[u] = 0
#         for i in range(T):
#             sir = SIR(G, n, u)
#             while not sir.done:
#                 sir.step()
#             s += sir.F[-1]
#             if len(sir.F) <= 10:
#                 F10[u] += sir.F[-1]
#             else:
#                 F10[u] += sir.F[10]
#         F10[u] /= T
#         F[u] = s / T

#     return F, F10

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

    # F, F10 = get_F(G, n, args.T)
    F10, sus = calc_f10(G, n, args.T)
    F = F10
    kF = sorted(F, key=F.get, reverse = True)
    for u in kF:
        print(u, F[u])
    print('-------------------------------------')
    bc = nx.algorithms.centrality.betweenness_centrality(G)
    # bc = nx.algorithms.centrality.closeness_centrality(G)
    kbc = sorted(bc, key = bc.get, reverse = True)
    for u in kbc:
        print(u, bc[u])

    print('-------------------------------------')
    cbc = nx.algorithms.centrality.closeness_centrality(G)
    kbc = sorted(cbc, key = cbc.get, reverse = True)
    for u in kbc:
        print(u, cbc[u])        

    print('-------------------------------------')
    cbc_sum = collective_bc_sum(G, bc, 1)
    kbc = sorted(cbc_sum, key = cbc_sum.get, reverse = True)
    for u in kbc:
        print(u, cbc_sum[u])

    # print('-------------------------------------')
    # sus = SIR.susceptible(G, n, args.T)
    # nodes = [i for i in range(min(sus), max(sus)+1)]
    # nodes = sorted(nodes, key=lambda x: sus[x])
    # sus_f10 = {}
    # for u in nodes:
    #     sus_f10[u] = sus[u]
    #     print(u, sus[u])

    deg = nx.algorithms.centrality.degree_centrality(G)

    plt.rcParams.update({'figure.figsize': (20, 4)})

    ax = plt.subplot(151)
    # plt.title('collective degree')
    plt.xscale('log')
    plt.yscale('log')
    ax.set_xlabel('closeness centrality')
    ax.set_ylabel('F(t)')
    ax.set_title(args.name+'    ', loc = 'right', y = 0.01)
    plot(F10, cbc)

    #-----------------------------
    ax = plt.subplot(152)
    # plt.title('collective sum')
    plt.xscale('log')
    plt.yscale('log')
    plot(F10, cbc_sum)
    ax.set_xlabel('collective betweenness')
    ax.set_title(args.name+'    ', loc = 'right', y = 0.01)
    #-----------------------------
    ax = plt.subplot(153)
    # plt.title('collective sum')
    plt.xscale('log')
    plt.yscale('log')
    plot(F10, deg)
    ax.set_xlabel('degree centrality')
    ax.set_title(args.name+'    ', loc = 'right', y = 0.01)
    #-----------------------------
    ax = plt.subplot(154)
    # plt.title('collective sum')
    plt.xscale('log')
    plt.yscale('log')
    plot(F10, bc)
    ax.set_xlabel('betweenness centrality')
    ax.set_title(args.name+'    ', loc = 'right', y = 0.01)

    ax = plt.subplot(155)
    # plt.title('collective')
    plt.xscale('log')
    plt.yscale('log')
    cbc2 = collective_bc_sum2(G, bc, 2)
    plot(F10, cbc2)
    ax.set_xlabel('distance 2')
    ax.set_title(args.name+'    ', loc = 'right', y = 0.01)

    plt.tight_layout()
    if args.output:
        plt.savefig(args.output)
        plt.savefig(args.name + '.png')
        plt.savefig(args.name + '.pdf')
        plt.savefig(args.name + '.svg')
        plt.savefig(args.name + '.eps')
        plt.savefig(args.name + '.tiff')
    # plt.show()

if __name__ == '__main__':
    main()
