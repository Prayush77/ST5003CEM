
def get_padded_tiles(multipliers):

    return [1] + multipliers + [1]

def build_dp_table(n):
 
    return [[0] * n for _ in range(n)]

def compute_shatter_logic(tiles, dp, i, j, k):

    # Points from previously solved sub-ranges
    left_points = dp[i][k]
    right_points = dp[k][j]
    
    # Points for shattering tile k last (it is now adjacent to i and j)
    shatter_score = tiles[i] * tiles[k] * tiles[j]
    
    return left_points + right_points + shatter_score

def optimize_tile_shattering(tiles, dp):

    n = len(tiles)
    
    # gap represents the distance between the left (i) and right (j) boundary
    for gap in range(2, n):
        for i in range(n - gap):
            j = i + gap
            # Try every tile 'k' between boundaries i and j as the last one to shatter
            for k in range(i + 1, j):
                current_score = compute_shatter_logic(tiles, dp, i, j, k)
                # Store the maximum score found for this range
                dp[i][j] = max(dp[i][j], current_score)

def solve_tile_game(tile_multipliers):

    if not tile_multipliers:
        return 0

    # 1. Prepare boundaries
    tiles = get_padded_tiles(tile_multipliers)
    n = len(tiles)
    
    # 2. Setup DP structure
    dp = build_dp_table(n)
    
    # 3. Execute the DP algorithm
    optimize_tile_shattering(tiles, dp)
    
    # 4. The result for the full range is at dp[0][n-1]
    return dp[0][n-1]


# VALIDATION SECTION


if __name__ == "__main__":
    print("-" * 65)
    print("QUESTION 2: STRATEGIC TILE SHATTER - DYNAMIC PROGRAMMING")
    print("-" * 65)

    # Test Case 1
    input_1 = [3, 1, 5, 8]
    result_1 = solve_tile_game(input_1)
    print(f"Test 1 Input:    {input_1}")
    print(f"Calculated:      {result_1}")
    print(f"Expected:        167")
    print(f"Status:          {'PASS' if result_1 == 167 else 'FAIL'}")

    # Test Case 2
    input_2 = [1, 5]
    result_2 = solve_tile_game(input_2)
    print(f"\nTest 2 Input:    {input_2}")
    print(f"Calculated:      {result_2}")
    print(f"Expected:        10")
    print(f"Status:          {'PASS' if result_2 == 10 else 'FAIL'}")
    print("-" * 65)