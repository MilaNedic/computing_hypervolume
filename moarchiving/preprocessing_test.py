from avltree import AvlTree
from functools import total_ordering

@total_ordering
class ReverseComparisonTuple(tuple):
    def __lt__(self, other):
        return lexicographic_less(self, other)

class DLNode:
    def __init__(self, x=None):
        self.x = x if x else [None, None, None]
        self.closest = [None, None]  # closest[0]: cx, closest[1]: cy
        self.next = None
        self.prev = None

def lexicographic_less(a, b):
    return a[2] < b[2] or (a[2] == b[2] and (a[1] < b[1] or (a[1] == b[1] and a[0] <= b[0])))


def preprocessing(head, ref):
    avl_tree = AvlTree()
    # Initialize with sentinel values based on reference point
    avl_tree[ReverseComparisonTuple(head.x)] = head
    avl_tree[ReverseComparisonTuple(head.prev[2].x)] = head.prev[2]

    p = head.next[2]  # Skip the head sentinel
    stop = head.prev[2]  # Stop before the tail sentinel
    while p != stop:
        #print("Processing node:", p.x)
        s = find_outer_delimiterx(p, avl_tree)
        #print("Outer delimiter x:", s.x if s else "None")
        remove_dominatedy(p, avl_tree, s.x if s else None)
        p.closest[0] = s
        p.closest[1] = find_outer_delimitery(p, avl_tree, s.x if s else None)
        avl_tree[ReverseComparisonTuple(p.x)] = p
        #print("Current AVL Tree Keys:", sorted(avl_tree.keys()))
        p = p.next[2]


    print("Preprocessing has finished successfully")
    return avl_tree

def find_outer_delimiterx(p, avl_tree):
    # Implement finding the outer delimiter from AVL tree in x dimension
    closest_keys = sorted(avl_tree.keys())
    #print("closest_keys", closest_keys)
    for key in closest_keys:
        if key[0] <= p.x[0]:
            return avl_tree[key]
    return None

def find_outer_delimitery(current, avl_tree, start_key):
    # Ensure the start key is in the AVL tree
    closest_keys = sorted(avl_tree.keys())
    #print("closest_keys", closest_keys)
    if start_key in closest_keys:
        start_index = closest_keys.index(start_key)
        for key in closest_keys[start_index:]:
            if key[1] <= current.x[1]:
                return avl_tree[key]
    return None

def remove_dominatedy(current, avl_tree, start_key):
    start_key = ReverseComparisonTuple(start_key)
    # Remove nodes dominated by current starting from start_key, if it exists
    #print("start_key", start_key)
    if start_key in avl_tree:
        keys_to_remove = [key for key in avl_tree if key[1] < current.x[1] and key[2] < current.x[2] and key != start_key]
        for key in keys_to_remove:
            del avl_tree[key]

points = [
    0.16, 0.86, 0.47,  
    0.66, 0.37, 0.29,
    0.79, 0.79, 0.04,
    0.28, 0.99, 0.29,
    0.51, 0.37, 0.38,
    0.92, 0.62, 0.07,
    0.16, 0.53, 0.70,
    0.01, 0.98, 0.94,
    0.67, 0.17, 0.54,
    0.79, 0.72, 0.05
]
d = 3
ref = [1.0, 1.0, 1.0]

from hv_plus import setup_cdllist_new, print_cdllist
head = setup_cdllist_new(points, 10, 10, d, ref)
avl_tree = preprocessing(head, ref)
print_cdllist(head, d-1)

from hv_plus import hv3dplus
p = head.next[2]
stop = head.prev[2]
while p != stop:
    print("Current node:", p.x)
    print("p.closest[0]", (p.closest[0].x if p.closest[0] != None else None))
    print("p.closest[1]", (p.closest[1].x if p.closest[1] != None else None))
    p = p.next[2]
    
print(list(avl_tree))
#print("Hypervolume in 3d", hv3dplus(head))
