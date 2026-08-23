# quantum-traffic-optimization
IoT &amp; Quantum-inspired Genetic Algorithms for real-time urban traffic optimization in SUMO

# Phase 1: 9-Intersection QIGA Prototype

This phase establishes the core mathematical framework for the Quantum-Inspired Genetic Algorithm (QIGA) applied to urban traffic signal control.

## Features
- **Quantum Representation:** Uses Q-bit phase angles ($\theta$) on a Bloch-sphere abstraction to represent dynamic traffic signal states.
- **Rotation Gate Updates:** Implements dynamic rotation gates ($\Delta\theta$) to steer population convergence toward global delay minima.
- **Classical Baseline:** Benchmarks QIGA against a Classical Random Search engine across identical traffic parameters.

## Key Results
- **Grid Scale:** 9 static intersections (hardcoded topology).
- **Performance:** QIGA achieved faster convergence and lower total network delay compared to classical search baselines.
- **Outputs:** Saved performance benchmarks in `convergence_chart.png`.

## How to Run
```bash
python phase-1-prototype/run_comparison.py
