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

edgeFilename = Path(r'C:\Users\jerem\Downloads\soc-tribes\soc-tribes_cleaned.edges')
edges = np.loadtxt(edgeFilename,usecols=(0,1),dtype=int)

G = nx.from_edgelist(edges)

"""
Degree Analysis

    Visualization of the network and two common visualizations of degree distribution.

NetworkX. (n.d.). Degree Analysis. https://networkx.org/documentation/stable/auto_examples/drawing/plot_degree.html
"""

degree_sequence = sorted((d for n, d in G.degree()), reverse=True)
dmax = max(degree_sequence)

fig = plt.figure("Degree of Gahuku–Gama Tribes", figsize=(10, 10))
axgrid = fig.add_gridspec(5, 4)

ax0 = fig.add_subplot(axgrid[0:3, :])
Gcc = G.subgraph(sorted(nx.connected_components(G), key=len, reverse=True)[0])
pos = nx.shell_layout(Gcc)
nx.draw_networkx_nodes(Gcc, pos, ax=ax0, node_size=20)
nx.draw_networkx_edges(Gcc, pos, ax=ax0, alpha=0.4)
ax0.set_title("Connections of the Gahuku–Gama Tribes")
ax0.set_axis_off()

ax1 = fig.add_subplot(axgrid[3:, :2])
ax1.plot(degree_sequence, "b-", marker="o")
ax1.set_title("Degree Rank Plot")
ax1.set_ylabel("Degree")
ax1.set_xlabel("Rank")

ax2 = fig.add_subplot(axgrid[3:, 2:])
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
nx.draw(G, pos, with_labels=True, node_size=400, font_size=12, node_color=node_colors)
plt.title("Degree Centrality", fontsize=14)

plt.show()

for node, value in degree.items():
    print(f"Node {node:02}: {value:.4f}")

"""
Assortative Mixing by Degree

    Measures the tendency of nodes to connect to others with similar degree.

Positive: High-degree nodes connect to other high-degree nodes (assortative).
Negative: High-degree nodes connect to low-degree nodes (disassortative).

Microsoft. (2025). Network Metrics and Their Interpretations (July 8 version) [Large language model]. https://copilot.microsoft.com/shares/pages/PrNXiYNb8CdJ8aqnAkXwZ
"""

assortativity = nx.degree_assortativity_coefficient(G)
print(f"Assortative Mixing by Degree: {assortativity: .4f}")

"""
Eigenvector Centrality

    Refelcts a node's influence based on the importance of its neighbors.

High: Node is connected to other well-connected nodes (central in a global sense).
Low: Node is isolated or connected to low-importance nodes.

Microsoft. (2025). Network Metrics and Their Interpretations (July 8 version) [Large language model]. https://copilot.microsoft.com/shares/pages/PrNXiYNb8CdJ8aqnAkXwZ
"""

eigenvector = nx.eigenvector_centrality(G)

norm = mcolors.Normalize(vmin=min(eigenvector.values())-0.1, vmax=max(eigenvector.values()))
node_colors = [plt.cm.Reds(norm(eigenvector[node])) for node in G.nodes()]
    
plt.figure(figsize=(6,6))
nx.draw(G, pos, with_labels=True, node_size=400, font_size=12, node_color=node_colors)
plt.title("Eigenvector Centrality", fontsize=14)

plt.show()

for node, value in eigenvector.items():
    print(f"Node {node:02}: {value:.4f}")

"""
Betweenness Centrality

    Quantifies how often a node lies on shortest paths between other nodes.

High: Node acts as a bridge or gatekeeper in the network.
Low: Node is not critical for information flow.

Microsoft. (2025). Network Metrics and Their Interpretations (July 8 version) [Large language model]. https://copilot.microsoft.com/shares/pages/PrNXiYNb8CdJ8aqnAkXwZ
"""

betweenness = nx.betweenness_centrality(G)
    
norm = mcolors.Normalize(vmin=min(betweenness.values())-0.1, vmax=max(betweenness.values()))
node_colors = [plt.cm.Greens(norm(betweenness[node])) for node in G.nodes()]
    
plt.figure(figsize=(6,6))
nx.draw(G, pos, with_labels=True, node_size=400, font_size=12, node_color=node_colors)
plt.title("Betweenness Centrality", fontsize=14)

plt.show()

for node, value in betweenness.items():
    print(f"Node {node:02}: {value:.4f}")

"""
Clustering Coefficient

    Indicates how interconnected a node's neighbors are.

High: Node is in a tightly-knit group or community.
Low: Node's neighbors are loosely connected.

Microsoft. (2025). Network Metrics and Their Interpretations (July 8 version) [Large language model]. https://copilot.microsoft.com/shares/pages/PrNXiYNb8CdJ8aqnAkXwZ
"""

clustering = nx.clustering(G)

norm = mcolors.Normalize(vmin=min(clustering.values())-0.1, vmax=max(clustering.values()))
node_colors = [plt.cm.Purples(norm(clustering[node])) for node in G.nodes()]
    
plt.figure(figsize=(6,6))
nx.draw(G, pos, with_labels=True, node_size=400, font_size=12, node_color=node_colors)
plt.title("Clustering Coefficient per Node", fontsize=14)

plt.show()

for node, value in clustering.items():
    print(f"Node {node:02}: {value:.4f}")
avg_clustering = nx.average_clustering(G)
print(f"Average Clustering Coefficient:{avg_clustering: .4f}")
