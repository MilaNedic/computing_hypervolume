# -------------------- AVL Tree ---------------
from avltree import AvlTree, _avl_tree_node, _avl_tree_key
from functools import cmp_to_key
import numpy as np

# --------------- Auxiliary Functions ---------------------

# Compares tuples based on the y-coordinate
def lexicographic_less_2d(a, b):
    return (a[1] < b[1] or (a[1] == b[1] and a[0] <= b[0]))


def lexicographic_less(a, b):
    return a[2] < b[2] or (a[2] == b[2] and (a[1] < b[1] or (a[1] == b[1] and a[0] <= b[0])))

# for 4D points
def lexicographic_less_4d(a, b):
    return a[3] < b[3] or (a[3] == b[3] and (a[2] < b[2] or (a[2] == b[2] and (a[1] < b[1] or (a[1] == b[1] and a[0] <= b[0])))))

# ------------------- Data Structure ------------------------

class DLNode:
    def __init__(self, x=None):
        self.x = x if x else [None, None, None, None]
        self.closest = [None, None]  # closest in x coordinate, closest in y coordinate
        self.cnext = [None, None]  # current next

        # keeps the points sorted according to coordinates 2,3, and 4
        # (in the case of 2 and 3, only the points swept by 4 are kept)
        self.next = [None, None, None, None]

        # keeps the points sorted according to coordinates 2 and 3 (except the sentinel 3)
        self.prev = [None, None, None, None]

        self.ndomr = 0  # number of dominators


# ----------------------------- Data Structure Functions -----------------------------------------

def init_sentinels(ref, d):
    s1 = DLNode()
    s2 = DLNode()
    s3 = DLNode()

    # Set values for s1
    s1.x[0] = float('-inf')
    s1.x[1] = ref[1]
    s1.x[2] = float('-inf')
    s1.x[3] = float('-inf')
    s1.closest[0] = s2
    s1.closest[1] = s1
    s1.next[2] = s2
    s1.next[3] = s2
    s1.prev[2] = s3
    s1.prev[3] = s3 

    # Set values for s2
    s2.x[0] = ref[0]
    s2.x[1] = float('-inf')
    s2.x[2] = float('-inf')
    s2.x[3] = float('-inf')
    s2.closest[0] = s2
    s2.closest[1] = s1
    s2.next[2] = s3
    s2.next[3] = s3
    s2.prev[2] = s1
    s2.prev[3] = s1

    # Set values for s3
    s3.x[0] = s3.x[1] = float('-inf')
    s3.x[2] = ref[2]
    if d == 4:
        s3.x[3] = ref[3]
    else:
        s3.x[3] = float('-inf')
    s3.closest[0] = s2
    s3.closest[1] = s1
    s3.next[2] = s1
    s3.prev[2] = s2
    s3.prev[3] = s2

    return s1

def init_sentinels_new(list_nodes, ref, d):
    s1, s2, s3 = list_nodes[0], list_nodes[1], list_nodes[2]

    # Initialize s1 node
    s1.x = [float('-inf'), ref[1], float('-inf'), float('-inf')]
    s1.closest = [s2, s1]
    s1.next = [None, None, s2, s2]
    s1.cnext = [None, None]
    s1.prev = [None, None, s3, s3]
    s1.ndomr = 0

    # Initialize s2 node
    s2.x = [ref[0], float('-inf'), float('-inf'), float('-inf')]
    s2.closest = [s2, s1]
    s2.next = [None, None, s3, s3]
    s2.cnext = [None, None]
    s2.prev = [None, None, s1, s1]
    s2.ndomr = 0

    # Initialize s3 node
    s3.x = [float('-inf'), float('-inf'), ref[2], ref[3] if d == 4 else float('-inf')]
    s3.closest = [s2, s1]
    s3.next = [None, None, s1, None]
    s3.cnext = [None, None]
    s3.prev = [None, None, s2, s2]
    s3.ndomr = 0

    return s1


# ------------

def clear_point(list_node, p):
    p.closest[1] = list_node
    p.closest[0] = list_node.next[2]

    p.cnext[1] = list_node
    p.cnext[0] = list_node.next[2]
    
    p.ndomr = 0
    

def point2struct(list_node, p, v, d):
    # Update the node p with values from v based on dimension d
    for i in range(d):
        p.x[i] = v[i]
    
    # Reset the node's properties
    clear_point(list_node, p)
    
    return p



# --------------------- Updating Data Structures --------------------------

def add_to_z(new):
    new.next[2] = new.prev[2].next[2]
    new.next[2].prev[2] = new
    new.prev[2].next[2] = new

def remove_from_z(old):
    old.prev[2].next[2] = old.next[2]
    old.next[2].prev[2] = old.prev[2]




def setup_z_and_closest(list_, new):
    closest1 = list_
    closest0 = list_.next[2]

    q = list_.next[2].next[2]
    newx = new.x

    while q and lexicographic_less(q.x, newx):
        if q.x[0] <= newx[0] and q.x[1] <= newx[1]:
            new.ndomr += 1
        elif q.x[1] < newx[1] and (q.x[0] < closest0.x[0] or (q.x[0] == closest0.x[0] and q.x[1] < closest0.x[1])):
            closest0 = q
        elif q.x[0] < newx[0] and (q.x[1] < closest1.x[1] or (q.x[1] == closest1.x[1] and q.x[0] < closest1.x[0])):
            closest1 = q

        q = q.next[2]

    new.closest[0] = new.cnext[0] = closest0
    new.closest[1] = new.cnext[1] = closest1
    new.prev[2] = q.prev[2] if q else None
    new.next[2] = q



# ------------------- Update Links --------------------


def update_links(head, new, p):
    stop = head.prev[2]
    ndom = 0
    all_delimiters_visited = False

    while p != stop and not all_delimiters_visited:
        if p.x[0] <= new.x[0] and p.x[1] <= new.x[1] and (p.x[0] < new.x[0] or p.x[1] < new.x[1]):
            all_delimiters_visited = True
        else:
            if new.x[0] <= p.x[0]:
                if new.x[1] <= p.x[1]:
                    p.ndomr += 1
                    ndom += 1
                    remove_from_z(p)  # Assuming this is the equivalent to removeFromz in C
                elif new.x[0] < p.x[0] and (new.x[1] < p.closest[1].x[1] or (new.x[1] == p.closest[1].x[1] and (new.x[0] < p.closest[1].x[0] or (new.x[0] == p.closest[1].x[0] and new.x[2] < p.closest[1].x[2])))):
                    p.closest[1] = new
            elif new.x[1] < p.x[1] and (new.x[0] < p.closest[0].x[0] or (new.x[0] == p.closest[0].x[0] and (new.x[1] < p.closest[0].x[1] or (new.x[1] == p.closest[0].x[1] and new.x[2] < p.closest[0].x[2])))):
                p.closest[0] = new
        p = p.next[2]

    return ndom

# ----------------------------------------- Sort -----------------------------------

# compare two points in 3D with coordinates (z1, y1, x1) and (z2, y2, x2)
def compare_points_3d(p1, p2):
    for i in range(2,-1,-1):
        c1 = p1[i] # current coordinate of the first point
        c2 = p2[i] # current coordnate of the second point
        if c1 < c2:
            return -1 # p1 comes before p2
        elif c2 < c1:
            return 1 # p2 comes before p1
    return 0 # p1 and p2 are equal
        
        
# compare two points in 4D with coordinates (w1, z1, y1, x1) and (w2, z2, y2, x2)
def compare_points_4d(p1, p2):
    for i in range(3,-1,-1):
        c1 = p1[i] # current coordinate of the first point
        c2 = p2[i] # current coordnate of the second point
        if c1 < c2:
            return -1
        elif c2 < c1:
            return 1
    return 0

def compare_tree_asc_y(p1, p2):
    x1 = p1[1]
    x2 = p2[1]

    if x1 < x2:
        return -1
    elif x1 > x2:
        return 1
    else:
        return 0


# --------- Auxiliary function that compares points in 3d or in 4d and sorts them in ascending order of the last coorinate ---------------

def sort_3d(list):
    #return sorted(list, key=key_point3d)
    return sorted(list, key=cmp_to_key(compare_points_3d))

def sort_4d(list):
    #return sorted(list, key=key_point4d)
    return sorted(list, key=cmp_to_key(compare_points_4d))


"Auxiliary function which return a list of dlnodes, setup in the order which setup_cdllist returns"
def cdllist_to_list(head, di): # head = setup_cdllist(points, nalloc, n, d, ref_p) the output of setup_cdlllist
    nodes_list = []
    current = head.next[di]
    while current != head:
        nodes_list.append(current)
        # print(current.x)
        current = current.next[di]
    return nodes_list # return a list of DLNodes


"Auxiliary function for printing element of cdllist"
def print_cdllist(head, di):
    print("Circular Doubly-Linked List:")
    current = head.next[di]
    while current is not None and current != head:
        print(current.x)
        current = current.next[di] if current.next[di] != head else None




" This is now the correct implementation of setup_cdlist "
def setup_cdllist(data, n, d, ref):
    head = [DLNode() for _ in range(n + 3)]
    init_sentinels_new(head[0:3], ref, d) # init_sentinels_new accepts a list at the beginning, therefore we use head[0:3]
    di = d - 1

    if n > 0:
        # Convert data to a structured format suitable for sorting and linking
        points = np.array(data).reshape(n, d)
        if d == 3:
            # Using np.lexsort to sort by z, y, x in ascending order
            sorted_indices = np.lexsort((points[:, 0], points[:, 1], points[:, 2]))
        elif d == 4:
            # Using np.lexsort to sort by w, z, y, x in ascending order
            sorted_indices = np.lexsort((points[:, 0], points[:, 1], points[:, 2], points[:, 3]))
        sorted_points = points[sorted_indices]

        # Create nodes from sorted points
        for i, index in enumerate(sorted_indices):
            head[i + 3].x = points[index].tolist()
            if d == 3: #
                head[i + 3].x.append(0.0) # Add 0.0 for 3d points so that it matches the original code, written in C

        # Link nodes
        s = head[0].next[di]
        s.next[di] = head[3]
        head[3].prev[di] = s

        for i in range(3, n+2):
            head[i].next[di] = head[i+1] if i+1 < len(head) else head[0]
            head[i+1].prev[di] = head[i]

        s = head[0].prev[di]
        s.prev[di] = head[n+2]
        head[n+2].next[di] = s

    return head[0]


def free_cdllist(list):
    # In Python, garbage collection handles memory deallocation
    del list



# ------------------------- Hyperovlume Indicator Algorithms ---------------------------------------
def restart_list_y(list_node): # head == list
    # This function resets the cnext pointers for the y-dimension.
    list_node.next[2].cnext[1] = list_node
    list_node.cnext[0] = list_node.next[2]
    
def compute_area_simple(p, di, s, u):
    dj = 1 - di
    area = 0
    q = s
    area += (q.x[dj] - p[dj]) * (u.x[di] - p[di])

    while p[dj] < u.x[dj]:
        q = u
        u = u.cnext[di]
        area += (q.x[dj] - p[dj]) * (u.x[di] - q.x[di])

    return area



# ----------------------------------------------------------------


def restart_base_setup_z_and_closest(list, new):
    p = list.next[2].next[2]
    closest1 = list
    closest0 = list.next[2]

    newx = new.x

    restart_list_y(list)

    while p and lexicographic_less(p.x, newx):
        p.cnext[0] = p.closest[0]
        p.cnext[1] = p.closest[1]

        p.cnext[0].cnext[1] = p
        p.cnext[1].cnext[0] = p

        if p.x[0] <= newx[0] and p.x[1] <= newx[1]:
            new.ndomr += 1
        elif p.x[1] < newx[1] and (p.x[0] < closest0.x[0] or (p.x[0] == closest0.x[0] and p.x[1] < closest0.x[1])):
            closest0 = p
        elif p.x[0] < newx[0] and (p.x[1] < closest1.x[1] or (p.x[1] == closest1.x[1] and p.x[0] < closest1.x[0])):
            closest1 = p

        p = p.next[2]

    new.closest[0] = closest0
    new.closest[1] = closest1
    new.prev[2] = p.prev[2] if p else None
    new.next[2] = p


# --------------- one contribution 3d ------------------

def one_contribution_3d(cdllist, new):
    print("Entering one_contribution_3d")
    # Assume restart_base_setup_z_and_closest and compute_area_simple are already defined
    restart_base_setup_z_and_closest(cdllist, new)
    if new.ndomr > 0:
        print("Selected new node id dominated, exiting early")
        return 0
    
    new.cnext[0] = new.closest[0]
    new.cnext[1] = new.closest[1]
    area = compute_area_simple(new.x, 1, new.cnext[0], new.cnext[0].cnext[1])
    
    p = new.next[2]
    lastz = new.x[2]
    volume = 0

    while p and (p.x[0] > new.x[0] or p.x[1] > new.x[1]):
        volume += area * (p.x[2] - lastz)
        p.cnext[0] = p.closest[0]
        p.cnext[1] = p.closest[1]
        
        if p.x[0] >= new.x[0] and p.x[1] >= new.x[1]:
            area -= compute_area_simple(p.x, 1, p.cnext[0], p.cnext[0].cnext[1])
            p.cnext[1].cnext[0] = p
            p.cnext[0].cnext[1] = p
        elif p.x[0] >= new.x[0]:
            if p.x[0] <= new.cnext[0].x[0]:
                x = [p.x[0], new.x[1], p.x[2]]
                area -= compute_area_simple(x, 1, new.cnext[0], new.cnext[0].cnext[1])
                p.cnext[0] = new.cnext[0]
                p.cnext[1].cnext[0] = p
                new.cnext[0] = p
        else:
            if p.x[1] <= new.cnext[1].x[1]:
                x = [new.x[0], p.x[1], p.x[2]]
                area -= compute_area_simple(x, 0, new.cnext[1], new.cnext[1].cnext[0])
                p.cnext[1] = new.cnext[1]
                p.cnext[0].cnext[1] = p
                new.cnext[1] = p
        
        lastz = p.x[2]
        p = p.next[2]
    
    if p:
        volume += area * (p.x[2] - lastz)
    print("Volume computed:", volume)
    return volume


" this is very straightfoward and same as the c code "
" the problem occrus when seeting up examples "
def hv3dplus(list_node):
    p = list_node
    area = 0
    volume = 0

    restart_list_y(list_node)
    p = p.next[2].next[2]

    stop = list_node.prev[2]

    while p != stop:
        if p.ndomr < 1:
            p.cnext[0] = p.closest[0]
            p.cnext[1] = p.closest[1]

            print("Current p", (p.x if p!= None else None))
            print("p ndomr", p.ndomr)
            print("p.closest[0]", p.closest[0].x)
            print("p.closest[1]", p.closest[1].x)
            print("p.cnext[0].cnext[1]", p.cnext[0].cnext[1].x, "\n")

            area += compute_area_simple(p.x, 1, p.cnext[0], p.cnext[0].cnext[1])
            print("Area:", area)

            p.cnext[0].cnext[1] = p
            p.cnext[1].cnext[0] = p
        else:
            remove_from_z(p)

        volume += area * (p.next[2].x[2] - p.x[2])
        print("Volume:", volume)

        p = p.next[2]

    return volume


def cdllist_start_node(head, di):
    current = head.next[di]
    #print(current.x)
    return current
    

def cdllist_end_node(head, di, n):
    current = head.next[di]
    counter = 0
    end_of_list = DLNode()
    while current is not None and current != head:
        current = current.next[di] if current.next[di] != head else None
        counter += 1
        if counter == n - 1:
            end_of_list = DLNode(current.x)
            #print(end_of_list.x)
    return end_of_list

def cdllist_preprocessing(head, di, n):
    start_node = cdllist_start_node(head, di)
    #print("head", head.x)
    current = head.next[di]
    end_of_list = cdllist_end_node(head, di, n)
    while current is not None and current != head:
        current.closest[0] = start_node
        current.closest[1] = end_of_list
        current.cnext[0] = start_node
        current.cnext[0].cnext[1] = current.next[di]
        current = current.next[di] if current.next[di] != head else None
        
"""Compute the hypervolume indicator in d=4 by iteratively
   computing the hypervolume indicator in d=3 (using hv3d+) """

def hv4dplusR(list_):
    height = 0
    volume = 0
    hv = 0
    
    stop = list_.prev[3]
    new = list_.next[3].next[3]
    
    while new != stop:
        restart_base_setup_z_and_closest(list_, new)           # Compute cx and cy of 'new' and determine next and prev in z
        add_to_z(new)                            # Add 'new' to list sorted by z
        update_links(list_, new, new.next[2])   # Update cx and cy of the points above 'new' in z
                                                # and remove dominated points
        
        volume = hv3dplus(list_)               # Compute hv indicator in d=3 in linear time
        
        height = new.next[3].x[3] - new.x[3]
        #print("Hypervolume contribution of node", new.x, "is", volume * height)
        hv += volume * height                  # Update hypervolume in d=4
        
        new = new.next[3]
        
    return hv


"""Compute the hypervolume indicator in d=4 by iteratively
   computing the one contribution problem in d=3"""

def hv4dplusU(list_):
    height = 0
    volume = 0
    hv = 0
    
    last = list_.prev[3]
    new = list_.next[3].next[3]
    
    while new != last:
        volume += one_contribution_3d(list_, new)
        add_to_z(new)
        update_links(list_, new, new.next[2])
        
        height = new.next[3].x[3] - new.x[3]
        hv += volume * height
        
        new = new.next[3]
        
    return hv

from functools import total_ordering

@total_ordering
class ReverseComparisonTuple(tuple):
    def __lt__(self, other):
        return lexicographic_less_2d(self, other)
        

def preprocessing(node_list):
    #_K = TypeVar("_K", bound=AvlTreeLast)
    #_V = TypeVar("_V", bound=object)
    # Assuming the list_node is the start of a linked list of DLNodes

    # Create an AVL tree with a custom comparator for the y-coordinate
    avl_tree = AvlTree[ReverseComparisonTuple]()
    
    def find_le(tree, point):
        le_node = None
        for node_point in tree:
            if node_point <= point:
                if le_node is None or node_point > le_node:
                    le_node = node_point
        return le_node

    py_list = cdllist_to_list(node_list, 2)
    for idx, node in enumerate(py_list[1:-1], start=1):  # Skip sentinel nodes
        point = ReverseComparisonTuple(node.x)  # No need to reverse since we're using the avl_tree package
        avl_tree[point] = idx  # Index in node_list as key, point as value
        
    p = node_list.next[2].next[2]  # Skip the head sentinel
    stop = node_list.prev[2]  # Stop before the tail sentinel


    while p != stop:
        #print("curent point in preprocessing", p)
        point = ReverseComparisonTuple(p.x)
        le_point = find_le(avl_tree, point)
        
        # If a node to the left exists, perform comparisons
        if le_point is not None:
            le_idx = avl_tree[le_point]
            # Find the previous node that is not dominated by p
            while le_point is not None and le_point[0] >= point[0]:
                # Find the next node that could potentially dominate p
                higher_points = [k for k in avl_tree if k > le_point]
                if higher_points:
                    le_point = min(higher_points, key=lambda x: (x[1], x[0]))
                else:
                    le_point = None

            if le_point is not None:
                le_idx = avl_tree[le_point]
                p.closest[0] = le_point
                print("p.closest[0]",p.closest[0])
                p.closest[1] = le_idx
                print("p.closest[1]",p.closest[1])

        # The point is not dominated, insert it into the tree
        if p.ndomr == 0:
            avl_tree[point] = idx
        
        p = p.next[2]

    return avl_tree






