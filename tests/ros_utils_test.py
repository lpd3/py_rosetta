from random import randrange
from unittest import TestCase
from ..tools.ros_utils import identity, index_or_none, BinaryHeap 
import operator
import unittest


class TestSimpleUtilities(TestCase):

    def test_identity(self):
        self.assertEqual(12345, identity(12345))
        self.assertEqual("Hello, there!", identity("Hello, there!"))
        self.assertEqual([1, 2, 3, 4, 5], identity([1, 2, 3, 4, 5]))

    def test_index_or_none(self):
        nums = [10, -20, 1.33567, -2, 6789]
        text = "GlumSchwartzkopfvex'dbyNJIQ."
        word_tuple = ("uno", "dos", "tres", "cuatro")
        for i, num in enumerate(nums):
            self.assertEqual(i, index_or_none(num, nums))
        self.assertIs(None, index_or_none(42, nums))
        for i, char in enumerate(text):
            self.assertEqual(i, index_or_none(char, text))
        self.assertIs(None, index_or_none('%', text))
        for i, word in enumerate(word_tuple):
            self.assertEqual(i, index_or_none(word, word_tuple))
        self.assertIs(None, index_or_none("imposter", word_tuple))


RUNS_PER_TEST = 20
MAX_DATA_SIZE = 100

        
class TestBinaryHeap(TestCase):

    def make_data_set(self, *, n=None, min_val=-1_000_000, max_val=1_000_000, is_each_unique=False):
        if n is None:
            n = randrange(1, MAX_DATA_SIZE)
        raw_data = [randrange(min_val, max_val+1) for _ in range(n)]
        if is_each_unique:
            return list(set(raw_data))
        return raw_data
        
    def test_is_empty(self):
        heap = BinaryHeap()
        self.assertTrue(heap.is_empty())
        for run in range(RUNS_PER_TEST):
            data_length = randrange(MAX_DATA_SIZE)
            data = self.make_data_set(n=data_length)
            heap.heap = data
            if data_length == 0:
                self.assertTrue(heap.is_empty())
            else:
                self.assertFalse(heap.is_empty())

    def test_heapsearch(self):
        heap = BinaryHeap()
        for i in range(RUNS_PER_TEST):
            data = self.make_data_set(is_each_unique=True)
            heap.heap = data
            for j in range(min(heap.heaplen(), RUNS_PER_TEST)):
                index = randrange(heap.heaplen())
                self.assertEqual(index, heap.heapsearch(data[index]))
            max_val = max(data)
            self.assertIs(heap.heapsearch(randrange(max_val+1, max_val+100)), None)
                
    def test_heappeek(self):
        heap = BinaryHeap()
        with self.assertRaises(AssertionError):
            heap.heappeek()
        for i in range(RUNS_PER_TEST):
            data = self.make_data_set()
            heap.heap = data
            self.assertEqual(heap.heappeek(), data[0])

    def test__sift_up(self):
        heap = BinaryHeap()
        data = [100, 19, 36, 17, 3, 25, 1] # A balanced max heap
        heap.heap = data
        heap_len = len(data)
        for i in range(RUNS_PER_TEST):
            new = randrange(-1_000_000, 1_000_001)
            while new in heap.heap:
                new = randrange(-1_000_000, 1_000_001)
            heap.heap.append(new)
            heap_len += 1
            heap._sift_up()
            for (parent_index, parent) in enumerate(heap.heap):
                left_index = (parent_index * 2) + 1
                right_index = left_index + 1
                if left_index >= heap_len:
                    break
                left = heap.heap[left_index]
                self.assertTrue(left < parent)
                if right_index <  heap_len:
                    right = heap.heap[right_index]
                    self.assertTrue(right < parent)

    def test__sift_down(self):
        heap = BinaryHeap()
        heap.heap = [100, 19, 36, 17, 3, 25, 1] # A balanced max heap
        for i in range(1000):
            next = randrange(-1_000_000, 1_000_001)
            while next in heap.heap:
                next = randrange(-1_000_000, 1_000_001)
            heap._sift_up()
        while len(heap.heap) > 1:
            _, heap.heap[0] = heap.heap[0], heap.heap[-1]
            heap.heap.pop()
            heap._sift_down()
            for (parent_index, parent) in enumerate(heap.heap):
                left_index = 2 * parent_index + 1
                if left_index >= len(heap.heap):
                    break
                left = heap.heap[left_index]
                self.assertTrue(parent > left)
                right_index = left_index + 1
                if right_index < len(heap.heap):
                    right = heap.heap[right_index]
                    self.assertTrue(parent > right)

    def test_heappop(self):
        heap = BinaryHeap()
        with self.assertRaises(AssertionError):
            heap.heappop()
        for i in range(1000):
            new = randrange(-1000000, 1000001)
            while new in heap.heap:
                new = randrange(-1000000, 1000001)
            heap.heap.append(new)
            heap._sift_up()
            data = sorted(heap.heap.copy(), reverse=True)
            output = []
            while not heap.is_empty():
                output.append(heap.heappop())
            self.assertEqual(output, data)

    def test_heappush(self):
        data = []
        heap = BinaryHeap()
        for i in range(1000):
            new = randrange(-1000000, 1000001)
            while heap.heapsearch(new) is not None:
                new = randrange(-1000000, 1000001)
            data.append(new)
            heap.heappush(new)
        results = []
        data = sorted(data, reverse=True)
        while not heap.is_empty():
            results.append(heap.heappop())
        self.assertEqual(data, results)
        
    def test_heap_initialization(self):
        data = list({randrange(-1000000, 1000001) for _ in range(1000)})
        heap = BinaryHeap(data.copy())
        data = sorted(data, reverse=True)
        results = []
        while not heap.is_empty():
            results.append(heap.heappop())
        self.assertEqual(results, data)

    def test_heappushpop(self):
        heap = BinaryHeap()
        for i in range(100):
            heap.heappush(randrange(-1000, 1001))
        # Test that attempting to pushpop an item that is greater than or equal to
        # than the greatest item on the heap returns that item and
        # does not
        # change the heap.
        init_heap = heap.heap.copy()
        for i in range(RUNS_PER_TEST):
            pushable = randrange(1001, 2002)
            popped = heap.heappushpop(pushable)
            self.assertEqual(popped, pushable)
        pushable = heap.heappeek()
        popped = heap.heappushpop(pushable)
        self.assertEqual(popped, pushable)

        self.assertEqual(heap.heap, init_heap)

        # Now, we test the case where the pushable < the
        # max value of heap. This should 1. give us the max
        # value, which will be greater than the pushable; 2.
        # add the pushable to the heap, keeping the heap balanced,
        # 3. Not change the length of the heap.
        # 4. Not alter the other items, except for their positions.
        # We have to be careful not to try to push a value that the heap
        # already contains. 5. Maintain a balanced heap.
        for i in range(RUNS_PER_TEST):
            pre_op_set = set(heap.heap.copy())
            top = heap.heappeek()
            pushed = randrange(min(heap.heap)-1000, top)
            while heap.heapsearch(pushed) is not None:
                pushed = randrange(min(heap.heap)-1000, top)
            popped = heap.heappushpop(pushed)
            self.assertGreater(popped, pushed)
            self.assertEqual(popped, top)
            self.assertEqual(len(heap.heap), len(pre_op_set))
            post_op_set = set(heap.heap)
            pre_op_set.remove(popped)
            post_op_set.remove(pushed)
            self.assertEqual(pre_op_set, post_op_set)
        results = []
        data = sorted(heap.heap.copy(), reverse=True)
        while not heap.is_empty():
            results.append(heap.heappop())
        self.assertEqual(results, data)        

    def test_heapdelete(self):
        heap = BinaryHeap()
        for i in range(1000):
            new = randrange(5000, 25001)
            while heap.heapsearch(new) is not None:
                new = randrange(5000, 25001)
            heap.heappush(new)
        pre_op = heap.heap.copy()
        # Attempting to delete an item in the heap does nothing
        for i in range(RUNS_PER_TEST):
            new = randrange(5000)
            heap.heapdelete(new)
        self.assertEqual(heap.heap, pre_op)
        # As long as there are items in the heap, deleting one of
        # those items will remove it from the heap. It will be have
        # one fewer item, the deleted item will not be present, the
        # other members will be intact, and the heap will stay balanced.
        while not heap.is_empty():
            pre_op = heap.heap.copy()
            index = randrange(len(heap.heap))
            removeable = heap.heap[index]
            pre_op.remove(removeable)
            heap.heapdelete(removeable)
            self.assertEqual(set(heap.heap), set(pre_op))
            for (parent_index, parent) in enumerate(heap.heap):
                left_index = parent_index * 2 + 1
                if left_index >= len(heap.heap):
                    break
                left = heap.heap[left_index]
                self.assertGreater(parent, left)
                right_index = left_index + 1
                if right_index < len(heap.heap):
                    right = heap.heap[right_index]
                    self.assertGreater(parent, right)
        # Now that heap is empty, attempting to delete an
        # item should do nothing.
        assert(heap.is_empty())
        heap.heapdelete(42)
        self.assertTrue(heap.is_empty())

    def test_comp_function(self):
        data = list(set([randrange(-1000000, 1000001) for _ in range(1000)]))
        heap = BinaryHeap(data, comp=operator.lt)
        results = []
        while not heap.is_empty():
            results.append(heap.heappop)

        data = sorted(data)
        self.assertEqual(results, data)
        
        
if __name__ == '__main__':
    unittest.main()
