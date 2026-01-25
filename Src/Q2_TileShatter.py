def solve_tile_shatter(multipliers):
    n = len(multipliers)
    # DP table to store results of subproblems
    # dp[i][j] stores max points for shattering tiles from index i to j
    dp = [[0] * n for _ in range(n)]

    # 'length' is the length of the sub-array we are solving for
    for length in range(1, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            
            # Try every possible last tile 'k' to shatter in this range [i, j]
            for k in range(i, j + 1):
                # Points from left subarray (if any)
                left_points = dp[i][k-1] if k > i else 0
                
                # Points from right subarray (if any)
                right_points = dp[k+1][j] if k < j else 0
                
                # Points from shattering tile 'k' itself
                # Neighbors are outside the current range [i, j]
                # If out of bounds, use multiplier 1 [cite: 90]
                left_neighbor = multipliers[i-1] if i > 0 else 1
                right_neighbor = multipliers[j+1] if j < n - 1 else 1
                
                current_shatter_points = left_neighbor * multipliers[k] * right_neighbor
                
                total_points = left_points + right_points + current_shatter_points
                
                # Maximize
                if total_points > dp[i][j]:
                    dp[i][j] = total_points

    return dp[0][n-1]

# Test Case 1 [cite: 98]
test1 = [3, 1, 5, 8]
print(f"Input: {test1} -> Max Points: {solve_tile_shatter(test1)}") # Expected: 167

# Test Case 2 [cite: 109]
test2 = [1, 5]
print(f"Input: {test2} -> Max Points: {solve_tile_shatter(test2)}") # Expected: 10