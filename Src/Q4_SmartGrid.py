import pandas as pd

# 1. Model the Input Data [cite: 170]
demand_data = {
    'Hour': ['06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'],
    'District_A': [20, 22, 25, 30, 35, 35, 30, 25, 20, 20, 25, 30, 35, 40, 30], # Example values extended
    'District_B': [15, 16, 20, 25, 30, 30, 25, 20, 15, 15, 20, 25, 30, 35, 25],
    'District_C': [25, 28, 30, 35, 40, 40, 35, 30, 25, 25, 30, 35, 40, 45, 35]
}

sources = {
    'Solar':  {'cap': 50, 'cost': 1.0, 'start': 6, 'end': 18},
    'Hydro':  {'cap': 40, 'cost': 1.5, 'start': 0, 'end': 24},
    'Diesel': {'cap': 60, 'cost': 3.0, 'start': 17, 'end': 23}
}

# Output storage
results = []
total_daily_cost = 0

print(f"{'Hour':<5} {'Dist':<5} {'Solar':<8} {'Hydro':<8} {'Diesel':<8} {'Total':<8} {'Demand':<8} {'Status'}")

# 2. Design Hourly Allocation [cite: 172]
for i, hr_str in enumerate(demand_data['Hour']):
    hr = int(hr_str)
    
    # Calculate Total Demand for this hour
    demands = {'A': demand_data['District_A'][i], 
               'B': demand_data['District_B'][i], 
               'C': demand_data['District_C'][i]}
    
    # 3. Implement Greedy Source Prioritization [cite: 174]
    # Reset available capacity for the hour
    avail_solar = sources['Solar']['cap'] if sources['Solar']['start'] <= hr <= sources['Solar']['end'] else 0
    avail_hydro = sources['Hydro']['cap']
    avail_diesel = sources['Diesel']['cap'] if sources['Diesel']['start'] <= hr <= sources['Diesel']['end'] else 0
    
    for dist, demand in demands.items():
        used_solar = 0
        used_hydro = 0
        used_diesel = 0
        remaining_demand = demand
        
        # Step A: Use Solar (Cheapest)
        if remaining_demand > 0 and avail_solar > 0:
            take = min(remaining_demand, avail_solar)
            used_solar = take
            avail_solar -= take
            remaining_demand -= take
            
        # Step B: Use Hydro (Mid)
        if remaining_demand > 0 and avail_hydro > 0:
            take = min(remaining_demand, avail_hydro)
            used_hydro = take
            avail_hydro -= take
            remaining_demand -= take
            
        # Step C: Use Diesel (Expensive)
        if remaining_demand > 0 and avail_diesel > 0:
            take = min(remaining_demand, avail_diesel)
            used_diesel = take
            avail_diesel -= take
            remaining_demand -= take
            
        total_used = used_solar + used_hydro + used_diesel
        
        # 4. Handle Approximate Demand (±10%) [cite: 178]
        # If total_used is within 90% of demand, we consider it met.
        status = "Met" if total_used >= 0.9 * demand else "Under"
        
        # Calculate Cost
        cost = (used_solar * 1.0) + (used_hydro * 1.5) + (used_diesel * 3.0)
        total_daily_cost += cost
        
        print(f"{hr_str:<5} {dist:<5} {used_solar:<8} {used_hydro:<8} {used_diesel:<8} {total_used:<8} {demand:<8} {status}")

print(f"\nTotal Daily Cost: Rs. {total_daily_cost}")