import numpy as np
import networkx as nx
from qiga_core import create_base_grid, evaluate_fitness

def run_classical_random_search(generations, pop_size, num_lights, grid):
    """
    Simulates a classical random search approach to optimize traffic timings
    """
    best_overall_delay = float('inf')
    best_overall_plan = None
    delay_history = []

    # Match the generational loops of the QIGA algorithm
    for generation in range (1, generations + 1):

        # Generate entirely random binary plans (0s and 1s) that classical computers might try
        # Shape: (pop_lights, num_lights)
        classical_plans = np.random.randint(0, 2, size=(pop_size, num_lights))

        # Evaluate how well these random guesses performed on the grid
        scores, delays = evaluate_fitness(classical_plans, grid)

        # Find the best guess in this current batch
        min_current_delay = min(delays)
        best_current_idx = np.argmin(delays)

        # If this random guess is better than anything before, save it!
        if min_current_delay < best_overall_delay:
            best_overall_delay = min_current_delay
            best_overall_plan = classical_plans[best_current_idx]

        delay_history.append(best_overall_delay)

    return best_overall_delay, best_overall_plan, delay_history

if __name__ == "__main__":
    # Standardize parameters to match the QIGA setup exactly
    GENERATIONS = 10
    POP_SIZE = 5
    NUM_LIGHTS = 9

    grid_network = create_base_grid()

    print("-=- STARTING CLASSICAL RANDOM SEARCH =--")
    best_delay, best_plan, history = run_classical_random_search(GENERATIONS, POP_SIZE, NUM_LIGHTS, grid_network)

    print("\n--- CLASSICAL SEARCH COMPLETE ---")
    print(f"Best Classical Plan Found: {best_plan}")
    print(f"🏆 Minimum Delay Achieved: {best_delay}s")
    print(f"Delay history over 10 generations: {history}")
