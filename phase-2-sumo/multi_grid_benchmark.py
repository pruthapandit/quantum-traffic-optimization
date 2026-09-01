import time
import numpy as np
import matplotlib.pyplot as plt
from grid_builder import generate_city_grid
from qiga_engine import QIGAEngine
from run_phase2_benchmark import run_classical_baseline

def benchmark_grid_scale(dimensions, generations=150, pop_size=20):
    grid_results = {}

    for dim in dimensions:
        rows, cols = dim
        print(f"\n──────────────────────────────────────────")
        print(f"Testing Grid Scale: {rows}x{cols}")

        # Generate grid topology
        grid = generate_city_grid(rows, cols)
        num_edges = grid.number_of_edges()
        print(f"Nodes: {grid.number_of_nodes()} | Edges (Q-bits): {num_edges}")

        # Run classical baseline
        start_time = time.time()
        classical_hist = run_classical_baseline(grid, pop_size=pop_size, generations=generations)
        classical_time = time.time() - start_time

        # Run QIGA Engine
        # Scale theta step size slightly smaller for larger grids to prevent premature lock-in
        step_size = 0.04 * np.pi if num_edges <= 48 else 0.03 * np.pi
        engine = QIGAEngine(grid, pop_size=pop_size, delta_theta=step_size)

        start_time = time.time()
        best_delay, best_plan, qiga_hist = engine.run_optimization(generations=generations)
        qiga_time = time.time() - start_time

        # Record Metrics
        classical_improvement = ((classical_hist[0] - classical_hist[-1])/classical_hist[0]) * 100
        qiga_improvement = ((qiga_hist[0] - best_delay)/qiga_hist[0]) * 100

        grid_results[f"{rows}x{cols}"] = {
            'edges': num_edges, 
            'classical_hist': classical_hist, 
            'qiga_hist': qiga_hist, 
            'classical_time': classical_time, 
            'qiga_time': qiga_time, 
            'qiga_improvement': qiga_improvement
        }

    print(f"QIGA Delay Reduction: {qiga_improvement:.2f}% (Execution Time: {qiga_time:.2f}s)")
    print(f"Classical Delay Reduction: {classical_improvement:.2f}% (Execution Time: {classical_time:.2f}s)")

    return grid_results

def plot_scalability_results(results, generations=150):
    fig, axes = plt.subplots(1, 3, figsize=(18, 5), sharey=False)
    grid_keys = list(results.keys())

    for idx, key in enumerate(grid_keys):
        res = results[key]
        ax = axes[idx]

        ax.plot(range(1, generations + 1), res['classical_hist'], label="Classical Baseline", color = "red", linestyle="--")
        ax.plot(range(1, generations + 1), res['qiga_hist'], label="Dynamic QIGA", color="blue", linewidth=2)

        ax.set_title(f"Grid Size: {key} ({res['edges']} Q-bits)", fontsize=12, fontweight='bold')
        ax.set_xlabel("Generations")
        if idx == 0:
            ax.set_ylabel("Total Network Delay (s)")
        ax.legend()
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    chart_path = "phase-2-sumo/multi_grid_scalability_chart.png"
    plt.savefig(chart_path)

if __name__ == "__main__":
    # Benchmark 3x3 (24 edges), 4x4 (48 edges), 5x5 (80 edges)
    grid_dimensions = [(3, 3), (4, 4), (5, 5)]
    print("Starting Phase 2 Multi-Scalability Benchmark...")

    benchmark_data = benchmark_grid_scale(grid_dimensions, generations=150)
    plot_scalability_results(benchmark_data, generations=150)
    