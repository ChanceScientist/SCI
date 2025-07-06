import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

node_data = {
    'Figure': ['5000301450.001', '5000301450.003', '5000301450.004'],
    'Name': ['1761 Arts Inc.', 'Arlington Area Childcare Inc.', 'Arlington Arts Enrichment Program'],
    'Age': [8, 37, 17],
    'Population': [3, 15, 50]
}  

edge_data = {
    'Source': ['Arlington Arts Enrichment Program', 'Arlington Arts Enrichment Program'],
    'Target': ['1761 Arts Inc.', 'Arlington Area Childcare Inc.'],
    'Weight': [3, 5]
}

df1 = pd.DataFrame(node_data)
df2 = pd.DataFrame(edge_data)

G = nx.Graph()

for _, row in df1.iterrows():
    G.add_node(row['Name'], value1= row['Age'], value2= row['Population'])

for _, row in df2.iterrows():
    G.add_edge(row['Source'], row['Target'], weight=row['Weight'])

    # Color gradient for nodes based on age
    node_values1 = nx.get_node_attributes(G, 'value1')
    cmap = plt.cm.rainbow
    norm = plt.Normalize(vmin=min(node_values1.values()), vmax=max(node_values1.values()))
    node_colors = [cmap(norm(value)) for value in node_values1.values()]

    # Node size determined by degree and population
    node_values2 = nx.get_node_attributes(G, 'value2')
    node_sizes = [100 * G.degree(node) * G.nodes[node]['value2'] for node in G.nodes]

    pos = nx.shell_layout(G)

    nx.draw(G, pos, with_labels=True, node_size=node_sizes, node_color=node_colors)

    # Numerical label and line width based on edge weight
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw(G, pos, with_labels=True, width=[edge_labels[edge] for edge in G.edges], node_size=node_sizes, node_color=node_colors)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

print(df1)
print(df2)
plt.title("SCI Network example")
plt.show()