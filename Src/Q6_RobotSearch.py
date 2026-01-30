import networkx as nx
import matplotlib.pyplot as plt
import heapq
from collections import deque

# ============================================================================
# 1. DATA MODELING (Nepal Names, Coursework Topology)
# ============================================================================

# Mapping Strategy:
# Glogow (Start) -> Mahendranagar
# Plock (Goal)   -> Kathmandu
# Wloclawek      -> Pokhara (The main gateway to the goal)

NEPAL_MAP = {
    'Mahendranagar': {'Dhangadhi': 45, 'Nepalgunj': 140},           # Was Glogow (START)
    'Dhangadhi':     {'Mahendranagar': 45, 'Surkhet': 90, 'Tansen': 140, 'Nepalgunj': 100}, # Was Leszno
    'Nepalgunj':     {'Dhangadhi': 100, 'Mahendranagar': 140, 'Tansen': 160, 'Narayangarh': 118, 'Dang': 100}, # Was Wroclaw
    'Surkhet':       {'Dailekh': 140, 'Butwal': 120, 'Tansen': 130, 'Dhangadhi': 90}, # Was Poznan
    'Dailekh':       {'Surkhet': 140, 'Pokhara': 110},              # Was Bydgoszcz
    'Pokhara':       {'Dailekh': 110, 'Kathmandu': 55, 'Butwal': 120}, # Was Wloclawek (Key Hub)
    'Kathmandu':     {'Pokhara': 55, 'Bhaktapur': 130},             # Was Plock (GOAL)
    'Butwal':        {'Pokhara': 120, 'Surkhet': 120, 'Tansen': 120, 'Hetauda': 120}, # Was Konin
    'Tansen':        {'Surkhet': 130, 'Butwal': 120, 'Hetauda': 160, 'Nepalgunj': 160, 'Dhangadhi': 140}, # Was Kalisz
    'Bhaktapur':     {'Kathmandu': 130, 'Hetauda': 150, 'Janakpur': 105}, # Was Warsaw
    'Hetauda':       {'Bhaktapur': 150, 'Butwal': 120, 'Tansen': 160, 'Narayangarh': 128, 'Janakpur': 165}, # Was Lodz
    'Janakpur':      {'Bhaktapur': 105, 'Hetauda': 165, 'Sindhuli': 82, 'Biratnagar': 280}, # Was Radom
    'Narayangarh':   {'Nepalgunj': 118, 'Hetauda': 128, 'Lumbini': 80}, # Was Częstochowa
    'Dang':          {'Nepalgunj': 100, 'Lumbini': 85},             # Was Opole
    'Lumbini':       {'Narayangarh': 80, 'Dang': 85, 'Biratnagar': 85}, # Was Katowice
    'Sindhuli':      {'Janakpur': 82, 'Biratnagar': 120},           # Was Kielce
    'Biratnagar':    {'Lumbini': 85, 'Sindhuli': 120, 'Janakpur': 280} # Was Kraków
}

# Heuristic Straight-Line Distance to Kathmandu (Goal)
# Values mapped from Diagram B [cite: 290-328]
H_KATHMANDU = {
    'Dailekh': 90, 'Pokhara': 44, 'Kathmandu': 0, 'Butwal': 96,
    'Surkhet': 107, 'Bhaktapur': 95, 'Hetauda': 118, 'Dhangadhi': 103,
    'Tansen': 107, 'Janakpur': 91, 'Mahendranagar': 40, 'Nepalgunj': 80,
    'Narayangarh': 90, 'Sindhuli': 102, 'Dang': 190, 'Biratnagar': 68,
    'Lumbini': 61
}

# Visualization Coordinates (Keeping topology layout)
CITY_COORDS = {
    'Dailekh': (4, 9), 'Pokhara': (6, 8), 'Kathmandu': (7, 7.5),
    'Surkhet': (2, 7), 'Butwal': (4, 6), 'Bhaktapur': (9, 6),
    'Mahendranagar': (0, 4), 'Dhangadhi': (2, 5), 'Tansen': (3, 4), 'Hetauda': (6, 4.5), 'Janakpur': (8, 3),
    'Nepalgunj': (2, 3), 'Narayangarh': (5, 2), 'Sindhuli': (7, 2),
    'Dang': (3, 1), 'Lumbini': (5, 1), 'Biratnagar': (7, 0)
}

# ============================================================================
# 2. SEARCH ALGORITHMS
# ============================================================================

def get_dfs_path(start, goal):
    stack = [(start, [start])]
    visited = set()
    while stack:
        (node, path) = stack.pop()
        if node == goal: return path
        if node not in visited:
            visited.add(node)
            for neighbor in reversed(list(NEPAL_MAP.get(node, {}).keys())):
                stack.append((neighbor, path + [neighbor]))
    return None

def get_bfs_path(start, goal):
    queue = deque([(start, [start])])
    visited = {start}
    while queue:
        (node, path) = queue.popleft()
        if node == goal: return path
        for neighbor in NEPAL_MAP.get(node, {}):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    return None

def get_astar_path(start, goal):
    # Priority Queue: (f_score, g_score, current_node, path)
    pq = [(H_KATHMANDU.get(start, 999), 0, start, [start])]
    visited_costs = {start: 0}
    
    while pq:
        (f, g, node, path) = heapq.heappop(pq)
        if node == goal: return path
        
        for neighbor, weight in NEPAL_MAP.get(node, {}).items():
            new_g = g + weight
            if neighbor not in visited_costs or new_g < visited_costs[neighbor]:
                visited_costs[neighbor] = new_g
                h = H_KATHMANDU.get(neighbor, 999)
                heapq.heappush(pq, (new_g + h, new_g, neighbor, path + [neighbor]))
    return None

# ============================================================================
# 3. VISUALIZATION ENGINE
# ============================================================================

def draw_network_path(path, algorithm_name, ax):
    G = nx.Graph()
    for city, neighbors in NEPAL_MAP.items():
        for neighbor, weight in neighbors.items():
            G.add_edge(city, neighbor, weight=weight)
    
    # Draw Base Map
    nx.draw_networkx_edges(G, pos=CITY_COORDS, ax=ax, edge_color='#e0e0e0', width=1)
    nx.draw_networkx_nodes(G, pos=CITY_COORDS, ax=ax, node_color='#cccccc', node_size=300)
    
    # Draw Labels
    nx.draw_networkx_labels(G, pos=CITY_COORDS, ax=ax, font_size=8, font_weight='bold')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos=CITY_COORDS, edge_labels=edge_labels, ax=ax, font_size=7)
    
    # Highlight Path
    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos=CITY_COORDS, edgelist=path_edges, ax=ax, edge_color='red', width=3)
        nx.draw_networkx_nodes(G, pos=CITY_COORDS, nodelist=path, ax=ax, node_color='#ff9999', node_size=400)
        
        # Start and Goal
        nx.draw_networkx_nodes(G, pos=CITY_COORDS, nodelist=[path[0]], ax=ax, node_color='green', node_size=500)
        nx.draw_networkx_nodes(G, pos=CITY_COORDS, nodelist=[path[-1]], ax=ax, node_color='gold', node_size=500)
        
        cost = sum(NEPAL_MAP[path[i]][path[i+1]] for i in range(len(path)-1))
        ax.set_title(f"{algorithm_name}\nNodes: {len(path)} | Cost: {cost}", fontsize=10, fontweight='bold')
    else:
        ax.set_title(f"{algorithm_name}: No Path", color='red')
    ax.axis('off')

if __name__ == "__main__":
    start_city = 'Mahendranagar'
    target_city = 'Kathmandu'
    
    print(f"Calculating delivery routes: {start_city} to {target_city}...")
    
    p_dfs = get_dfs_path(start_city, target_city)
    p_bfs = get_bfs_path(start_city, target_city)
    p_astar = get_astar_path(start_city, target_city)
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    plt.suptitle(f"Nepal Logistics AI: {start_city} to {target_city}", fontsize=16)
    
    draw_network_path(p_dfs, "DFS (Depth First)", axes[0])
    draw_network_path(p_bfs, "BFS (Breadth First)", axes[1])
    draw_network_path(p_astar, "A* Search (Optimal)", axes[2])
    
    plt.tight_layout()
    plt.show()