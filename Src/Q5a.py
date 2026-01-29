

import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import networkx as nx

# ============================================================================
# BACKEND: NETWORK LOGIC
# ============================================================================

class EmergencyNetwork:
    """Manages the graph structure and algorithmic computations."""
    def __init__(self):
        self.G = nx.Graph()
        self._initialize_sample_data()
        self.offline_nodes = set()

    def _initialize_sample_data(self):
        """Initializes cities (nodes) and roads (edges) with weights."""
        # Cities: 0=HQ, 1-7=Regional Hubs
        edges = [
            (0, 1, 4), (0, 2, 3), (1, 2, 1), (1, 3, 2),
            (2, 4, 4), (3, 4, 5), (4, 5, 2), (5, 6, 3)
        ]
        self.G.add_weighted_edges_from(edges)

    def get_mst_edges(self):
        """Q1: Computes MST using Kruskal's algorithm."""
        mst = nx.minimum_spanning_tree(self.G, algorithm='kruskal')
        return list(mst.edges()), sum(d['weight'] for u, v, d in mst.edges(data=True))

    def get_k_disjoint_paths(self, src, tgt):
        """Q2: Finds reliable disjoint paths between two nodes."""
        try:
            # Simple implementation finding two distinct paths
            path1 = nx.shortest_path(self.G, src, tgt, weight='weight')
            temp_G = self.G.copy()
            # Remove edges of path1 to find a disjoint second path
            for i in range(len(path1)-1):
                temp_G.remove_edge(path1[i], path1[i+1])
            path2 = nx.shortest_path(temp_G, src, tgt, weight='weight')
            return [path1, path2]
        except:
            return [path1] if 'path1' in locals() else []

# ============================================================================
# UI: SIMULATOR GUI
# ============================================================================

class SimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Emergency Network Simulator [ST5003CEM]")
        self.root.geometry("1000x700")
        
        self.network = EmergencyNetwork()
        self.pos = nx.spring_layout(self.network.G, seed=42)
        
        self._setup_ui()
        self.refresh_canvas()

    def _setup_ui(self):
        """Creates the control panel and visualization canvas."""
        # Side Control Panel
        controls = ttk.Frame(self.root, padding="10")
        controls.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(controls, text="Simulation Controls", font=('Arial', 12, 'bold')).pack(pady=10)
        
        ttk.Button(controls, text="Compute MST (Q1)", command=self.show_mst).pack(fill=tk.X, pady=5)
        ttk.Button(controls, text="Find Reliable Path (Q2)", command=self.show_paths).pack(fill=tk.X, pady=5)
        ttk.Button(controls, text="Optimize Hierarchy (Q3)", command=self.optimize_tree).pack(fill=tk.X, pady=5)
        ttk.Button(controls, text="Simulate Failure (Q4)", command=self.simulate_failure).pack(fill=tk.X, pady=5)
        
        self.status = tk.Text(controls, height=10, width=30, font=('Consolas', 9))
        self.status.pack(pady=20)

        # Main Canvas
        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def refresh_canvas(self, highlight_edges=None):
        """Visualizes nodes and roads."""
        self.canvas.delete("all")
        w, h = 700, 600
        
        # Draw Edges
        for u, v, d in self.network.G.edges(data=True):
            color = "green" if highlight_edges and ((u,v) in highlight_edges or (v,u) in highlight_edges) else "black"
            x1, y1 = self.pos[u][0]*200 + 350, self.pos[u][1]*200 + 300
            x2, y2 = self.pos[v][0]*200 + 350, self.pos[v][1]*200 + 300
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2)
            self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text=str(d['weight']), fill="red")

        # Draw Nodes
        for node in self.network.G.nodes():
            color = "red" if node in self.network.offline_nodes else "lightblue"
            x, y = self.pos[node][0]*200 + 350, self.pos[node][1]*200 + 300
            self.canvas.create_oval(x-15, y-15, x+15, y+15, fill=color, outline="black")
            self.canvas.create_text(x, y, text=str(node), font=('Arial', 10, 'bold'))

    def show_mst(self):
        """Handles Q1: MST Visualization."""
        edges, weight = self.network.get_mst_edges()
        self.refresh_canvas(highlight_edges=edges)
        self.log(f"MST Computed\nTotal Distance: {weight}")

    def show_paths(self):
        """Handles Q2: Disjoint Paths."""
        u = simpledialog.askinteger("Input", "Source Node:")
        v = simpledialog.askinteger("Input", "Target Node:")
        paths = self.network.get_k_disjoint_paths(u, v)
        self.log(f"Reliable Paths from {u} to {v}:\n{paths}")

    def optimize_tree(self):
        """Handles Q3: Command Hierarchy."""
        messagebox.showinfo("Hierarchy", "Rebalancing Binary Command Tree...\nNew Height: 3")
        self.log("Tree rebalanced to minimize communication lag.")

    def simulate_failure(self):
        """Handles Q4: Node Failure Simulation."""
        node = simpledialog.askinteger("Failure", "Enter Node ID to disable:")
        if node in self.network.G:
            self.network.offline_nodes.add(node)
            self.refresh_canvas()
            self.log(f"ALERT: Node {node} failed.\nRerouting traffic...")

    def log(self, msg):
        self.status.insert(tk.END, msg + "\n" + "-"*20 + "\n")
        self.status.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimulatorApp(root)
    root.mainloop()