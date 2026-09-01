import os
import sys
import networkx as nx
import numpy as np

# Ensure SUMO_HOME environment path is accessible
if "SUMO_HOME" in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare environment variable 'SUMO_HOME' before running.")

import traci
from grid_builder import generate_city_grid
from qiga_engine import QIGAEngine

def update_graph_from_sumo(graph):
    # Pulls dynamic vehicle counts from SUMO via TraCI and updates NetworkX edge attributes
    for u, v, data in graph.edges(data=True):
        edge_id = f"e_{u}_{v}" # Standard SUMO naming scheme

        try:
            # Extract live vehicle counts on edge
            vehicle_count = traci.edge.getLastStepVehicleNumber(edge_id)
            mean_speed = traci.edge.getLastStepMeanSpeed(edge_id)

            # Update graph attributes dynamically
            data['current_flow'] = vehicle_count
            if mean_speed > 0:
                data['base_delay'] = data['length']/mean_speed
        except traci.exceptions.TraCIExceptions:
            # Fallback if specific edge ID isn't track during step
            pass

    return graph

def apply_qiga_signals_to_sumo(graph, optimized_plan):
    # Translates binary QIGA chromosome states back into active SUMO traffic light phases
    edges = list(graph.edges())
    for idx, (u, v) in enumerate(edges):
        tlds_id = f"tls_{u}" # Intersections bound to node IDs
        phase_bit = optimized_plan[idx]

        try:
            # Set signal phase state (0 = Hold Red/Main Green, 1 = Cross Green)
            traci.trafficlight.setPhase(tls_id, phase_bit)
        except traci.exceptions.TraCIException:
            pass

def run_sumo_qiga_loop(sumo_cfg_file, steps=1000):
    # Main simulation coupling loop running SUMO alongside dynamic QIGA optimization
    # Start with SUMO in background via TraCI
    traci.start(["sumo", "-c", sumo_cfg_file, "--no-step-log", "true"])

    # Build underlying 4x4 topology abstraction
    graph = generate_city_grid(4, 4)

    print("Connected to SUMO via TraCI. Starting dynamic co-simulation...")

    step = 0
    while step < steps:
        traci.simulationStep()

        # Optimize signals every 60 simulation seconds
        if step % 60 == 0:
            # Refresh network attributes from live traffic
            updated_graph = update_graph_from_sumo(graph)

            # Execute QIGA optimization on live state
            engine = QIGAEngine(updated_graph, pop_size=20, delta_theta=0.03 * np.pi)
            best_delay, best_plan, _ = engine.run_optimization(generation=30)

            # Apply optimized timing vectors directly into SUMO
            apply_qiga_signals_to_sumo(updated_graph, best_plan)
            print(f"Step {step}: Live traffic optimized via QIGA | Est. Network Delay: {best_delay:.2f}s")

        step += 1

    traci.close()
    print("Co-simulation run complete")

if __name__ == "__main__":
    # Test stub for pipeline verification
    print("Connector logic initialized. Ready for SUMO network configuration XML files.")