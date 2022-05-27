import networkx as nx
import math
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

with open(sys.argv[1]) as fin:
    G, n = graph_tools.read_graph(fin)

# pos = nx.spectral_layout(G, scale = 500)
# pos = nx.shell_layout(G)
# pos = nx.spring_layout(G, k = 0.1, iterations = 50, scale = 2)
# with open('fig2_net_pos.out', 'w') as fout:
#      fout.write(str(pos))
with open('fig2_net_pos.out') as fin:
    pos = ast.literal_eval(fin.read())

bc = nx.algorithms.centrality.betweenness_centrality(G)
print('------------------------------------')
nodes1 = [u for u in G]
nodes1 = sorted(nodes1, key = lambda x: bc[x], reverse = True)
for u in nodes1:
    print(u, bc[u])

cbc = collective_bc_sum(G, bc, 1);
print('------------------------------------')
nodes2 = [u for u in G]
nodes2 = sorted(nodes2, key = lambda x: cbc[x], reverse = True)
for u in nodes2:
    print(u, cbc[u])
    

# S = [     1,     3,     15,     22,     21,     26,     29,     30,     34] 
# S = [10, 11, 12, 18, 19, 25, 26, 29, 32, 33]
col = []
S = []
for i, u in enumerate(nodes2):
    j = nodes1.index(u)
    if j - i > 126:
        S.append(u)

node_size = []        
for u in G:
    node_size.append(get_size(cbc, u))
    if u in S:
        col.append('red')
    else:
        col.append('white')

plt.rcParams.update({'figure.figsize': (20, 10)})

nx.draw_networkx(G, pos = pos, node_size = node_size, node_color = col, with_labels = False, alpha = 0.3)
nx.draw_networkx_nodes(G, pos = pos, node_size = node_size, node_color = col, edgecolors='black', with_labels = False)
ax = plt.gca()
ax.set_title('   Netscience', loc = 'left', y = 0)
# ax.set_title('   sawmill', loc = 'left', y = 0)
# plt.savefig('sawmill.png')
# plt.savefig('sawmill.eps')
# plt.savefig('sawmill.tiff')
# plt.savefig('sawmill.pdf')
# plt.savefig('sawmill.svg')
plt.tight_layout()
plt.savefig('netscience.png')
plt.savefig('netscience.eps')
plt.savefig('netscience.tiff')
plt.savefig('netscience.pdf')
plt.savefig('netscience.svg')

plt.show()
