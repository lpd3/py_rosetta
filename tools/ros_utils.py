# ros_utils.py: Useful utilities for Rosetta Code problems

import operator


def identity(x):
    '''Given any object x, return x unchanged'''
    return x


def index_or_none(item, iter):
    '''Given an item and an iterable, return the index of the leftmost example of item in 
       sequence. If item is not in sequence, return None.'''
    for (index, value) in enumerate(iter):
        if value == item:
            return index
    return None


'''Binary Heap'''


class BinaryHeap:
    def __init__(self, data_seq=None, *, comp=operator.gt, key=identity, allow_duplicates=False):
        self.heap = []
        self.comp = comp
        self.key = key
        self.allow_duplicates = allow_duplicates
        if data_seq:
            for item in data_seq:
                self.heappush(item)

    def is_empty(self):
        return len(self.heap) == 0

    def heappush(self, item):
        if not self.allow_duplicates:
            if self.heapsearch(item) is not None:
                return
        self.heap.append(item)
        self._sift_up()

    def heappop(self):
        assert not self.is_empty(), \
          "Cannot pop from empty BinaryHeap."
        item, self.heap[0] = self.heap[0], self.heap[-1]
        self.heap.pop()
        self._sift_down()
        return item

    def heaplen(self):
        return len(self.heap)

    def heappeek(self):
        assert not self.is_empty(), \
          "Cannot peek into empty BinaryHeap."
        return self.heap[0]

    def heappushpop(self, pushed):
        if self.is_empty():
            return pushed
        top = self.heappeek()
        if self.comp(self.key(top), self.key(pushed)):
            if not self.allow_duplicates and pushed in self.heap:
                return self.heappop()
            popped, self.heap[0] = self.heap[0], pushed
            self._sift_down()
            return popped
        return pushed
    
    def heapsearch(self, item):
        return index_or_none(item, self.heap)

    def heapdelete(self, item):
        pivot_index = self.heapsearch(item)
        if pivot_index is not None:
            swapped = self.heap[-1]
            self.heap[pivot_index], self.heap[-1] = swapped, item
            self.heap.pop()
            if self.comp(self.key(swapped), self.key(item)):
                self._sift_up(pivot_index)
            elif self.comp(self.key(item), self.key(swapped)):
                self._sift_down(pivot_index)
            else:
                pass
        else:
            pass
                
    def _sift_up(self, index=None):
        heap_len = len(self.heap)
        if heap_len < 2 or (index is not None and index >= heap_len):
            return
        if index is None:
            cur_index = heap_len - 1
        else:
            cur_index = index
        item = self.heap[cur_index]
        while cur_index > 0:
            parent_index = (cur_index - 1) // 2
            parent = self.heap[parent_index]
            if self.comp(self.key(item), self.key(parent)):
                self.heap[parent_index], self.heap[cur_index] = item, parent
                cur_index = parent_index
            else:
                return

    def _sift_down(self, index=0):
        heap_len = len(self.heap)
        if heap_len < 2 or index >= heap_len:
            return
        cur_index = index
        item = self.heap[cur_index]
        while True:
            left_index = 2 * cur_index + 1
            right_index = left_index + 1
            if left_index >= heap_len:
                return
            if right_index < heap_len:
                left_child = self.heap[left_index]
                right_child = self.heap[right_index]
                if self.comp(self.key(left_child), self.key(right_child)):
                    better_child = left_child
                    better_index = left_index
                    worse_child = right_child
                    worse_index = right_index
                else:
                    better_child = right_child
                    better_index = right_index
                    worse_child = left_child
                    worse_index = left_index
                if self.comp(self.key(better_child), self.key(item)):
                    self.heap[cur_index], self.heap[better_index] = better_child, item
                    cur_index = better_index
                elif self.comp(self.key(worse_child), self.key(item)):
                    self.heap[cur_index], self.heap[worse_index] = worse_child, item
                    cur_index = worse_index
                else:
                    return
            else:
                child = self.heap[left_index]
                if self.comp(self.key(child), self.key(item)):
                    self.heap[cur_index], self.heap[left_index] = child, item
                return
