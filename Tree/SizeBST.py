"""
    A SizeBST implementation:
    An augmented BST that keeps track of the node with 
    the number of nodes in the subtree rooted at this node
"""

from BST import BSTNode, BST

def size(node):
    if node is None:
        return 0
    else:
        return node.size

class SizeBSTNode(BSTNode):
    """
    A BSTNode which is augmented to keep track of 
    the number of nodes in the subtree rooted at this node.
    """
    def __init__(self, key, parent):
        """
        Creates a node.
        
        Args:
            parent: The node's parent.
            k: key of the node.
        """
        super(SizeBSTNode, self).__init__(key, parent)
        self.size = 1

    def _update_info(self):
        self.size = 1 + size(self.left) + size(self.right)
        if(self.parent is not None):
            self.parent._update_info()

    def rank(self, k):
        """
        Count the number of nodes that key is less than k.

        Args:
            k: The key that the nodes' key is less than.
        
        Returns:
            The number of nodes that key is less than k

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
                return 1 + size(self.left) + self.right.rank(k)

    def check_ri(self):
        """
        Checks the BST representation invariant around this node.
    
        Assert is not true if the RI is violated.

        Running Time:
            O(n)
        """
        size = 1
        if self.left is not None:
            assert(self.left.key <= self.key)
            assert(self.left.parent is self)
            size += self.left.size
            self.left.check_ri()
        if self.right is not None:
            assert(self.right.key >= self.key)
            assert(self.right.parent is self)
            size += self.right.size
            self.right.check_ri()
        assert(self.size == size)

class SizeBST(BST):
    """
    An augmented BST that keeps track of the node with 
    the number of nodes in the subtree rooted at this node
    """
    def __init__(self, node_class = SizeBSTNode):
        super(SizeBST, self).__init__(node_class)
    
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

    def insert(self, k):
        """
        Inserts a node into the SizeBST.
        
        Args:
            k: The key of the node to be inserted.
        
        Returns:
            The node inserted.
        
        Running Time:
            O(log(n))
        """
        node = super(SizeBST, self).insert(k)
        node._update_info()
        return node

    def remove(self, k):
        """
        Removes and returns the node with key k from the SizeBST.

        Args:
            k: The key of the node that we want to delete.
            
        Returns:
            The deleted node with key k.

        Running Time:
            O(log(n))
        """
        node = super(SizeBST, self).remove(k)
        node._update_info()
        return node

    def check_ri(self):
        """
        Checks the BST representation invariant.
        
        Assert is not true if the RI is violated.
        """
        if self.root is not None:
            assert(self.root.parent is None)
            self.root.check_ri()
