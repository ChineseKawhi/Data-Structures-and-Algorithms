"""
    A BST implementation
"""



class BSTNode(object):
    """A node in the BST tree."""
    def __init__(self, key, parent):
        """
        Creates a node.

        Args:
            key: key of the node.
            parent: The node's parent.
        
        Running Time:
            O(1)
        """
        self.key = key
        self.parent = parent
        self.left = None
        self.right = None

    """str method is copied from mit 6.006 material"""
    def _str(self):
        """Internal method for ASCII art."""
        label = str(self.key)
        if self.left is None:
            left_lines, left_pos, left_width = [], 0, 0
        else:
            left_lines, left_pos, left_width = self.left._str()
        if self.right is None:
            right_lines, right_pos, right_width = [], 0, 0
        else:
            right_lines, right_pos, right_width = self.right._str()
        middle = max(right_pos + left_width - left_pos + 1, len(label), 2)
        pos = left_pos + middle // 2
        width = left_pos + middle + right_width - right_pos
        while len(left_lines) < len(right_lines):
            left_lines.append(' ' * left_width)
        while len(right_lines) < len(left_lines):
            right_lines.append(' ' * right_width)
        if (middle - len(label)) % 2 == 1 and self.parent is not None and \
           self is self.parent.left and len(label) < middle:
            label += '.'
        label = label.center(middle, '.')
        if label[0] == '.':
            label = ' ' + label[1:]
        if label[-1] == '.':
            label = label[:-1] + ' '
        lines = [' ' * left_pos + label + ' ' * (right_width - right_pos),
                 ' ' * left_pos + '/' + ' ' * (middle-2) +
                 '\\' + ' ' * (right_width - right_pos)] + \
            [left_line + ' ' * (width - left_width - right_width) + right_line
             for left_line, right_line in zip(left_lines, right_lines)]
        return lines, pos, width

    def __str__(self):
        return '\n'.join(self._str()[0])
    """str method is copied from mit 6.006 material"""

    def find(self, k):
        """
        Finds and returns the node with key k from the subtree 
        rooted at this node.
        
        Args:
            k: The key of the node we want to find.
        
        Returns:
            The node with key k.

        Running Time:
            O(log(n))
        """
        if k == self.key:
            return self
        elif k < self.key:
            if self.left is None:
                return None
            else:
                return self.left.find(k)
        else:
            if self.right is None:  
                return None
            else:
                return self.right.find(k)

    def insert(self, node):
        """
        Inserts a node into the subtree rooted at this node.
        
        Args:
            node: The node to be inserted.
        
        Running Time:
            O(log(n))
        """
        if(node.key < self.key):
            if(self.left is None):
                node.parent = self
                self.left = node
            else:
                self.left.insert(node)
        else:
            if(self.right is None):
                node.parent = self
                self.right = node
            else:
                self.right.insert(node)

    def remove(self):
        """
        Removes and returns this node from the BST.

        Returns:
            The deleted node with key k.

        Running Time:
            O(log(n))
        """
        # wrong first time
        # swap the key value first instead of swapping the pointer
        # if the tree is z-zagged or straight:
        #   just move the children one level up
        #   there is no need to find next lagger node
        # else:
        #   find next lagger node, swap the key
        # follow course material's idea, remove the root is 
        # handle by the tree remove with a presudo node
        if(self.left is None or self.right is None):
            if(self is self.parent.left):
                self.parent.left = self.left or self.right
                if self.parent.left is not None:
                    self.parent.left.parent = self.parent
            else:
                self.parent.right = self.left or self.right
                if(self.parent.right is not None):
                    self.parent.right.parent = self.parent
            return self
        else:
            next_larger = self.next_larger()
            self.key, next_larger.key = next_larger.key, self.key
            return next_larger.remove()
                
    def next_larger(self):
        """
        Returns the node with the next larger key (the successor) in the BST.

        Running Time:
            O(log(n))
        """
        if(self.right is None):
            current = self
            while(current.parent and current.parent.right == current):
                current = current.parent
            return current.parent
        else:
            return self.right.find_min()
    
    def find_max(self):
        """
        Finds the node with the maxmum key in the subtree 
        rooted at this node.
        
        Returns:
            The node with the maxmum key.

        Running Time:
            O(log(n))
        """
        if(self.right is None):
            return self
        else:
            return self.right.find_max()

    def find_min(self):
        """
        Finds the node with the minimum key in the subtree 
        rooted at this node.
        
        Returns:
            The node with the minimum key.

        Running Time:
            O(log(n))
        """
        if(self.left is None):
            return self
        else:
            return self.left.find_min()

    def check_ri(self):
        """
        Checks the BST representation invariant around this node.
    
        Assert is not true if the RI is violated.

        Running Time:
            O(n)
        """
        if self.left is not None:
            assert(self.left.key <= self.key)
            assert(self.left.parent is self)
            self.left.check_ri()
        if self.right is not None:
            assert(self.right.key >= self.key)
            assert(self.right.parent is self)
            self.right.check_ri()

class BST(object):
    """A binary search tree. Node type is TreeNode"""
    def __init__(self, node_class = BSTNode):
        """
        Creates a BST.
        
        Running Time:
            O(1)
        """
        self.root = None
        self.node_class = node_class

    """str method is copied from mit 6.006 material"""
    def __str__(self):
        if self.root is None: return '<empty tree>'
        return str(self.root)
    """str method is copied from mit 6.006 material"""

    def find(self, k):
        """
        Finds and returns the node with key k from the BST.
        
        Args:
            k: The key of the node we want to find.
        
        Returns:
            The node with key k.

        Running Time:
            O(log(n))
        """
        return self.root.find(k)

    def insert(self, k):
        """
        Inserts a node with key k into the BST.
        
        Args:
            k: The key of the node to be inserted.
        
        Returns:
            The node inserted.
        
        Running Time:
            O(log(n))
        """
        node = self.node_class(k, None)
        if(self.root is None):
            self.root = node
        else:
            self.root.insert(node)
        return node

    def remove(self, k):
        """
        Removes and returns the node with key k from the BST.

        Args:
            k: The key of the node that we want to delete.
            
        Returns:
            The deleted node with key k.

        Running Time:
            O(log(n))
        """
        node = self.find(k)
        if(node is self.root):
            pseudoroot = self.node_class(0, None)
            pseudoroot.left = self.root
            self.root.parent = pseudoroot
            root = self.root.remove()
            self.root = pseudoroot.left
            # wrong first time:
            # the root may be the only one node
            # have to check None
            if self.root is not None:
                self.root.parent = None
            return root
        else:
            return node.remove()

    def next_larger(self, k):
        """
        Returns the node with the next larger key (the successor) in the BST.

        Running Time:
            O(log(n))
        """
        node = self.root.find(k) 
        if(node is None):
            return None
        else:
            return node.next_larger()

    def check_ri(self):
        """
        Checks the BST representation invariant.
        
        Assert is not true if the RI is violated.
        """
        if self.root is not None:
            assert(self.root.parent is None)
            self.root.check_ri()

    def find_min(self):
        """Returns the minimum key of this BST."""
        
        return self.root and self.root.find_min().key

    def find_max(self):
        """Returns the maxmum key of this BST."""
        
        return self.root and self.root.find_max().key


        