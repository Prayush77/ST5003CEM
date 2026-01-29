

class EnergyGridOptimizer:
    def __init__(self):
        # 1. Model the Input Data [cite: 170, 171]
        self.sources = [
            {"id": "S1", "type": "Solar", "max": 50, "hours": range(6, 19), "cost": 1.0},
            {"id": "S2", "type": "Hydro", "max": 40, "hours": range(0, 24), "cost": 1.5},
            {"id": "S3", "type": "Diesel", "max": 60, "hours": range(17, 24), "cost": 3.0}
        ]
        
        # Hourly Demand Table (kWh) [cite: 128, 141]
        self.demand_table = {
            "06": {"A": 20, "B": 15, "C": 25},
            "07": {"A": 22, "B": 16, "C": 28}
        }

    def solve_hourly_allocation(self, hour_str, demands):
        """
        Design an Hourly Allocation Algorithm[cite: 172].
        Uses Greedy Source Prioritization (cheapest first)[cite: 174, 175].
        """
        hour = int(hour_str)
        total_demand = sum(demands.values())
        
        # Filter available sources and sort by cost [cite: 132, 175]
        available = sorted(
            [s for s in self.sources if hour in s['hours']], 
            key=lambda x: x['cost']
        )
        
        allocation_results = {dist: {"Solar": 0, "Hydro": 0, "Diesel": 0} for dist in demands}
        remaining_demand = demands.copy()
        
        for source in available:
            source_cap = source['max']
            source_type = source['type']
            
            for dist in demands:
                needed = remaining_demand[dist]
                if needed <= 0 or source_cap <= 0:
                    continue
                
                # Fulfill demand greedily from the current source
                drawn = min(needed, source_cap)
                allocation_results[dist][source_type] += drawn
                source_cap -= drawn
                remaining_demand[dist] -= drawn
        
        return allocation_results

    def generate_report(self):
        """Analyze Cost and Resource Usage[cite: 181, 182]."""
        total_cost = 0
        total_renewable = 0
        total_energy = 0
        
        print(f"{'Hour':<6} {'Dist':<6} {'Solar':<8} {'Hydro':<8} {'Diesel':<8} {'Used':<8} {'Demand':<8} {'% Met'}")
        print("-" * 70)

        for hour, dist_demands in self.demand_table.items():
            allocations = self.solve_hourly_allocation(hour, dist_demands)
            
            for dist, used in allocations.items():
                solar, hydro, diesel = used["Solar"], used["Hydro"], used["Diesel"]
                actual_used = solar + hydro + diesel
                demand = dist_demands[dist]
                met_pct = (actual_used / demand) * 100
                
                # Tracking metrics
                total_cost += (solar * 1.0) + (hydro * 1.5) + (diesel * 3.0)
                total_renewable += (solar + hydro)
                total_energy += actual_used
                
                print(f"{hour:<6} {dist:<6} {solar:<8.1f} {hydro:<8.1f} {diesel:<8.1f} {actual_used:<8.1f} {demand:<8.1f} {met_pct:.1f}%")

        # Handle Approximate Demand Satisfaction Analysis [cite: 176, 184]
        renewable_pct = (total_renewable / total_energy) * 100 if total_energy > 0 else 0
        print("-" * 70)
        print(f"Total Distribution Cost: Rs. {total_cost:.2f}")
        print(f"Renewable Energy Fulfillment: {renewable_pct:.1f}%")

# ============================================================================
# EXECUTION
# ============================================================================

if __name__ == "__main__":
    optimizer = EnergyGridOptimizer()
    optimizer.generate_report()