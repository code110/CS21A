import unittest

import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

from cormen_lib.factory_utils import make_array, make_stack
from cormen_lib.test_utils import build_and_run_watched_suite, run_generic_test, to_cormen_string, cormen_equals
from cormen_lib.trees import BinaryTreeNode, NaryTreeNode
from cormen_lib.stacks import Stack
from cormen_lib.linked_lists import SinglyLinkedListNode

from ps3 import sort_stack, linked_list_min, weighted_sum, non_recursive_in_order, is_isomorphic, lowest_common_ancestor

class SortStackTest(unittest.TestCase):

    def test_zero_elems(self):
        s = Stack()
        expected = Stack()
        run_generic_test(s, expected, sort_stack, in_place=True, custom_comparator=self.__custom_stack_comparator)

    def test_one_elem(self):
        s = make_stack([1])
        expected = make_stack([1])
        run_generic_test(s, expected, sort_stack, in_place=True, custom_comparator=self.__custom_stack_comparator)

    def test_basic_stack(self):
        s = make_stack([5, 2, 4, 3, 1])
        expected = make_stack([1, 2, 3, 4, 5])
        run_generic_test(s, expected, sort_stack, in_place=True, custom_comparator=self.__custom_stack_comparator)

    def test_stability(self):
        s = make_stack([self._DummyObject("C", 1), self._DummyObject("B", 1), self._DummyObject("B", 2), self._DummyObject("B", 3), self._DummyObject("A", 1), self._DummyObject("B", 4)])
        expected = make_stack([self._DummyObject("A", 1), self._DummyObject("B", 1), self._DummyObject("B", 2), self._DummyObject("B", 3), self._DummyObject("B", 4), self._DummyObject("C", 1)])
        run_generic_test(s, expected, sort_stack, in_place=True, custom_comparator=self._DummyObject.compare_stacks)

# ------------------------------------------------------------------------------------------------
    
    class _DummyObject(unittest.TestCase):
        '''A dummy object used to test stability of a sorting algorithm.'''

        def __init__(self, sortable_id, unique_id):
            self.sortable_id = sortable_id
            self.unique_id = unique_id

        def _compare(self, other, method):
            return method(self.sortable_id, other.sortable_id)

        def __lt__(self, other):
            return self._compare(other, lambda s, o: s < o)

        def __le__(self, other):
            return self._compare(other, lambda s, o: s <= o)

        def __eq__(self, other):
            return self._compare(other, lambda s, o: s == o)

        def __ge__(self, other):
            return self._compare(other, lambda s, o: s >= o)

        def __gt__(self, other):
            return self._compare(other, lambda s, o: s > o)

        def __ne__(self, other):
            return self._compare(other, lambda s, o: s != o)
        
        def __str__(self):
            return f'{self.sortable_id}.{self.unique_id}'

        def true_eq(self, other):
            return self.sortable_id == other.sortable_id and self.unique_id == other.unique_id

        @staticmethod
        def compare_stacks(s1, s2):
            if s1.size() != s2.size():
                return False
            s1_temp = Stack()
            s2_temp = Stack()
            while not s1.is_empty():
                s1_temp.push(s1.pop())
                s2_temp.push(s2.pop())
                if not s1_temp.top().true_eq(s2_temp.top()): return False
            while not s1_temp.is_empty():
                s1.push(s1_temp.pop())
                s2.push(s2_temp.pop())
            return True

    # A custom stack comparator is required until AFTER version 1.1.0 to compare Stacks
    # See issue #8 on github  at https://github.com/Cormen-Lib-Developers/Cormen-Lib/issues/8 for more info
    def __custom_stack_comparator(self, s1, s2):
        if s1.size() != s2.size():
            return False
        s1_temp = Stack()
        s2_temp = Stack()
        while not s1.is_empty():
            s1_temp.push(s1.pop())
            s2_temp.push(s2.pop())
            if not cormen_equals(s1_temp.top(), s2_temp.top()): return False
        while not s1_temp.is_empty():
            s1.push(s1_temp.pop())
            s2.push(s2_temp.pop())
        return True


class LinkedListMinTest(unittest.TestCase):

    def test_no_min(self):
        head = None
        expected = None
        run_generic_test(head, expected, linked_list_min)

    def test_one_node_list(self):
        head = SinglyLinkedListNode(2)
        expected = 2
        run_generic_test(head, expected, linked_list_min)

    def test_simple_list(self):
        head = SinglyLinkedListNode(4)
        head.next = SinglyLinkedListNode(5)
        head.next.next = SinglyLinkedListNode(6)
        expected = 4
        run_generic_test(head, expected, linked_list_min)

    def test_min_at_end(self):
        head = SinglyLinkedListNode(6, SinglyLinkedListNode(6, SinglyLinkedListNode(4, SinglyLinkedListNode(4,
                                                                                                            SinglyLinkedListNode(
                                                                                                                3)))))
        expected = 3
        run_generic_test(head, expected, linked_list_min)

    def test_negative_numbers(self):
        head = SinglyLinkedListNode(-5, SinglyLinkedListNode(6, SinglyLinkedListNode(-10, SinglyLinkedListNode(100,
                                                                                                               SinglyLinkedListNode(
                                                                                                                   -400,
                                                                                                                   SinglyLinkedListNode(
                                                                                                                       0))))))
        expected = -400
        run_generic_test(head, expected, linked_list_min)


class WeightedSumTest(unittest.TestCase):

    def test_none(self):
        root = None
        expected = 0
        run_generic_test(root, expected, weighted_sum)

    def test_one_node(self):
        root = BinaryTreeNode(-1)
        expected = -1
        run_generic_test(root, expected, weighted_sum)

    def test_not_full_tree(self):
        root = BinaryTreeNode(1, None, BinaryTreeNode(3, BinaryTreeNode(4), BinaryTreeNode(5)))
        expected = 1 * 1 + 2 * 3 + 3 * 4 + 3 * 5
        run_generic_test(root, expected, weighted_sum)

    def test_tree_with_negatives(self):
        root = BinaryTreeNode(1, BinaryTreeNode(-6, BinaryTreeNode(15), BinaryTreeNode(-7, None, BinaryTreeNode(21))),
                              BinaryTreeNode(0, BinaryTreeNode(9), BinaryTreeNode(3)))
        expected = 1 * 1 + -6 * 2 + 0 * 2 + 15 * 3 + -7 * 3 + 9 * 3 + 3 * 3 + 21 * 4
        run_generic_test(root, expected, weighted_sum)


class NonRecursiveInOrderTest(unittest.TestCase):

    def test_none(self):
        root = None
        n = 0
        expected = make_array([])
        run_generic_test([root, n], expected, non_recursive_in_order,
                         params_to_string=self.non_recursive_in_order_to_string)

    def test_one_node(self):
        root = BinaryTreeNode(10)
        n = 1
        expected = make_array([10])
        run_generic_test([root, n], expected, non_recursive_in_order,
                         params_to_string=self.non_recursive_in_order_to_string)

    def test_full_left_tree(self):
        root = BinaryTreeNode(1, BinaryTreeNode(2, BinaryTreeNode(3, BinaryTreeNode(4), BinaryTreeNode(5)),
                                                BinaryTreeNode(6, BinaryTreeNode(7), BinaryTreeNode(8))),
                              BinaryTreeNode(9))
        n = 9
        expected = make_array([4, 3, 5, 2, 7, 6, 8, 1, 9])
        run_generic_test([root, n], expected, non_recursive_in_order,
                         params_to_string=self.non_recursive_in_order_to_string)

    def test_jagged_tree(self):
        root = BinaryTreeNode(1, BinaryTreeNode(2, None, BinaryTreeNode(6, BinaryTreeNode(7), BinaryTreeNode(8))),
                              BinaryTreeNode(9, None, BinaryTreeNode(11, None, BinaryTreeNode(12))))
        n = 8
        expected = make_array([2, 7, 6, 8, 1, 9, 11, 12])
        run_generic_test([root, n], expected, non_recursive_in_order,
                         params_to_string=self.non_recursive_in_order_to_string)

    def non_recursive_in_order_to_string(self, params):
        return f'{to_cormen_string(params[0])}, {params[1]}'


class IsIsomorphicTest(unittest.TestCase):

    def test_none(self):
        root1 = None
        root2 = BinaryTreeNode(5)
        expected = False
        run_generic_test([root1, root2], expected, is_isomorphic, params_to_string=self.is_isomorphic_to_string)

    def test_single_elemF(self):
        root1 = BinaryTreeNode(5)
        root2 = BinaryTreeNode(6)
        expected = False
        run_generic_test([root1, root2], expected, is_isomorphic, params_to_string=self.is_isomorphic_to_string)

    def test_single_elemT(self):
        root1 = BinaryTreeNode(10)
        root2 = BinaryTreeNode(10)
        expected = True
        run_generic_test([root1, root2], expected, is_isomorphic, params_to_string=self.is_isomorphic_to_string)

    def test_jagged_tree(self):
        root1 = BinaryTreeNode(0, BinaryTreeNode(2, BinaryTreeNode(4), BinaryTreeNode(5, BinaryTreeNode(7))),
                               BinaryTreeNode(3, BinaryTreeNode(6, BinaryTreeNode(10))))
        root2 = BinaryTreeNode(0, BinaryTreeNode(3, BinaryTreeNode(6, BinaryTreeNode(10))),
                               BinaryTreeNode(2, BinaryTreeNode(4), BinaryTreeNode(5, BinaryTreeNode(7))))
        expected = True
        run_generic_test([root1, root2], expected, is_isomorphic, params_to_string=self.is_isomorphic_to_string)

    def test_not_isomorphic(self):
        root1 = BinaryTreeNode(1, BinaryTreeNode(2, BinaryTreeNode(4), BinaryTreeNode(5, BinaryTreeNode(7))),
                               BinaryTreeNode(3))
        root2 = BinaryTreeNode(1, BinaryTreeNode(3, BinaryTreeNode(4), BinaryTreeNode(5, BinaryTreeNode(7))),
                               BinaryTreeNode(2))
        expected = False
        run_generic_test([root1, root2], expected, is_isomorphic, params_to_string=self.is_isomorphic_to_string)

    def test_simple_isomorphic(self):
        root1 = BinaryTreeNode(1, BinaryTreeNode(2, BinaryTreeNode(4), BinaryTreeNode(5, BinaryTreeNode(7))),
                               BinaryTreeNode(3))
        root2 = BinaryTreeNode(1, BinaryTreeNode(3),
                               BinaryTreeNode(2, BinaryTreeNode(4), BinaryTreeNode(5, BinaryTreeNode(7))))
        expected = True
        run_generic_test([root1, root2], expected, is_isomorphic, params_to_string=self.is_isomorphic_to_string)

    def test_multiple_swaps(self):
        root1 = BinaryTreeNode(0, BinaryTreeNode(2, BinaryTreeNode(4),
                                                 BinaryTreeNode(5, BinaryTreeNode(7), BinaryTreeNode(19))),
                               BinaryTreeNode(3, BinaryTreeNode(6, BinaryTreeNode(10, None, BinaryTreeNode(33)))))
        root2 = BinaryTreeNode(0, BinaryTreeNode(3, BinaryTreeNode(6, BinaryTreeNode(10, BinaryTreeNode(33)))),
                               BinaryTreeNode(2, BinaryTreeNode(4),
                                              BinaryTreeNode(5, BinaryTreeNode(19), BinaryTreeNode(7))))
        expected = True
        run_generic_test([root1, root2], expected, is_isomorphic, params_to_string=self.is_isomorphic_to_string)

    def is_isomorphic_to_string(self, params):
        return f'{to_cormen_string(params[0])}, {to_cormen_string(params[1])}'


# TODO needs to be rewritten
class LowestCommonAncestorTest(unittest.TestCase):

    def test_none(self):
        root = None
        v = None
        w = None
        expected = None
        run_generic_test([root, v, w], expected, lowest_common_ancestor)

    def test_self(self):
        root = NaryTreeNode('0')
        v = root
        w = root
        expected = root
        run_generic_test([root, v, w], expected, lowest_common_ancestor, params_to_string=self.LCA_to_string,
                         expected_to_string=self.LCA_expected_to_string, output_to_string=self.LCA_output_to_string)

    def test_LCA_is_root_binary_tree(self):
        v = NaryTreeNode('h')
        w = NaryTreeNode('e')
        a = NaryTreeNode('a')
        b = NaryTreeNode('b')
        c = NaryTreeNode('c')
        d = NaryTreeNode('d')
        f = NaryTreeNode('f')
        g = NaryTreeNode('g')

        a.leftmost_child = b
        b.parent = a
        f.parent = a
        b.right_sibling = f
        b.leftmost_child = c
        c.parent = b
        d.parent = b
        c.right_sibling = d
        d.leftmost_child = w
        w.parent = d
        f.leftmost_child = g
        g.parent = f
        g.leftmost_child = v
        v.parent = g

        expected = a
        run_generic_test([a, v, w], expected, lowest_common_ancestor, params_to_string=self.LCA_to_string,
                         expected_to_string=self.LCA_expected_to_string, output_to_string=self.LCA_output_to_string)

    def test_LCA_is_root(self):
        v = NaryTreeNode('v')
        w = NaryTreeNode('w')
        h = NaryTreeNode('h')
        e = NaryTreeNode('e')
        a = NaryTreeNode('a')
        b = NaryTreeNode('b')
        c = NaryTreeNode('c')
        d = NaryTreeNode('d')
        l = NaryTreeNode('l')
        z = NaryTreeNode('z')
        y = NaryTreeNode('y')
        x = NaryTreeNode('x')
        f = NaryTreeNode('f')
        g = NaryTreeNode('g')

        a.leftmost_child = b
        b.parent = a
        z.parent = a
        f.parent = a
        b.right_sibling = z
        z.right_sibling = f
        b.leftmost_child = c
        c.parent = b
        d.parent = b
        c.right_sibling = d
        y.parent = z
        x.parent = z
        w.parent = z
        y.right_sibling = x
        x.right_sibling = w
        f.leftmost_child = g
        g.parent = f
        d.leftmost_child = l
        l.parent = d
        w.leftmost_child = h
        h.parent = w
        g.leftmost_child = v
        v.parent = g
        v.leftmost_child = e
        e.parent = v

        expected = a
        run_generic_test([a, v, w], expected, lowest_common_ancestor, params_to_string=self.LCA_to_string,
                         expected_to_string=self.LCA_expected_to_string, output_to_string=self.LCA_output_to_string)

    def test_LCA_is_not_root(self):
        v = NaryTreeNode('v')
        w = NaryTreeNode('w')
        a = NaryTreeNode('a')
        b = NaryTreeNode('b')
        z = NaryTreeNode('z')
        c = NaryTreeNode('c')
        d = NaryTreeNode('d')
        p = NaryTreeNode('p')
        q = NaryTreeNode('q')
        f = NaryTreeNode('f')
        l = NaryTreeNode('l')
        g = NaryTreeNode('g')
        x = NaryTreeNode('x')
        y = NaryTreeNode('y')

        a.leftmost_child = b
        b.parent = a
        z.parent = a
        b.right_sibling = z
        b.leftmost_child = c
        c.parent = b
        d.parent = b
        c.right_sibling = d
        z.leftmost_child = p
        p.parent = z
        q.parent = z
        f.parent = z
        p.right_sibling = q
        q.right_sibling = f
        c.leftmost_child = v
        v.parent = c
        d.leftmost_child = l
        l.parent = d
        f.leftmost_child = g
        g.parent = f
        v.leftmost_child = x
        x.parent = f
        l.leftmost_child = w
        w.parent = l
        w.leftmost_child = y
        y.parent = w

        run_generic_test([a, v, w], b, lowest_common_ancestor, params_to_string=self.LCA_to_string,
                         expected_to_string=self.LCA_expected_to_string, output_to_string=self.LCA_output_to_string)

    def LCA_to_string(self, params):
        return f'{to_cormen_string(params[0])}, {params[1].data}, {params[2].data}'

    def LCA_expected_to_string(self, expected):
        return f'{to_cormen_string(expected.data)}'

    def LCA_output_to_string(self, output):
        return f'{to_cormen_string(output.data) if output is not None else None}'


if __name__ == '__main__':
    build_and_run_watched_suite(
        [SortStackTest, LinkedListMinTest, WeightedSumTest, LowestCommonAncestorTest, NonRecursiveInOrderTest, IsIsomorphicTest], 4)
