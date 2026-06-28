import matplotlib.pyplot as plt
from qiga_core import create_base_grid, run_qiga
from classical_baseline import run_classical_random_search

def comparison():
    # --- Simulation Values ---
    GENERATIONS = 50
    POP_SIZE = 10
    NUM_LIGHTS = 9

    print(f"--- Launching Traffic Optimization Benchmark ({GENERATIONS} Generations) ---")
    shared_grid = create_base_grid()

    # Run QIGA
    print("Running Quantum-Inspired Genetic Algorithm...")
    qiga_delay, qiga_plan, qiga_history, _, _, _, _, _ = run_qiga(GENERATIONS, POP_SIZE, NUM_LIGHTS, shared_grid)

    # Run Classical Baseline
    print("Running Classical Random Search...")
    classical_delay, classical_plan, classical_history = run_classical_random_search(GENERATIONS, POP_SIZE, NUM_LIGHTS, shared_grid)

    # --- Analytics Summary Report ---
    print("\n==================================================")
    print("                COMPARISON REPORT                 ")
    print("==================================================")
    print(f"Target Optimal Layout Constraints : Even lights=0, Odd lights=1")
    print(f"Total Traffic Intersections       : {NUM_LIGHTS} Lights")
    print(f"Evaluation Horizon                : {GENERATIONS} Generations\n")
    
    print(f"QIGA Best Plan Found           : {qiga_plan}")
    print(f"QIGA Minimum Total Delay       : {qiga_delay}s")
    print(f"QIGA Optimization History      : {qiga_history}\n")
    
    print(f"Classical Best Plan Found      : {classical_plan}")
    print(f"Classical Minimum Total Delay  : {classical_delay}s")
    print(f"Classical Optimization History : {classical_history}")
    print("==================================================")

    # Quick text-based convergence check
    if qiga_delay < classical_delay:
        print("SUCCESS: QIGA successfully outperformed the Classical Baseline!")
    elif qiga_delay == classical_delay:
        print("TIE: Both found the same minimum delay. Compare generation tracking arrays to see which hit it faster!")
    else:
        print("NOTICE: Classical random search found a better layout by luck. Consider expanding parameters.")

    # --- Generate Peformance Plot ---
    plt.figure(figsize=(10,6))
    plt.plot(range(1, GENERATIONS + 1), qiga_history, label="QIGA (Quantum-Inspired)", color='#00d2ff', linewidth=2)
    plt.plot(range(1, GENERATIONS + 1), classical_history, label="Classical Random Baseline", color='#ff3838', linestyle="--", linewidth=2)

    plt.title("Algorithm Convergence: Network Delay Optimization", fontsize=14, fontweight='bold')
    plt.xlabel('Generation/Iteration', fontsize=12)
    plt.ylabel('Minimum Total Network Delay (seconds)', fontsize=12)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(fontsize=11)

    plt.savefig('convergence_chart.png', dpi=300)

if __name__ == "__main__":
    comparison()