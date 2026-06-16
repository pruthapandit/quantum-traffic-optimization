import numpy as np
import networkx as nx

def initialize_q_population(pop_size, num_lights):
    """
    Creates a 3D array holding the quantum population.
    Shape: (pop_size, 2, num_lights)
    Row 0 = Alpha values, Row 1 = Beta values
    """
    # 1 / sqrt(2) ensures that |alpha|^2 + |beta|^2  = 0.5 + 0.5 = 1.0
    val = 1.0/np.sqrt(2)

    # Fill the 3D matrix of that size with the starting value
    q_pop = np.full((pop_size, 2, num_lights), val)
    return q_pop

def collapse_wavefunction(q_pop):
    """
    Observes the quantum state and collapses it into a classical binary matrix (0s and 1s).
    Shape: (pop_size, num_lights)
    """
    pop_size, _, num_lights = q_pop.shape

    # Calculate |beta|^2 probabilties for all lights instantly
    beta_squares = q_pop[:, 1, :] ** 2

    # Generate a matrix of random decimals between 0 and 1
    random_matrix = np.random.rand(pop_size, num_lights)

    # If the random number is less than beta^2, it becomes a 1 (True), else 0 (False)
    classical_pop = (random_matrix < beta_squares).astype(int)
    return classical_pop

def create_base_grid():
    """
    Generates a 3x3 traffic grid with baseline road travel times (10 seconds)
    """
    G = nx.grid_2d_graph(3, 3)
    for edge in G.edges():
        G.edges[edge]['delay'] = 10.0 # baseline travel delay in seconds
    return G

def evaluate_fitness(classical_pop, grid):
    """
    Evaluates the total network delay for each individual traffic plan
    Returns an array of fitness scores based on actual graph edge weights. (Higher fitness = Lower total delay)
    """
    pop_size, num_lights = classical_pop.shape
    total_delays = []

    # Get a list of all edge pairs in the network graph to manipulate
    edges = list(grid.edges())

    # Loop through each individual plan in the population
    for i in range(pop_size):
        plan = classical_pop[i]
        
        # Reset all edges to base delay before testing this individual plan
        for edge in edges:
            grid.edges[edge]['delay'] = 10.0

       # Apply the plan's configurations to alter the graph's edge weights
        for light_idx in range(num_lights):
            if light_idx < len(edges):
                target_edge = edges[light_idx]

                # Let's mock a scenario where odd-indexed lights desperately need to be '1' (East-West) and even-indexed lights desperately need to be '0' (North-South)
                # If the binary bit matches the odd/even rule, the road is clear
                # If it doesn't match, the graph edge must be penalized
                if light_idx % 2 == 1 and plan[light_idx] != 1:
                    grid.edges[target_edge]['delay'] = 150.0
                elif light_idx % 2 == 0 and plan[light_idx] != 0:
                    grid.edges[target_edge]['delay'] = 150.0
    
        # Calculate total delay by checking the weights of our graph edges
        network_delay = sum(grid.edges[edge]['delay'] for edge in edges) 
        total_delays.append(network_delay)

    # In genetic algorithms, fitness usually increases for better choices
    # Because we want to MINIMIZE delay, we convert it: Fitness = 10,000 / Total Delay
    fitness_scores = 10000.0 / np.array(total_delays)
    return fitness_scores, total_delays  

def apply_rotation_gate(q_pop, classical_pop, fitness_scores, best_plan):
    """
    Applies the quantum rotation matrix to nudge the alpha/beta amplitudes closer to the configuration of the best-performing classical plan
    """
    pop_size, _, num_lights = q_pop.shape

    # Define a tiny learning angle (Delta Theta) as specified in QIGA literature
    # 0.05 radians is roughly 3 degrees-small adjustments prevent overshooting
    delta_theta = 0.05

    # Loop through every individual and every qubit to apply the rotation
    for i in range(pop_size):
        for j in range(num_lights):
            alpha = q_pop[i, 0, j]
            beta = q_pop[i, 1, j]

            current_bit = classical_pop[i, j]
            best_bit = best_plan[j]

            # Determine rotation direction based on literature lookup table: 
            # Change theta to drive the probabilities toward the champion bit
            if current_bit == 0 and best_bit == 1:
                # Nudge towards beta (1)
                theta = delta_theta
            elif current_bit == 1 and best_bit == 0:
                # Nudge towards alpha (0)
                theta = -delta_theta
            else:
                # If they already match, don't change anything
                theta = 0.0
            
            # Apply the rotation matrix math
            q_pop[i, 0, j] = alpha * np.cos(theta) - beta * np.sin(theta)
            q_pop[i, 1, j] = alpha * np.sin(theta) + beta * np.cos(theta)

    return q_pop

# --- QUICK TEST REGION ---
if __name__ == "__main__":
    # 1. Initialize and collapse a test population
    q_pop = initialize_q_population(pop_size=5, num_lights=9)
    grid_network = create_base_grid()

    print("--- STARTING EVOLUTION ---")
    print("Initial Beta^2 values for first individuals\n", q_pop[0, 1, :] ** 2)
    print()

    # 2. Run the genetic loop for 10 generations
    for generation in range(1, 11):
        # Collapse probabilities into 0s and 1s
        classical_plans = collapse_wavefunction(q_pop)

        # Score them on the NetworkX graph
        scores, delays = evaluate_fitness(classical_plans, grid_network)

        # Find the champion of this generation
        best_idx = np.argmax(scores)
        best_plan = classical_plans[best_idx]

        # Evolve the entire quantum population towards the winner
        q_pop = apply_rotation_gate(q_pop, classical_plans, scores, best_plan)

    # 3. Print the final results after the 10 generations are completely done
    print("--- EVOLUTION COMPLETE ---")
    print("Collapsed Classical Plans from the Final Gen:\n", classical_plans)
    print("\nCalculated Network Delays (in seconds):", delays)
    print("Calculated Fitness Scores (Higher is better)", scores)

    print(f"\n🏆 Individual {best_idx + 1} is the Champion with a final delay of {delays[best_idx]}s!")
    print("\nEvolved Beta^2 values for first individual:\n", q_pop[0, 1, :] ** 2)
