from qiga_core import create_base_grid, run_qiga
from classical_baseline import run_classical_random_search

def execute_head_to_head_comparison():
    # --- SIMULATION CONFIGURATION ---
    GENERATIONS = 12
    POP_SIZE = 6
    NUM_LIGHTS = 9

    print("==================================================")
    print("      QIGA VS. CLASSICAL BASELINE RUNNER          ")
    print("==================================================\n")

    # Initialize the exact same road grid network for both algorithms
    shared_grid = create_base_grid()

    # 1. RUN THE QUANTUM-INSPIRED ALGORITHM
    print("[Executing] Running Quantum-Inspired Genetic Algorithm (QIGA)...")

    # Use underscores(_) for the extra variables that you don't care about in this script
    qiga_delay, qiga_plan, qiga_history, _, _, _, _, _ = run_qiga(GENERATIONS, POP_SIZE, NUM_LIGHTS, shared_grid)

    # 2. RUN THE CLASSICAL RANDOM SEARCH ALGORITHM
    print("[Executing] Running Classical Random Search Baseline...")
    classical_delay, classical_plan, classical_history = run_classical_random_search(GENERATIONS, POP_SIZE, NUM_LIGHTS, shared_grid)

    # --- ANALYTICS SUMMARY REPORT ---
    print("\n==================================================")
    print("                COMPARISON REPORT                 ")
    print("==================================================")
    print(f"Target Optimal Layout Constraints : Even lights=0, Odd lights=1")
    print(f"Total Traffic Intersections       : {NUM_LIGHTS} Lights")
    print(f"Evaluation Horizon                : {GENERATIONS} Generations\n")
    
    print(f"🛸 QIGA Best Plan Found           : {qiga_plan}")
    print(f"🛸 QIGA Minimum Total Delay       : {qiga_delay}s")
    print(f"🛸 QIGA Optimization History      : {qiga_history}\n")
    
    print(f"🎲 Classical Best Plan Found      : {classical_plan}")
    print(f"🎲 Classical Minimum Total Delay  : {classical_delay}s")
    print(f"🎲 Classical Optimization History : {classical_history}")
    print("==================================================")

    # Quick text-based convergence check
    if qiga_delay < classical_delay:
        print("🎉 SUCCESS: QIGA successfully outperformed the Classical Baseline!")
    elif qiga_delay == classical_delay:
        print("🤝 TIE: Both found the same minimum delay. Compare generation tracking arrays to see which hit it faster!")
    else:
        print("⚠️ NOTICE: Classical random search found a better layout by luck. Consider expanding parameters.")

if __name__ == "__main__":
    execute_head_to_head_comparison()