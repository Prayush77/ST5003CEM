

from typing import Optional, List

class CityNode:
    """Represents a city in the corporation's network."""
    def __init__(self, name: int = 0, left: Optional['CityNode'] = None, right: Optional['CityNode'] = None):
        self.name = name
        self.left = left
        self.right = right

class NetworkServicePlanner:
    """
    Greedy algorithm to calculate the minimum number of service centers.
    
    Node States:
        0 -> UNCOVERED: Needs a service center nearby.
        1 -> CENTER_INSTALLED: This city has a service center.
        2 -> COVERED: This city is serviced by an adjacent center.
    """

    UNCOVERED = 0
    CENTER_INSTALLED = 1
    COVERED = 2

    def __init__(self):
        self.total_centers = 0

    def _determine_node_state(self, node: Optional[CityNode]) -> int:
        """
        Recursive post-order traversal to decide state based on children.
        Logic: Always place centers as high as possible (greedy) to maximize coverage.
        """
        if not node:
            # Null nodes are considered covered by default to not trigger center placement
            return self.COVERED

        # Bottom-up evaluation
        left_state = self._determine_node_state(node.left)
        right_state = self._determine_node_state(node.right)

        # 1. If any child is UNCOVERED, a center MUST be placed at the current node
        if left_state == self.UNCOVERED or right_state == self.UNCOVERED:
            self.total_centers += 1
            return self.CENTER_INSTALLED

        # 2. If any child has a center, the current node is now COVERED
        if left_state == self.CENTER_INSTALLED or right_state == self.CENTER_INSTALLED:
            return self.COVERED

        # 3. Otherwise, children are covered but have no center; current node is UNCOVERED
        return self.UNCOVERED

    def calculate_min_centers(self, root: Optional[CityNode]) -> int:
        """
        Main interface to solve the problem for a given root node.
        """
        self.total_centers = 0
        if not root:
            return 0
            
        # If the root is left UNCOVERED after the DFS, place a center at the root
        if self._determine_node_state(root) == self.UNCOVERED:
            self.total_centers += 1
            
        return self.total_centers

# ============================================================================
# HELPER: TREE CONSTRUCTION
# ============================================================================

def construct_from_list(values: List[Optional[int]]) -> Optional[CityNode]:
    """Helper to build a binary tree from a level-order representation."""
    if not values:
        return None
    
    nodes = [CityNode(v) if v is not None else None for v in values]
    for i in range(len(nodes)):
        if nodes[i] is not None:
            left_idx = 2 * i + 1
            right_idx = 2 * i + 2
            if left_idx < len(nodes):
                nodes[i].left = nodes[left_idx]
            if right_idx < len(nodes):
                nodes[i].right = nodes[right_idx]
    return nodes[0]

# ============================================================================
# VALIDATION
# ============================================================================

if __name__ == "__main__":
    print("-" * 65)
    print("QUESTION 3: MINIMUM SERVICE CENTERS - GREEDY DFS")
    print("-" * 65)

    # Example Input: tree= {0,0, null, 0, null, 0, null, null, 0} [cite: 118]
    # This represents a chain-like structure in the provided diagram
    example_input = [0, 0, None, 0, None, 0, None, None, 0]
    network_root = construct_from_list(example_input)

    planner = NetworkServicePlanner()
    result = planner.calculate_min_centers(network_root)
    
    print(f"Input Representation: {example_input}")
    print(f"Minimum Centers Required: {result}") # Output: 2 [cite: 119]
    print(f"Status: {'PASS' if result == 2 else 'FAIL'}")
    print("-" * 65)