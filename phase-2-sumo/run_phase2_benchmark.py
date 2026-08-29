import numpy as np
import matplotlib.pyplot as plt
from grid_builder import generate_city_grid
from qiga_engine import QIGAEngine

def run_classical_baseline(graph, pop_size=20, generations=150):
    # Simulates classical random search across idential network topology
    num_edges = graph.number_of_edges()
    best_overall_delay = float('inf')
    delay_history = []

    # Instantiate engine purely for fitness evaluation logic
    eval_engine = QIGAEngine(graph, pop_size=pop_size)

    for _ in range(generations):
        # Generate completely random binary plans (0s and 1s)
        random_plans = np.random.randint(0, 2, size=(pop_size, num_edges))
        delays = eval_engine.evaluate_fitness(random_plans)

        min__delay = np.min(delays)
        if min__delay < best_overall_delay:
            best_overall_delay = min__delay

        delay_history.append(best_overall_delay)

    return delay_history

if __name__ == '__main__':
    # Generate single shared graph
    grid = generate_city_grid(4, 4)
    generations = 150

    # Run Classical Random Search Baseline
    print("Running Classical Baseline...")
    classical_history = run_classical_baseline(grid, pop_size=20, generations=generations)

    # Run QIGA Engine (Tuned delta_theta = 0.03*pi for stable exploration)
    print("Running QIGA Engine...")
    qiga_engine = QIGAEngine(grid, pop_size=20, delta_theta=0.03 * np.pi)
    _, _, qiga_history = qiga_engine.run_optimization(generations=generations)

    # Plot Comparison Chart
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, generations + 1), classical_history, label="Classical Random Search", color="red", linestyle="--")
    plt.plot(range(1, generations + 1), qiga_history, label="Dynamic QIGA Engine", color="blue", linewidth=2)

    plt.title("Phase 2 Optimization Benchmark: 4x4 Grid (48 Edges)")
    plt.xlabel("Generations")
    plt.ylabel("Total Network Delay (Seconds)")
    plt.legend()
    plt.grid(True)

    plt.savefig("phase-2-sumo/phase2_convergence_chart.png")
