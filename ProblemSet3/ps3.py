from cormen_lib.trees import BinaryTreeNode, NaryTreeNode, depth
from cormen_lib.arrays import Array
from cormen_lib.stacks import Stack
from cormen_lib.queues import Queue

# ************************** DO NOT MODIFY ABOVE THIS LINE ******************************

# Sort the original stack, do not return a new one
def sort_stack(s):
    if not s.is_empty():
        temp = s.pop()
        sort_stack(s)
        insert_stack(s,temp)

def insert_stack(s,temp):
    if s.is_empty() or temp > s.top():
        s.push(temp)
    else:
        top = s.pop()
        insert_stack(s,temp)
        s.push(top)

# return the minimum data value itself, not the node
def linked_list_min(head):
    if head.next is null:
        return min
    min =  head.data


def weighted_sum(root):
    pass

# return the node, not its data
# you may not need to use the root field
# See NaryTreeNode slides for syntax and associated methods
def lowest_common_ancestor(root, v, w):
    pass

# return an array of size n. The order of the elements in the array should be the order they are hit in the in-order traversal.
def non_recursive_in_order(root, n):
    pass

def is_isomorphic(root1, root2):
    pass