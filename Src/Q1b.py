"""
Module: Task1b.py
Problem: The Traveling Salesperson Problem (TSP)
Method: Simulated Annealing (SA)
Description: A modular implementation to find near-optimal routes using 
Metropolis criteria and custom cooling schedules.
"""

import math
import random

# CORE GEOMETRY & EVALUATION

def get_euclidean_dist(c1, c2):
    """Calculates the straight-line distance between two city coordinates."""
    return math.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)

def calculate_tour_cost(route, city_data):
    """
    Computes the total distance of a Hamiltonian cycle.
    Includes the return trip from the last city back to the first.
    """
    total = 0.0
    for i in range(len(route)):
        # Calculate distance between current city and next (with wrap-around)
        total += get_euclidean_dist(city_data[route[i]], city_data[route[(i + 1) % len(route)]])
    return total

# NEIGHBORHOOD OPERATORS

def apply_2opt_move(route):
    """
    Implements the 2-opt neighborhood operator.
    Reverses a segment of the tour to eliminate self-intersections.
    Example: [A, B, C, D, E] -> [A, D, C, B, E]
    """
    new_route = route[:]
    # Select two distinct indices for the segment reversal
    i, j = sorted(random.sample(range(len(route)), 2))
    new_route[i:j+1] = reversed(new_route[i:j+1])
    return new_route

# COOLING SCHEDULE STRATEGIES

class ExponentialCooler:
    """T = T_initial * alpha^k [cite: 79]"""
    def __init__(self, t_start, alpha):
        self.t_start = t_start
        self.alpha = alpha

    def get_temp(self, k):
        return self.t_start * (self.alpha ** k)

class LinearCooler:
    """T = T_initial - beta * k [cite: 79]"""
    def __init__(self, t_start, beta):
        self.t_start = t_start
        self.beta = beta

    def get_temp(self, k):
        return max(0.001, self.t_start - (self.beta * k))


# SIMULATED ANNEALING ENGINE

class SimulatedAnnealingTSP:
    def __init__(self, city_coords):
        self.cities = city_coords
        self.n = len(city_coords)

    def run_optimization(self, scheduler, max_steps=10000):
        # 1. Generate Initial State: Random Permutation 
        current_state = list(range(self.n))
        random.shuffle(current_state)
        current_cost = calculate_tour_cost(current_state, self.cities)
        
        best_state = current_state[:]
        best_cost = current_cost
        
        for k in range(max_steps):
            temp = scheduler.get_temp(k)
            if temp <= 0.001: break
            
            # 2. Generate Neighbor via 2-opt [cite: 77, 78]
            candidate = apply_2opt_move(current_state)
            candidate_cost = calculate_tour_cost(candidate, self.cities)
            
            # 3. Metropolis Acceptance Criterion
            delta = candidate_cost - current_cost
            if delta < 0 or random.random() < math.exp(-delta / temp):
                current_state = candidate
                current_cost = candidate_cost
                
                # Update global best
                if current_cost < best_cost:
                    best_cost = current_cost
                    best_state = current_state[:]
                    
        return best_state, best_cost


# PERFORMANCE ANALYSIS


if __name__ == "__main__":
    print("="*60)
    print("TSP OPTIMIZER: SIMULATED ANNEALING ANALYSIS")
    print("="*60)

    # Initialize N cities with random coordinates [0, 1000] [cite: 72]
    N_CITIES = 40 
    random_cities = [[random.uniform(0, 1000), random.uniform(0, 1000)] for _ in range(N_CITIES)]
    
    optimizer = SimulatedAnnealingTSP(random_cities)
    
    # Run Experiment 1: Exponential
    exp_schedule = ExponentialCooler(t_start=500.0, alpha=0.999)
    path_exp, cost_exp = optimizer.run_optimization(exp_schedule)
    print(f"Exponential Schedule Result: {cost_exp:.2f} units")
    
    # Run Experiment 2: Linear
    lin_schedule = LinearCooler(t_start=500.0, beta=0.05)
    path_lin, cost_lin = optimizer.run_optimization(lin_schedule)
    print(f"Linear Schedule Result:      {cost_lin:.2f} units")
    
    print("-" * 60)
    winner = "Exponential" if cost_exp < cost_lin else "Linear"
    print(f"Optimal Strategy for this instance: {winner}")
    print("="*60)