"""
    A Heap/Priority queue implementation
    Last modified at: 2020/4/28
"""

class Node:
    """A node in the Heap."""
    def __init__(self, value, k):
        """Creates a node.
        
        Args:
            value: The node's value.
            k: key of the node.
        
        Running Time:
            O(1)
        """
        self.key = k
        self.val = value

    def __str__(self):
        return f"{self.__class__.__name__}({self.key}, {self.val})"


class Heap:
    """A Heap"""
    def __init__(self, values: list):
        """Creates Heap.
        
        Running Time:
            O(n*log(n))
        """
        self.heap = []
        self._build_heap(values)

    def _build_heap(self, values: list):
        """Builds the heap from a list.
        
        Args:
            values: The unordered values.

        Running Time:
            O(n*log(n))
        """
        lastIdx = len(values) - 1
        # start from last nodes that has child
        startFrom = self._get_parent_idx(lastIdx)
        for i in values:
            self.heap.append(i)
        # check up down
        for i in range(startFrom, -1, -1):
            self._heap_down(i)
        # debug
        # self.__check_ri()

    def _get_parent_idx(self, idx):
        # O(1)
        return (idx - 1) // 2

    def _get_left_child_idx(self, idx):
        # O(1)
        return idx * 2 + 1

    def _get_right_child_idx(self, idx):
        # O(1)
        return idx * 2 + 2

    def _heap_down(self, idx):
        # O(log(n))
        smaller_idx = self.__get_smaller_child_idx(idx)
        if(not smaller_idx == idx): # if equals, we're done
            # if not, swap and check next node
            self.heap[idx], self.heap[smaller_idx] = self.heap[smaller_idx], self.heap[idx]
            self._heap_down(smaller_idx)

    def _heap_top(self, idx):
        # O(log(n))
        parent_idx = self._get_parent_idx(idx)
        if(parent_idx >= 0 and self.heap[parent_idx].key > self.heap[idx].key): # if not, we're done
            # if true, swap and check next node
            self.heap[idx], self.heap[parent_idx] = self.heap[parent_idx], self.heap[idx]
            self._heap_top(parent_idx)
                

    # private
    def __get_smaller_child_idx(self, idx):
        # O(1)
        l = self._get_left_child_idx(idx)
        r = self._get_right_child_idx(idx)
        smaller_idx = idx
        if(l < len(self.heap) and self.heap[l].key < self.heap[smaller_idx].key):
            smaller_idx = l
        if(r < len(self.heap) and self.heap[r].key < self.heap[smaller_idx].key):
            smaller_idx = r
        return smaller_idx

    # public
    def min(self):
        """Returns the node with minimum key from the heap.

        Running Time:
            O(log(n))
        """
        if(len(self.heap) > 0):
            return self.heap[0]
        else:
            return None

    def extract_min(self):
        """Removes and returns the node with minimum key from the heap.

        Running Time:
            O(log(n))
        """
        if(len(self.heap) > 0):
            # swap first and last
            self.heap[-1], self.heap[0] = self.heap[0], self.heap[-1]
            minimum = self.heap.pop()
            # heapy root
            self._heap_down(0)
            # debug
            # self.__check_ri()
            # remove last(min) and return it
            return minimum
        else:
            return None

    def insert(self, node):
        """Inserts a node into the Heap.
        
        Args:
            node: The node to be inserted.
        
        Running Time:
            O(log(n))
        """
        self.heap.append(node)
        # check bottom up
        self._heap_top(len(self.heap)-1)
        # debug
        # self.__check_ri()

    def is_empty(self):
        """Inserts a node into the Heap.
        
        Args:
            node: The node to be inserted.
        
        Returns:
            Whether the heap is empty.

        Running Time:
            O(1)
        """
        return True if len(self.heap) == 0 else False

    def print_values(self):
        """Print every node in the Heap.

        Running Time:
            O(n)
        """
        for el in self.heap:
            print(el)
    
    # debugging mathod:
    # only call when debugging,
    # check the representation invariant when heap changed
    def __check_ri(self):
        # O(n)
        lastIdx = len(self.heap) - 1
        # start from last nodes that has child
        startFrom = self._get_parent_idx(lastIdx)
        for i in range(startFrom, -1, -1):
            l = self._get_left_child_idx(i)
            if(l <= lastIdx):
                assert(self.heap[i].key <= self.heap[l].key)
            r = self._get_right_child_idx(i)
            if(r <= lastIdx):
                assert(self.heap[i].key <= self.heap[r].key)

