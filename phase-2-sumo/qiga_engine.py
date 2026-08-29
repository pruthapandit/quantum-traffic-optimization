import numpy as np
import networkx as nx
from grid_builder import generate_city_grid

class QIGAEngine:
    def __init__(self, graph, pop_size=20, delta_theta=0.03 * np.pi):
        self.G = graph
        self.num_edges = self.G.number_of_edges()
        self.pop_size = pop_size
        self.delta_theta = delta_theta

        # Intiialize the quantum chromosomes with equal superposition (theta = pi/4)
        self.q_pop = np.full((self.pop_size, self.num_edges), np.pi/4)

    def measure_population(self):
        # Collapse Q-bit probabilities into classical binary phase timing plans
        probabilities = np.sin(self.q_pop) ** 2
        random_draws = np.random.rand(self.pop_size, self.num_edges)
        return (random_draws < probabilities).astype(int)

    def evaluate_fitness(self, binary_plans):
        # Calculate total network delay using NetworkX edge attributes
        delays = []
        edges = list(self.G.edges(data=True))

        for plan in binary_plans:
            total_delay = 0
            for idx, (u, v, data) in enumerate(edges):
                signal_state = plan[idx] # 0 or 1 timing phase
                capacity = data['capacity']
                current_flow = data['current_flow']
                base_delay = data['base_delay']

                # Penalty multiplier if traffic flow exceeds capacity under given signal phase 
                effective_delay = base_delay * (1 + (current_flow/capacity) ** 2)
                if signal_state == 0:
                    effective_delay *= 1.35 # Additional hold delay for phase 0

                total_delay += effective_delay
            delays.append(total_delay)
        return np.array(delays)

    def apply_rotation_gates(self, best_plan):
        # Rotates quantum states (theta) toward the generation's champion timing plan
        for i in range(self.pop_size):
            for j in range(self.num_edges):
                target_bit = best_plan[j]
                current_theta = self.q_pop[i, j]

                # Nudge angle toward 0 or pi/2 based on champion bit target
                if target_bit == 1 and current_theta < (np.pi/2):
                    self.q_pop[i, j] += self.delta_theta
                elif target_bit == 0 and current_theta > 0:
                    self.q_pop[i, j] -= self.delta_theta

                # Enforce boundary limits [0, pi/2]
                self.q_pop[i, j] = np.clip(self.q_pop[i, j], 0, np.pi/2)

    def run_optimization(self, generations=150):
        # Runs the full multi-generational QIGA optimization loop
        best_overall_delay = float('inf')
        best_overall_plan = None
        delay_history = []

        for g in range(generations):
            binary_plans = self.measure_population()
            delays = self.evaluate_fitness(binary_plans)

            min_idx = np.argmin(delays)
            current_best_delay = delays[min_idx]
            current_best_plan = binary_plans[min_idx]

            if current_best_delay < best_overall_delay:
                best_overall_delay = current_best_delay
                best_overall_plan = current_best_plan

            delay_history.append(best_overall_delay)
            self.apply_rotation_gates(best_overall_plan)

        return best_overall_delay, best_overall_plan, delay_history

if __name__ == "__main__":
    # Test on a dynamic 4x4 grid
    grid = generate_city_grid(4, 4)
    engine = QIGAEngine(grid, pop_size=20)

    print(f"Running QIGA optimization over 150 generations...")
    best_delay, best_plan, history = engine.run_optimization(generations=150)

    print(f"Optimization Complete!")
    print(f"Initial Delay: {history[0]:.2f}s --> Optimized Delay: {best_delay:.2f}s")
    print(f"Total Delay Reduction: {((history[0] - best_delay) / history[0]) * 100:.2f}%")