"""
    A AVL Tree implementation
"""

from BST import BSTNode, BST


class AVLNode(BSTNode):
    """
    A AVLNode which is augmented to keep track of 
    the height of the subtree rooted at this node.
    """
    def __init__(self, key, parent):
        """
        Creates a node.
        
        Args:
            parent: The node's parent.
            k: key of the node.
        """
        super(AVLNode, self).__init__(key, parent)
        self.height = 1

    def _update_info(self):
        self.height = max(AVL._height(self.left), AVL._height(self.right)) + 1

    def list(self, k1, k2, result = []):
        if(self.key < k2 and self.key > k1):
            result.append(self.key)
            if(self.left is not None):
                self.left.list(k1, k2, result)
            if(self.right is not None):
                self.right.list(k1, k2, result)
        elif(self.key > k2 and self.left is not None):
            self.left.list(k1, k2, result)
        elif(self.key < k1 and self.right is not None):
            self.right.list(k1, k2, result)

    def check_ri(self):
        """
        Checks the BST representation invariant around this node.
    
        Assert is not true if the RI is violated.

        Running Time:
            O(n)
        """
        assert((AVL._height(self.right) - AVL._height(self.left) < 2) or\
            (AVL._height(self.right) - AVL._height(self.left) > -2))
        if self.left is not None:
            assert(self.left.key <= self.key)
            assert(self.left.parent is self)
            self.left.check_ri()
        if self.right is not None:
            assert(self.right.key >= self.key)
            assert(self.right.parent is self)
            self.right.check_ri()

class AVL(BST):
    def __init__(self, node_class = AVLNode):
        super(AVL, self).__init__(node_class)

    @staticmethod
    def _height(node):
        if node is None:
            return 0
        else:
            return node.height

    def _rebalance(self, node):
        while(node is not None):
            node._update_info()
            if(AVL._height(node.right) - AVL._height(node.left) >= 2):
                if(AVL._height(node.right.right) > AVL._height(node.right.left)):
                    self._left_rotate(node)
                else:
                    self._right_rotate(node.right)
                    self._left_rotate(node)
            elif(AVL._height(node.left) - AVL._height(node.right) >= 2):
                if(AVL._height(node.left.left) > AVL._height(node.left.right)):
                    self._right_rotate(node)
                else:
                    self._left_rotate(node.left)
                    self._right_rotate(node)
            node = node.parent

    def _left_rotate(self, x):
        y = x.right
        y.parent = x.parent
        if y.parent is None:
            self.root = y
        else:
            if y.parent.right is x:
                y.parent.right = y
            elif y.parent.left is x:
                y.parent.left = y
        x.right = y.left
        if(x.right is not None):
            x.right.parent = x
        x.parent = y
        y.left = x
        x._update_info()
        y._update_info()

    def _right_rotate(self, x):
        y = x.left
        y.parent = x.parent
        if y.parent is None:
            self.root = y
        else:
            if y.parent.left is x:
                y.parent.left = y
            elif y.parent.right is x:
                y.parent.right = y
        x.left = y.right
        if x.left is not None:
            x.left.parent = x
        y.right = x
        x.parent = y
        x._update_info()
        y._update_info()

    def insert(self, k):
        """
        Inserts a node into the AVL.
        
        Args:
            k: The key of the node to be inserted.
        
        Returns:
            The node inserted.
        
        Running Time:
            O(log(n))
        """
        node = super(AVL, self).insert(k)
        self._rebalance(node)
        return node

    def remove(self, k):
        """
        Removes and returns the node with key k from the AVL.

        Args:
            k: The key of the node that we want to delete.
            
        Returns:
            The deleted node with key k.

        Running Time:
            O(log(n))
        """
        node = super(AVL, self).remove(k)
        self._rebalance(node.parent)
        return node

    def list(self, k1, k2, result = []):
        if(self.root is None):
            return result
        else:
            self.root.list(k1, k2, result)

    def check_ri(self):
        """
        Checks the BST representation invariant.
        
        Assert is not true if the RI is violated.
        """
        if self.root is not None:
            assert(self.root.parent is None)
            self.root.check_ri()
    