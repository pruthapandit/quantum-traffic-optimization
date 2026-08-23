import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def generate_city_grid(rows=3, cols=3, base_capacity=100):
    # Generates an N x M urban traffic grid
    # Returns a NetworkX Directed Graph (DiGraph) representing intersections and road capacities

    G = nx.grid_2d_graph(rows, cols, create_using=nx.DiGraph)

    # Assign random peak traffic loads and capacities to each road edge
    np.random.seed(42) # For reproducible scientific benchmarking
    for (u, v) in G.edges():
        G.edges[u, v]['capacity'] = base_capacity
        G.edges[u, v]['current_flow'] = np.random.randint(20, base_capacity)
        G.edges[u, v]['base_delay'] = np.random.uniform(5.0, 15.0) # seconds

    print(f"Generated {rows}x{cols} City Grid: {G.number_of_nodes()} Intersections, {G.number_of_edges()} Road Segments.")
    return G

if __name__ == '__main__':
    # Test run: Build a 4x4 urban grid (16 intersections, 48 road distrinctions)
    test_grid = generate_city_grid(4, 4)

    # Render and plot the graph layout
    pos = {node: node for node in test_grid.nodes} # Use grid coordinates for positions
    plt.figure(figsize=(6, 6))
    nx.draw(test_grid, pos, with_labels=True, node_color='skyblue', node_size=700, arrowsize=15)
    plt.title("Phase 2: Procedural 4x4 Urban Traffic Grid")
    
    # Save the map preview
    plt.savefig("phase-2-sumo/grid_preview.png")