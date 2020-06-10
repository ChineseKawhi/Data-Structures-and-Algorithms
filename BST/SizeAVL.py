"""
    A SizeAVL implementation:
    An augmented AVL that keeps track of the node with 
    the number of nodes in the subtree rooted at this node
"""

from AVL import AVLNode, AVL



class SizeAVLNode(AVLNode):
    """
    A AVLNode which is augmented to keep track of 
    the number of nodes in the subtree rooted at this node.
    """
    def __init__(self, key, parent):
        """
        Creates a node.
        
        Args:
            parent: The node's parent.
            k: key of the node.
        """
        super(SizeAVLNode, self).__init__(key, parent)
        self.height = 1
    
    def _update_info(self):
        self.height = max(AVL._height(self.left), AVL._height(self.right)) + 1
        self.size = 1 + SizeAVL._size(self.left) + SizeAVL._size(self.right)

    def rank(self, k):
        """
        Count the number of nodes that key is smaller than k
        from the subtree rooted at this node.
        
        Args:
            k: The key of the node we want to find.
        
        Returns:
            The node with key k.

        Running Time:
            O(log(n))
        """

        if k < self.key:
            if(self.left is None):
                return 0
            else:
                return self.left.rank(k)
        else:
            if self.right is None:  
                return self.size
            else:
                return 1 + SizeAVL._size(self.left) + self.right.rank(k)

    def check_ri(self):
        """
        Checks the BST representation invariant around this node.
    
        Assert is not true if the RI is violated.

        Running Time:
            O(n)
        """
        size = 1
        assert((AVL._height(self.right) - AVL._height(self.left) < 2) or\
            (AVL._height(self.right) - AVL._height(self.left) > -2))
        if self.left is not None:
            assert(self.left.key <= self.key)
            assert(self.left.parent is self)
            size += SizeAVL._size(self.left)
            self.left.check_ri()
        if self.right is not None:
            assert(self.right.key >= self.key)
            assert(self.right.parent is self)
            size += SizeAVL._size(self.right)
            self.right.check_ri()
        assert(self.size == size)
        
class SizeAVL(AVL):
    """
    An augmented AVL that keeps track of the node with 
    the number of nodes in the subtree rooted at this node
    """
    def __init__(self, node_class = SizeAVLNode):
        super(SizeAVL, self).__init__(node_class)

    @staticmethod
    def _size(node):
        if node is None:
            return 0
        else:
            return node.size

    def rank(self, k):
        """
        Count the number of nodes that key is less than k.

        Running Time:
            O(log(n))
        """
        if(self.root is None):
            return 0
        else:
            return self.root.rank(k)

    def range(self, k1, k2):
        """
        Count the number of nodes that key is between k1 and k2.

        Running Time:
            O(log(n))
        """
        if(self.root is None):
            return 0
        else:
            return self.root.rank(k2) - self.root.rank(k1)

    def check_ri(self):
        """
        Checks the BST representation invariant.
        
        Assert is not true if the RI is violated.
        """
        if self.root is not None:
            assert(self.root.parent is None)
            self.root.check_ri()
        

