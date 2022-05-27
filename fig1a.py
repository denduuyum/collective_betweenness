import networkx as nx
import graph_tools
import sys
import matplotlib.pyplot as plt
import ast

with open(sys.argv[1]) as fin:
    G, n = graph_tools.read_graph(fin)

# pos = nx.spring_layout(G)
# with open('fig1_pos.out', 'w') as fout:
#     fout.write(str(pos))
# with open('fig1_pos.out') as fin:
#     pos = ast.literal_eval(fin.read())

nx.draw(G, pos = pos, with_labels = True)
plt.show()
