"""
    A van Emde Boas Tree implementation.
    van Emde Boas Tree is a fast data structure which is enable operations in lg(lgu) time.
    van Emde Boas Tree follows the divide and conquer paradigm.
"""
import math

class VEB(object):
    """
    Attributes:
        u: universal size
        summary: summary vEB tree (save the higher bits of each key)
        clusters: vEB tree clusters list (save the lower bits of each key, indexed by higher bits)
        min: the min key in this tree
        max: the max key in this tree
        root_u_ceil: higher bits length
        root_u_floor: lower bits length
    """
    def __init__(self, u):
        """
        Create a vEB tree cluster.

        Args:
            u: the universe size
        
        Running Time:
            O(1)
        """
        self.u = u
        lg = math.log(u, 2)/2
        self.__root_u_floor = 2**math.floor(lg)
        self.__root_u_ceil = 2**math.ceil(lg)
        self.summary = VEB(self.__root_u_ceil) if u > 2 else None
        self.clusters = [VEB(self.__root_u_floor) for _ in range(self.__root_u_ceil)] if u > 2 else None
        self._min = None
        self._max = None

    def __high(self, x):
        """
        extract higher bit of a number

        Args:
            x: the number
        
        Running Time:
            O(1)
        """
        return x // self.__root_u_floor

    def __low(self, x):
        """
        extract lower bit of a number

        Args:
            x: the number
        
        Running Time:
            O(1)
        """
        return x % self.__root_u_floor

    def __index(self, x, y):
        """
        compute the number from its higher bits and lower bits

        Args:
            x: the higher bits
            y: the lower bits
        
        Running Time:
            O(1)
        """
        return x * self.__root_u_floor + y

    def minimum(self):
        """
        Return the minimum key in the current tree.
        
        Running Time:
            O(1)
        """
        return self._min
    
    def maximum(self):
        """
        Return the maximum key in the current tree.
        
        Running Time:
            O(1)
        """
        return self._max

    def is_member(self, key):
        """
        Return whether the key is in the current tree.
        
        Running Time:
            O(lg(lgu))
        """
        if(key == self._min or key == self._max):
            return True
        elif(self.u == 2):
            return False
        else:
            return self.clusters[self.__high(key)].is_member(self.__low(key))

    def successor(self, key):
        """
        Return the successor key.
        
        Running Time:
            O(lg(lgu))
        """
        if(self.u == 2):
            if(key == 0 and self._max == 1):
                return 1
            else:
                return None
        elif(self._min is not None and key < self._min):
            return self._min
        else:
            high = self.__high(key)
            low = self.__low(key)
            maxlow = self.clusters[high]._max
            if(maxlow is not None and low < maxlow):
                offset = self.clusters[high].successor(low)
                return self.__index(high, offset)
            else:
                successor_cluster = self.summary.successor(high)
                if(successor_cluster is None):
                    return None
                else:
                    offset = self.clusters[successor_cluster]._min
                    return self.__index(successor_cluster, offset)

    def predecessor(self, key):
        """
        Return the predecessor key.
        
        Running Time:
            O(lg(lgu))
        """
        if(self.u == 2):
            if(key == 1 and self._min == 0):
                return 0
            else:
                return None
        elif(self._max is not None and key > self._max):
            return self._max
        else:
            high = self.__high(key)
            low = self.__low(key)
            minlow = self.clusters[high]._min
            if(minlow is not None and low > minlow):
                offset = self.clusters[high].predecessor(low)
                return self.__index(high, offset)
            else:
                predecessor_cluster = self.summary.predecessor(high)
                if(predecessor_cluster is None):
                    if(self._min is not None and key > self._min):
                        return self._min
                    else:
                        return None
                else:
                    offset = self.clusters[predecessor_cluster]._max
                    return self.__index(predecessor_cluster, offset)
    
    def __insert_empty(self, key):
        """
        Insert a key into a empty tree
        
        Running Time:
            O(1)
        """
        self._min = key
        self._max = key

    def insert(self, key):
        """
        Insert a key into a tree
        
        Running Time:
            O(lg(lgu))
        """
        if(self._min is None):
            self.__insert_empty(key)
        else:
            if(key < self._min):
                self._min, key = key, self._min
            if(self.u > 2):
                high = self.__high(key)
                low = self.__low(key)
                if(self.clusters[high]._min is None):
                    self.summary.insert(high)
                    self.clusters[high].__insert_empty(low)
                else:
                    self.clusters[high].insert(low)
            if(key > self._max):
                self._max = key
    
    def delete(self, key):
        """
        Delete a key from a tree
        
        Running Time:
            O(lg(lgu))
        """
        if(self._min == self._max):
            self._min = None
            self._max = None
        elif(self.u == 2):
            if(key == 0):
                self._min = 1
            else:
                self._min = 0
            self._max = self._min
        else:
            if(key == self._min):
                first_cluster = self.summary._min
                key = self.__index(first_cluster, self.clusters[first_cluster]._min)
                self._min = key
            high = self.__high(key)
            low = self.__low(key)
            self.clusters[high].delete(low)
            if(self.clusters[high]._min is None):
                self.summary.delete(high)
                if(key == self._max):
                    summary_max = self.summary._max
                    if(summary_max is None):
                        self._max = self._min
                    else:
                        self._max = self.__index(summary_max, self.clusters[summary_max]._max)
            elif(key == self._max):
                self._max = self.__index(high, self.clusters[high]._max)

