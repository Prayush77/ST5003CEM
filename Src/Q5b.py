"""
Module: Task5b.py
Project: Multithreaded Sorting System
Description: Implements a parallel sorting strategy where two threads sort halves 
of an array and a third thread merges the results. Includes a GUI for visualization.
"""

import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox

# ============================================================================
# CORE SORTING LOGIC (GLOBAL DATA STRUCTURES)
# ============================================================================

# Shared global arrays as suggested by the assignment brief [cite: 266-268]
original_data = []
final_sorted_array = []

class ThreadedSorter:
    """Manages the lifecycle of sorting and merging threads."""
    
    def __init__(self, data):
        global original_data, final_sorted_array
        original_data = data
        final_sorted_array = [0] * len(data)
        self.mid = len(data) // 2
        
        # Sublists for individual threads [cite: 269]
        self.left_half = []
        self.right_half = []

    def sort_sublist(self, is_left):
        """Thread function: Sorts one half of the global array[cite: 264]."""
        if is_left:
            # Thread 0: Start index 0 to mid [cite: 272]
            self.left_half = sorted(original_data[:self.mid])
        else:
            # Thread 1: Start index mid to end [cite: 272]
            self.right_half = sorted(original_data[self.mid:])

    def merge_sublists(self):
        """Thread function: Merges the results into the second global array[cite: 265]."""
        i = j = k = 0
        while i < len(self.left_half) and j < len(self.right_half):
            if self.left_half[i] < self.right_half[j]:
                final_sorted_array[k] = self.left_half[i]
                i += 1
            else:
                final_sorted_array[k] = self.right_half[j]
                j += 1
            k += 1
        
        # Handle remaining elements
        while i < len(self.left_half):
            final_sorted_array[k] = self.left_half[i]
            i += 1; k += 1
        while j < len(self.right_half):
            final_sorted_array[k] = self.right_half[j]
            j += 1; k += 1

# ============================================================================
# GUI LAYER
# ============================================================================

class SortingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multithreaded Sort [ST5003CEM]")
        self.root.geometry("600x450")
        self._setup_ui()

    def _setup_ui(self):
        """Initializes the interactive components of the application."""
        container = ttk.Frame(self.root, padding="20")
        container.pack(fill=tk.BOTH, expand=True)

        ttk.Label(container, text="Multithreaded Sorting System", font=('Arial', 14, 'bold')).pack(pady=10)
        
        self.input_entry = ttk.Entry(container, width=50)
        self.input_entry.insert(0, "7, 12, 19, 3, 18, 4, 2, 6, 15, 8")
        self.input_entry.pack(pady=5)
        
        ttk.Button(container, text="Execute Parallel Sort", command=self.run_sort).pack(pady=10)
        
        self.output_area = tk.Text(container, height=10, width=60, font=('Consolas', 10))
        self.output_area.pack(pady=10)

    def run_sort(self):
        """Orchestrates the three-thread process[cite: 270]."""
        try:
            raw_data = [int(x.strip()) for x in self.input_entry.get().split(",")]
            sorter = ThreadedSorter(raw_data)
            self.output_area.delete(1.0, tk.END)
            self.output_area.insert(tk.END, f"Input: {raw_data}\n\n")

            # 1. Create Sorting Threads [cite: 264]
            t0 = threading.Thread(target=sorter.sort_sublist, args=(True,))
            t1 = threading.Thread(target=sorter.sort_sublist, args=(False,))
            
            t0.start(); t1.start()
            t0.join(); t1.join() # Parent waits for sorting to exit 
            
            self.output_area.insert(tk.END, f"Thread 0 Result: {sorter.left_half}\n")
            self.output_area.insert(tk.END, f"Thread 1 Result: {sorter.right_half}\n")

            # 2. Create Merging Thread [cite: 265]
            tm = threading.Thread(target=sorter.merge_sublists)
            tm.start()
            tm.join()

            self.output_area.insert(tk.END, f"\nFinal Sorted List: {final_sorted_array}\n")
            messagebox.showinfo("Success", "Sort Completed with 3 Threads!")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid comma-separated list of integers.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SortingApp(root)
    root.mainloop()