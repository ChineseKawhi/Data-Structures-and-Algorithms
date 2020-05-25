"""
    A SizeBSTNode implementation:
    An augmented BST that keeps track of the node with 
    the number of nodes in the subtree rooted at this node
    Last modified at: 2020/5/25
"""

from BST import BSTNode, BST

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

    def insert(self, node):
        """
        Inserts a node into the subtree rooted at this node.
        
        Args:
            node: The node to be inserted.
        
        Returns:
            succeeds or not

        Running Time:
            O(log(n))
        """
        if(node.key == self.key):
            return False
        elif(node.key < self.key):
            if(self.left is None):
                node.parent = self
                self.left = node
                self.size += 1
                return True
            else:
                if(self.left.insert(node) == True):
                    self.size += 1
                    return True
                else:
                    return False
        else:
            if(self.right is None):
                node.parent = self
                self.right = node
                self.size += 1
                return True
            else:
                
                if(self.right.insert(node) == True):
                    self.size += 1
                    return True
                else:
                    return False

    def remove(self):
        """
        Removes and returns this node from the BST.

        Running Time:
            O(log(n))
        """
        if(self.left is None or self.right is None):
            if(self is self.parent.left):
                self.parent.left = self.left or self.right
                if self.parent.left is not None:
                    self.parent.left.parent = self.parent
            else:
                self.parent.right = self.left or self.right
                if(self.parent.right is not None):
                    self.parent.right.parent = self.parent
            # update size
            parent = self.parent
            while(parent is not None):
                parent.size -= 1
                parent = parent.parent
            return self
        else:
            next_larger = self.next_larger()
            self.key, next_larger.key = next_larger.key, self.key
            # update size
            parent = next_larger.parent
            while(parent is not None):
                parent.size -= 1
                parent = parent.parent
            return next_larger.remove()

    def rank(self, k, count_k: False):
        """
        Count the number of nodes that key is smaller than k
        from the subtree rooted at this node.
        
        Args:
            k: The key of the node we want to find.
            count_k: include the node that key equals k
        
        Returns:
            The node with key k.

        Running Time:
            O(log(n))
        """
        if k == self.key:
            
            if(self.left is None):
                return 1 if count_k else 0
            else:
                return (1 if count_k else 0) + self.left.size
        elif k < self.key:
            if(self.left is None):
                return 0
            else:
                return self.left.rank(k, count_k)
        else:
            if self.right is None:  
                return self.size
            else:
                return 1 + self.left.size + self.right.rank(k, count_k)

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
    def __init__(self):
        super(SizeBST, self).__init__()

    def count(self, low, high):
        """
        Count the number of nodes that key is between low and hight.

        Running Time:
            O(log(n))
        """
        return None
    
    def insert(self, key):
        """
        Inserts a node into the BST.
        
        Args:
            node: The node to be inserted.
        
        Running Time:
            O(log(n))
        """
        if(self.root is None):
            self.root = SizeBSTNode(key, None)
        else:
            self.root.insert(SizeBSTNode(key, None))
    
    def rank(self, k, count_k):
        """
        Count the number of nodes that key is not greater than k.

        Args:
            k: The key of the node we want to find.
            count_k: include the node that key equals k
        
        Returns:
            The node with key k.

        Running Time:
            O(log(n))
        """
        return self.root.rank(k, count_k)

    def range(self, k1, k2):
        """
        Count the number of nodes that key is between k1 and k2.
        k1, k2 included.

        Running Time:
            O(log(n))
        """
        return self.root.rank(k2, True) - self.root.rank(k1, False)

    def check_ri(self):
        """
        Checks the BST representation invariant.
        
        Assert is not true if the RI is violated.
        """
        if self.root is not None:
            assert(self.root.parent is None)
            self.root.check_ri()

if __name__ == "__main__":
    tree = SizeBST()
    tree.insert(5)

    tree.insert(1)

    tree.insert(5)

    tree.insert(3)

    tree.insert(4)
    
    print(tree.range(1,5))

    print(tree)
    tree.check_ri()