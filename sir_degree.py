import sys
import graph_tools
import networkx as nx
import random
import argparse
import matplotlib.pyplot as plt

random.seed()

def arg_setup():
    parser = argparse.ArgumentParser(description='SIR model')
    parser.add_argument('-T', '--niteration', dest='T', type = int, required = True,
                    help='number of test iteration')
    parser.add_argument('file', help = 'The file that contains graph information')
    return parser

class SIR:
    def __init__(self, G, n, x):
        self.G = G
        self.N = n
        self.k = sum([G.degree(u) for u in G]) // n
        self.time = 0
        self.I = [x]
        self.S = [True] * (n + 1)
        self.R = []
        self.nS = n - 1
        self.F = []
        self.done = False

    def step(self):
        self.time += 1
        infected = False
        for u in self.I[:]:
            v = random.randint(1, self.k)
            if v == 1:
                self.I.remove(u)
                self.R.append(u)
            else:
                # print(self.G[u])
                v = random.choice(list(self.G.neighbors(u)))
                if self.S[v]:
                    infected = True
                    self.S[v] = False
                    self.I.append(v)
                    self.nS -= 1

        assert len(self.I) + len(self.R) + self.nS == self.N
        self.F.append(len(self.I) + len(self.R))
        self.done = sum(self.F[-10:]) / 10 == self.F[-1]
        if len(self.F) > 10:
            self.done = True
        # self.done = infected == False

def get_F(G, n, T):
    F = {}
    F10 = {}
    for u in G:
        s = 0
        F10[u] = 0
        for i in range(T):
            sir = SIR(G, n, u)
            while not sir.done:
                sir.step()
            s += sir.F[-1]
            if len(sir.F) <= 10:
                F10[u] += sir.F[-1]
            else:
                F10[u] += sir.F[10]
        F10[u] /= T
        F[u] = s / T

    return F, F10

def plot(A, B):
    x = []
    y = []
    for k in A:
        x.append(B[k])
        y.append(A[k])
    plt.plot(x, y, '.')


def main():
    parser = arg_setup()
    args = parser.parse_args()
    
    with open(args.file) as fin:
        G, n = graph_tools.read_graph(fin)

    F, F10 = get_F(G, n, args.T)
    kF = sorted(F, key=F.get, reverse = True)
    for u in kF:
        print(u, F[u])
    print('-------------------------------------')
    bc = nx.algorithms.centrality.closeness_centrality(G, )
    deg = {}
    for u in G:
        deg[u] = G.degree(u)
    plt.subplot('121')
    plot(F10, bc)
    plt.subplot('122')
    plot(F10, deg)
    plt.show()    

if __name__ == '__main__':
    main()
