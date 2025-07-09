"""
Overview

"Tribes is social network of tribes of the Gahuku–Gama alliance structure of the Eastern Central Highlands of New Guinea, from Kenneth Read (1954). The dataset contains a list of all of links, where a link represents signed friendships between tribes" (Rossi & Ahmed, 2015).

Read, K. E. (1954). Cultures of the Central Highlands, New Guinea. Southwestern Journal of Anthropology, 10(1), 1–43. http://www.jstor.org/stable/3629074
Rossi, R., & Ahmed, N. (2015). Tribes. Network Repository. https://networkrepository.com/soc-tribes.php
"""

import numpy as np
import networkx as nx
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

edgeFilename = Path(r'C:\Users\jerem\SCI\soc-tribes_cleaned.edges')
edges = np.loadtxt(edgeFilename,usecols=(0,1),dtype=int)

G = nx.from_edgelist(edges)
directed_G = nx.DiGraph()
directed_G.add_edges_from(edges)

pos_u = nx.shell_layout(G)
pos_d = nx.shell_layout(directed_G)

fig = plt.figure(figsize=(12, 6))
axgrid = fig.add_gridspec(6, 12)

ax0 = fig.add_subplot(axgrid[: , :6 ])
nx.draw(G, pos_u, with_labels=True, ax=ax0, node_size=400, font_size=12)
ax0.set_title("Connections of Gahuku–Gama Tribes - Undirected")

ax1 = fig.add_subplot(axgrid[: , 6: ])
nx.draw(directed_G, pos_d, with_labels=True, ax=ax1, node_size=400, font_size=12)
ax1.set_title("Connections of Gahuku–Gama Tribes - Directed")

fig.tight_layout()
plt.show()

"""
Degree Analysis

    Visualization of the network and two common visualizations of degree distribution.

NetworkX. (n.d.). Degree Analysis. https://networkx.org/documentation/stable/auto_examples/drawing/plot_degree.html
"""

degree_sequence = sorted((d for n, d in G.degree()), reverse=True)
dmax = max(degree_sequence)

fig = plt.figure(figsize=(8,4))
axgrid = fig.add_gridspec(4,8)

ax1 = fig.add_subplot(axgrid[:, :4])
ax1.plot(degree_sequence, "b-", marker="o")
ax1.set_title("Degree Rank Plot")
ax1.set_ylabel("Degree")
ax1.set_xlabel("Rank")

ax2 = fig.add_subplot(axgrid[:, 4:])
ax2.bar(*np.unique(degree_sequence, return_counts=True))
ax2.set_title("Degree Distribution")
ax2.set_xlabel("Degree")
ax2.set_ylabel("# of Nodes")

fig.tight_layout()
plt.show()

"""
Degree Centrality

    Measures how many direct connections a node has.
    
High: Node is highly connected and potentially influential.
Low: Node is peripheral.

Microsoft. (2025). Network Metrics and Their Interpretations (July 8 version) [Large language model]. https://copilot.microsoft.com/shares/pages/PrNXiYNb8CdJ8aqnAkXwZ
"""

degree = nx.degree_centrality(G)

norm = mcolors.Normalize(vmin=min(degree.values())-0.1, vmax=max(degree.values()))
node_colors = [plt.cm.Blues(norm(degree[node])) for node in G.nodes()]

plt.figure(figsize=(6,6))
nx.draw(G, pos_u, with_labels=True, node_size=400, font_size=12, node_color=node_colors)
plt.title("Degree Centrality", fontsize=14)

plt.show()

for node, value in degree.items():
    print(f"Node {node:02}: {value:.4f}")


"""
Average Path Length

    The length of the shortest path between any two nodes in terms of number of edges.
    
Newman, M. (2018). Networks (2nd ed.). Oxford University Press. https://doi.org/10.1093/oso/9780198805090.001.0001
"""
if nx.is_connected(G):
    avg_path_length_u = nx.average_shortest_path_length(G)
    print(f"Average Path Length - Undirected: {avg_path_length_u}")
else:
    print("The undirected graph is not connected, so the average path length is undefined.")

if nx.is_strongly_connected(directed_G):
    avg_path_length_d = nx.average_shortest_path_length(directed_G)
    print(f"Average Path Length - Directed: {avg_path_length_d}")
else:
    print("The directed graph is not strongly connected, so the average path length is undefined.")
    
"""
Assortative Mixing by Degree

    Measures the tendency of nodes to connect to others with similar degree.

Positive: High-degree nodes connect to other high-degree nodes (assortative).
Negative: High-degree nodes connect to low-degree nodes (disassortative).

Microsoft. (2025). Network Metrics and Their Interpretations (July 8 version) [Large language model]. https://copilot.microsoft.com/shares/pages/PrNXiYNb8CdJ8aqnAkXwZ
"""

assortativity_u = nx.degree_assortativity_coefficient(G)
print("Degree Assortativity Coefficient - Undirected:", assortativity_u)

assortativity_d = nx.degree_assortativity_coefficient(directed_G)
print("Degree Assortativity Coefficient - Directed:", assortativity_d)

"""
Eigenvector Centrality

    Refelcts a node's influence based on the importance of its neighbors.

High: Node is connected to other well-connected nodes (central in a global sense).
Low: Node is isolated or connected to low-importance nodes.

Microsoft. (2025). Network Metrics and Their Interpretations (July 8 version) [Large language model]. https://copilot.microsoft.com/shares/pages/PrNXiYNb8CdJ8aqnAkXwZ
"""

u_eigenvector = nx.eigenvector_centrality(G)

u_norm = mcolors.Normalize(vmin=min(u_eigenvector.values())-0.1, vmax=max(u_eigenvector.values()))
u_node_colors = [plt.cm.Reds(u_norm(u_eigenvector[node])) for node in G.nodes()]

d_eigenvector = nx.eigenvector_centrality(directed_G, max_iter=1000)

d_norm = mcolors.Normalize(vmin=min(d_eigenvector.values())-0.1, vmax=max(d_eigenvector.values()))
d_node_colors = [plt.cm.Reds(d_norm(d_eigenvector[node])) for node in directed_G.nodes()]


fig = plt.figure(figsize=(12, 6))
axgrid = fig.add_gridspec(6, 12)

ax0 = fig.add_subplot(axgrid[: , :6 ])
nx.draw(G, pos_u, with_labels=True, ax=ax0, node_size=400, font_size=12, node_color=u_node_colors)
ax0.set_title("Eigenvector Centrality - Undirected")

ax1 = fig.add_subplot(axgrid[: , 6: ])
nx.draw(directed_G, pos_d, with_labels=True, ax=ax1, node_size=400, font_size=12, node_color=d_node_colors)
ax1.set_title("Eigenvector Centrality - Directed")

fig.tight_layout()
plt.show()

for node, value in u_eigenvector.items():
    print(f"u_Node {node:02}: {value:.4f}")
for node, value in d_eigenvector.items():
    print(f"d_Node {node:02}: {value: }")
    
"""
Betweenness Centrality

    Quantifies how often a node lies on shortest paths between other nodes.

High: Node acts as a bridge or gatekeeper in the network.
Low: Node is not critical for information flow.

Microsoft. (2025). Network Metrics and Their Interpretations (July 8 version) [Large language model]. https://copilot.microsoft.com/shares/pages/PrNXiYNb8CdJ8aqnAkXwZ
"""

u_betweenness = nx.betweenness_centrality(G)
    
u_norm = mcolors.Normalize(vmin=min(u_betweenness.values())-0.1, vmax=max(u_betweenness.values()))
u_node_colors = [plt.cm.Greens(u_norm(u_betweenness[node])) for node in G.nodes()]

d_betweenness = nx.betweenness_centrality(directed_G)
    
d_norm = mcolors.Normalize(vmin=min(d_betweenness.values())-0.1, vmax=max(d_betweenness.values()))
d_node_colors = [plt.cm.Greens(d_norm(d_betweenness[node])) for node in directed_G.nodes()]

fig = plt.figure(figsize=(12, 6))
axgrid = fig.add_gridspec(6, 12)

ax0 = fig.add_subplot(axgrid[: , :6 ])
nx.draw(G, pos_u, with_labels=True, ax=ax0, node_size=400, font_size=12, node_color=u_node_colors)
ax0.set_title("Betweenness Centrality - Undirected")

ax1 = fig.add_subplot(axgrid[: , 6: ])
nx.draw(directed_G, pos_d, with_labels=True, ax=ax1, node_size=400, font_size=12, node_color=d_node_colors)
ax1.set_title("Betweenness Centrality - Directed")

fig.tight_layout()
plt.show()

for node, value in u_betweenness.items():
    print(f"u_Node {node:02}: {value:.4f}")
for node, value in d_betweenness.items():
    print(f"d_Node {node:02}: {value:.4f}")

"""
Clustering Coefficient

    Indicates how interconnected a node's neighbors are.

High: Node is in a tightly-knit group or community.
Low: Node's neighbors are loosely connected.

Microsoft. (2025). Network Metrics and Their Interpretations (July 8 version) [Large language model]. https://copilot.microsoft.com/shares/pages/PrNXiYNb8CdJ8aqnAkXwZ
"""

u_clustering = nx.clustering(G)
u_avg_clustering = nx.average_clustering(G)

u_norm = mcolors.Normalize(vmin=min(u_clustering.values())-0.1, vmax=max(u_clustering.values()))
u_node_colors = [plt.cm.Purples(u_norm(u_clustering[node])) for node in G.nodes()]

d_clustering = nx.clustering(directed_G)
d_avg_clustering = nx.average_clustering(directed_G)

d_norm = mcolors.Normalize(vmin=min(d_clustering.values())-0.1, vmax=max(d_clustering.values()))
d_node_colors = [plt.cm.Purples(d_norm(d_clustering[node])) for node in directed_G.nodes()]

fig = plt.figure(figsize=(12, 6))
axgrid = fig.add_gridspec(6, 12)

ax0 = fig.add_subplot(axgrid[: , :6 ])
nx.draw(G, pos_u, with_labels=True, ax=ax0, node_size=400, font_size=12, node_color=u_node_colors)
ax0.set_title("Clustering Coefficient per Node - Undirected")

ax1 = fig.add_subplot(axgrid[: , 6: ])
nx.draw(directed_G, pos_d, with_labels=True, ax=ax1, node_size=400, font_size=12, node_color=d_node_colors)
ax1.set_title("Clustering Coefficient per Node - Directed")

fig.tight_layout()
plt.show()

for node, value in u_clustering.items():
    print(f"u_Node {node:02}: {value:.4f}")
print(f"Average - Undirected:{u_avg_clustering: .4f}")

for node, value in d_clustering.items():
    print(f"d_Node {node:02}: {value:.4f}")
print(f"Average - Directed:{d_avg_clustering: .4f}")