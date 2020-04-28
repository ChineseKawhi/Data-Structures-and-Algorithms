class TreeNode:
     def __init__(self, x):
         self.val = x
         self.left = None
         self.right = None
         self.subtree_size = 1

class AVL:
    def __init__(self):
        self.root = None
    
    