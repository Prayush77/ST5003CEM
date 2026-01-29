"""
Module: Task6.py
Problem: Robot Parcel Delivery (Poland Network)
Method: Functional Search Algorithms (DFS, BFS, A*)
Description: Implements uninformed and informed search strategies to find 
paths from Glogow (Start) to Plock (Goal) using Diagram (a) for 
actual distances and Diagram (b) for heuristics.
"""

from collections import deque
import heapq
from typing import Tuple, List, Dict, Optional, Set

# ============================================================================
# 1. STATE SPACE & HEURISTICS (Data Modeling)
# ============================================================================

# Actual distances between cities in Poland from Diagram (a) [cite: 329-367]
POLAND_MAP = {
    'Glogow': {'Leszno': 45, 'Wroclaw': 140},
    'Leszno': {'Glogow': 45, 'Poznan': 90, 'Kalisz': 140, 'Wroclaw': 100},
    'Wroclaw': {'Leszno': 100, 'Glogow': 140, 'Kalisz': 160, 'Częstochowa': 118, 'Opole': 100},
    'Poznan': {'Bydgoszcz': 140, 'Konin': 120, 'Kalisz': 130, 'Leszno': 90},
    'Bydgoszcz': {'Poznan': 140, 'Włocławek': 110},
    'Włocławek': {'Bydgoszcz': 110, 'Plock': 55, 'Konin': 120},
    'Plock': {'Włocławek': 55, 'Warsaw': 130},
    'Konin': {'Włocławek': 120, 'Poznan': 120, 'Kalisz': 120, 'Lodz': 120},
    'Kalisz': {'Poznan': 130, 'Konin': 120, 'Lodz': 160, 'Wroclaw': 160, 'Leszno': 140},
    'Warsaw': {'Plock': 130, 'Lodz': 150, 'Radom': 105},
    'Lodz': {'Warsaw': 150, 'Konin': 120, 'Kalisz': 160, 'Częstochowa': 128, 'Radom': 165},
    'Radom': {'Warsaw': 105, 'Lodz': 165, 'Kielce': 82, 'Kraków': 280},
    'Częstochowa': {'Wroclaw': 118, 'Lodz': 128, 'Katowice': 80},
    'Opole': {'Wroclaw': 100, 'Katowice': 85},
    'Katowice': {'Częstochowa': 80, 'Opole': 85, 'Kraków': 85},
    'Kielce': {'Radom': 82, 'Kraków': 120},
    'Kraków': {'Katowice': 85, 'Kielce': 120, 'Radom': 280}
}

# Straight-line distances (Heuristic h(n)) to Plock from Diagram (b) [cite: 290-328]
H_PLOCK = {
    'Bydgoszcz': 90, 'Wloclawek': 44, 'Plock': 0, 'Konin': 96,
    'Poznan': 107, 'Warsaw': 95, 'Lodz': 118, 'Leszno': 103,
    'Kalisz': 107, 'Radom': 91, 'Glogow': 40, 'Wroclaw': 80,
    'Częstochowa': 90, 'Kielce': 102, 'Opole': 190, 'Kraków': 68,
    'Katowice': 61
}

# ============================================================================
# 2. SEARCH ALGORITHMS
# ============================================================================

def depth_first_search(start: str, goal: str) -> Optional[List[str]]:
    """1a. DFS using Stack (Open) and Set (Closed) containers."""
    open_stack = [(start, [start])]
    closed_set = set()

    while open_stack:
        current, path = open_stack.pop()
        if current == goal: return path
        
        if current not in closed_set:
            closed_set.add(current)
            # Add neighbors to stack in reverse to maintain typical DFS order
            for neighbor in reversed(list(POLAND_MAP.get(current, {}).keys())):
                if neighbor not in closed_set:
                    open_stack.append((neighbor, path + [neighbor]))
    return None

def breadth_first_search(start: str, goal: str) -> Optional[List[str]]:
    """1b. BFS using Queue (Open) and Set (Closed) containers."""
    open_queue = deque([(start, [start])])
    closed_set = {start}

    while open_queue:
        current, path = open_queue.popleft()
        if current == goal: return path
        
        for neighbor in POLAND_MAP.get(current, {}):
            if neighbor not in closed_set:
                closed_set.add(neighbor)
                open_queue.append((neighbor, path + [neighbor]))
    return None

def a_star_search(start: str, goal: str) -> Tuple[Optional[List[str]], int]:
    """2. A* algorithm using f(n) = g(n) + h(n) logic."""
    # Open priority queue: (f_score, actual_g_score, current_node, current_path)
    open_pq = [(H_PLOCK[start], 0, start, [start])]
    closed_costs = {start: 0}

    while open_pq:
        f, g, current, path = heapq.heappop(open_pq)
        
        if current == goal: return path, g
        
        for neighbor, weight in POLAND_MAP.get(current, {}).items():
            new_g = g + weight
            # Only proceed if we found a cheaper way to this neighbor
            if neighbor not in closed_costs or new_g < closed_costs[neighbor]:
                closed_costs[neighbor] = new_g
                f_score = new_g + H_PLOCK.get(neighbor, 999)
                heapq.heappush(open_pq, (f_score, new_g, neighbor, path + [neighbor]))
    return None, 0

# ============================================================================
# 3. ANALYSIS & EXECUTION
# ============================================================================

def calculate_path_distance(path):
    """Calculates total road distance of a given path."""
    dist = 0
    for i in range(len(path) - 1):
        dist += POLAND_MAP[path[i]][path[i+1]]
    return dist

if __name__ == "__main__":
    start_city, target_city = 'Glogow', 'Plock'
    
    print("-" * 65)
    print(f"ROBOT DELIVERY TASK: {start_city} to {target_city}")
    print("-" * 65)

    # 1a. DFS Results
    dfs_path = depth_first_search(start_city, target_city)
    print(f"DFS Path: {' -> '.join(dfs_path)} (Dist: {calculate_path_distance(dfs_path)})")

    # 1b. BFS Results
    bfs_path = breadth_first_search(start_city, target_city)
    print(f"BFS Path: {' -> '.join(bfs_path)} (Dist: {calculate_path_distance(bfs_path)})")

    # 2. A* Results
    astar_path, astar_cost = a_star_search(start_city, target_city)
    print(f"A* Path:  {' -> '.join(astar_path)} (Dist: {astar_cost})")
    
    print("-" * 65)
    print("Discussion Context:")
    print("- BFS finds the path with fewest nodes but ignores road distance.")
    print("- DFS explores deep branches but often results in suboptimal path lengths.")
    print("- A* utilizes heuristics to minimize actual travel distance efficiently.")
    print("-" * 65)