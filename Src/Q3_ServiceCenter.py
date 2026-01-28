class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def min_camera_cover(root):
    # Returns a tuple: (cost_if_covered_by_child, cost_if_has_camera, cost_if_needs_cover)
    # 0: Covered by child (I don't have camera, but I am safe)
    # 1: I have a camera (I cover myself and parent)
    # 2: I need cover (Parent must cover me)
    
    def dfs(node):
        if not node:
            return 0, 9999, 0 # Null nodes don't need cover
        
        left = dfs(node.left)
        right = dfs(node.right)
        
        # Option 1: I have a camera
        # Cost = 1 + min state of children
        cost_camera = 1 + min(left) + min(right)
        
        # Option 2: I am covered by a child (at least one child must have camera)
        # If left has camera (left[1]), right can be anything.
        cost_covered = min(left[1] + min(right), right[1] + min(left))
        
        # Option 3: I need cover from parent
        # My children must be covered (state 0 or 1), they cannot 'need' cover.
        cost_need = min(left[0], left[1]) + min(right[0], right[1])
        
        return cost_covered, cost_camera, cost_need

    # The root cannot 'need' cover from a parent (it has no parent)
    # So we take min of (covered_by_child, has_camera)
    states = dfs(root)
    return min(states[0], states[1])

# Build Tree Example [cite: 118]
# Structure: Root -> Left(Node) -> Left(Node) -> Left(Node) (Linear chain for simplicity based on input)
root = TreeNode(0)
root.left = TreeNode(0)
root.left.left = TreeNode(0)
root.left.left.left = TreeNode(0) 

print(f"Min Service Centers: {min_camera_cover(root)}") # Expected: 2 [cite: 119]