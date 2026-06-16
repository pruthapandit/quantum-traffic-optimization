import networkx as nx
import matplotlib.pyplot as plt

# Create a 3x3 grid graph (representing 9 intersections)
G = nx.grid_2d_graph(3, 3)

print("Intersections (Nodes):", G.nodes())
print("Road segments (Edges):", len(G.edges()))

# Set a baseline delay of 10 seconds for all roads
for edge in G.edges():
    G.edges[edge]['weight'] = 10

# Create a massive traffic jam between intersection (0, 1) and (1, 1)
# Bumping its delay weight up to 150 seconds

G.edges[(0, 1), (1, 1)]['weight'] = 150
print("Traffic jam successfully injected between (0, 1) and (1, 1)")

start_node = (0, 0)
end_node = (2, 2)

# Calculate the smartest route based on travel time ('weight')
optimal_path = nx.dijkstra_path(G, source=start_node, target=end_node, weight='weight')
print("Optimal routing path to avoid the traffic jam: ", optimal_path)

# Lay out the grid coordinates cleanly
pos = {node: node for node in G.nodes()}

#Draw the nodes and lines
nx.draw(G, pos, with_labels=True, node_color ='skyblue', node_size=700, font_weight='bold')
plt.title("Phase 1 Sandbox: 3x3 Abstract Urban Traffic Grid")
plt.show()