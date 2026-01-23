import numpy as np
import random
import math
from scipy.optimize import minimize

# ==========================================
# PART A: OPTIMAL SENSOR PLACEMENT (Geometric Median)
# ==========================================
def calculate_total_distance(hub, sensors):
    """
    Objective function to minimize: Sum of Euclidean distances.
    """
    total_dist = 0
    for s in sensors:
        total_dist += np.sqrt((s[0] - hub[0])**2 + (s[1] - hub[1])**2)
    return total_dist

def solve_sensor_placement(sensors):
    # FIX: Ensure initial_guess is a flat 1D array [x, y], not [[x, y]]
    initial_guess = np.mean(sensors, axis=0)
    
    # Use standard optimization (Nelder-Mead) to find the minimum
    result = minimize(calculate_total_distance, initial_guess, args=(sensors,), method='Nelder-Mead')
    
    return result.x, result.fun

# ==========================================
# PART B: TSP WITH SIMULATED ANNEALING
# ==========================================
def total_tour_length(tour, dist_matrix):
    length = 0
    for i in range(len(tour)):
        # Distance from current city to next (wrapping around to start)
        length += dist_matrix[tour[i]][tour[(i + 1) % len(tour)]]
    return length

def simulated_annealing(cities, schedule_type='linear'):
    # Precompute distances
    n = len(cities)
    dist_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            dist_matrix[i][j] = np.linalg.norm(cities[i] - cities[j])

    # Initial State
    current_tour = list(range(n))
    random.shuffle(current_tour)
    current_cost = total_tour_length(current_tour, dist_matrix)
    
    best_tour = list(current_tour)
    best_cost = current_cost
    
    # Parameters
    T = 1000.0
    T_min = 1.0
    alpha = 0.99   # For exponential
    beta = 0.5     # For linear
    
    while T > T_min:
        # Create Neighbor: Swap two random cities
        i, j = random.sample(range(n), 2)
        new_tour = list(current_tour)
        new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
        
        new_cost = total_tour_length(new_tour, dist_matrix)
        
        # Acceptance Probability
        delta = new_cost - current_cost
        if delta < 0 or random.random() < math.exp(-delta / T):
            current_tour = new_tour
            current_cost = new_cost
            
            if current_cost < best_cost:
                best_cost = current_cost
                best_tour = list(current_tour)
        
        # Cooling Schedules
        if schedule_type == 'exponential':
            T = T * alpha
        else: # linear
            T = T - beta
            
    return best_cost, best_tour

# ==================== RUNNER ====================
if __name__ == "__main__":
    print("--- Q1 Part A: Sensor Placement ---")
    # Example 1 Data from Assignment Brief
    sensors = np.array([[0,1], [1,0], [1,2], [2,1]])
    
    hub_loc, min_dist = solve_sensor_placement(sensors)
    
    print(f"Optimal Hub Location: {hub_loc}")
    print(f"Minimum Total Distance: {min_dist:.5f}") # Expected: 4.00000

    print("\n--- Q1 Part B: TSP Simulated Annealing ---")
    # Generate random cities
    num_cities = 20
    cities = np.random.rand(num_cities, 2) * 1000
    
    cost_lin, _ = simulated_annealing(cities, 'linear')
    cost_exp, _ = simulated_annealing(cities, 'exponential')
    
    print(f"Final Cost (Linear Schedule): {cost_lin:.2f}")
    print(f"Final Cost (Exponential Schedule): {cost_exp:.2f}")