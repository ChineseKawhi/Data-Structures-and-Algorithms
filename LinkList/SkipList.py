"""
    A skip list implementation.
    Skip list allows search, add, erase operation in O(log(n)) time with high probability (w.h.p.).
"""
import random

class Node:
    """
    Attributes:
        key: the node's key
        next: the next node
        prev: the previous node
        bottom: the bottom node in skip list (the node has same key in the level below)
    """
    def __init__(self, key):
        """
        Create a node.

        Args:
            key: the node's key
        
        Running Time:
            O(1)
        """
        self.key = key
        self.next = None
        self.prev = None
        self.bottom = None
    
    def find(self, target):
        """
        Find the node whose next node has bigger key than target.

        Args:
            target: the bigger key
        
        Return:
            The first node whose next node have the key that is bigger than target
        
        Running Time:
            O(n)
        """
        if(self.next is not None and self.next.key <= target):
            return self.next.find(target)
        else:
            return self
        
    def append(self, target):
        """
        Append a node with key of target to current node.

        Args:
            target: the key of new node
        
        Running Time:
            O(1)
        """
        # define two side
        q = self.next
        p = Node(target)
        # connect left
        self.next = p
        p.prev = self
        # connect right
        p.next = q
        if(q is not None):
            q.prev = p
        
    def delete(self):
        """
        Delete the node next.
        
        Running Time:
            O(1)
        """
        # define two side
        p = self.prev
        q = self.next
        # connect
        # if(p is not None):
        p.next = q
        if(q is not None):
            q.prev = p
        del self

            
    
class Skiplist:
    """
    Attributes:
        startList: the head node list
    """
    def __init__(self):
        """
        Create a Skiplist.
        
        Running Time:
            O(1)
        """
        self.startList = [Node(-1)]

    def search(self, target: int) -> bool:
        """
        Query whether the node with target key exist.

        Args:
            target: the target key
        
        Return:
            Whether the node with target key exist
        
        Running Time:
            O(log(n)) w.h.p.
        """
        p = self.startList[-1]
        while(p is not None and p.key < target):
            p = p.find(target)
            if(p.key == target):
                return True
            else:
                p = p.bottom
        return False

    def add(self, num: int) -> None:
        """
        Add a node with key of num.

        Args:
            num: the key of the node
        
        Running Time:
            O(log(n)) w.h.p.
        """
        p = self.startList[-1]
        s = []
        while(p is not None and p.key < num):
            p = p.find(num)
            s.append(p)
            if(p.key == num):
                s.pop()
                while(p is not None):
                    s.append(p)
                    p = p.bottom
                break
            else:
                p = p.bottom
        b = None
        p = s.pop()
        p.append(num)
        p.next.bottom = b
        b = p.next
        while(random.choice([True, False])):
            if(len(s) > 0):
                p = s.pop()
                p.append(num)
                p.next.bottom = b
                b = p.next
            else:
                start = Node(-1)
                start.next = Node(num)
                start.bottom = self.startList[-1]
                
                start.next.bottom = b
                start.next.prev = start
                self.startList.append(start)

                b = start.next        
                
    def erase(self, num: int) -> bool:
        """
        Delete the node with key of num.

        Args:
            num: the key of the node

        Return:
            Whether delete success
        
        Running Time:
            O(log(n)) w.h.p.
        """
        p = self.startList[-1]
        while(p is not None and p.key < num):
            p = p.find(num)
            if(p.key == num):
                while(p is not None):
                    q = p
                    p = p.bottom
                    q.delete()
                return True
            else:
                p = p.bottom
        return False
