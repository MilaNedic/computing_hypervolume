from functools import cmp_to_key
import numpy as np

"""
Main Python file which includes algorithms for computing the hyperovlume in 3- and 4-D.
"""

# --------------- Auxiliary Functions ---------------------
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
        self.next = [None, None, None, None]
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


# --------------------------------------------------------------

def clear_point(head, p):
    p.closest[1] = head
    p.closest[0] = head.next[2]
    p.cnext[1] = head
    p.cnext[0] = head.next[2]    
    p.ndomr = 0
    

def point2struct(head, p, v, d):
    # Update the node p with values from v based on dimension d
    for i in range(d):
        p.x[i] = v[i]    
    # Reset the node's properties
    clear_point(head, p)    
    return p

# --------------------- Updating Data Structures --------------------------

def add_to_z(new):
    new.next[2] = new.prev[2].next[2]
    new.next[2].prev[2] = new
    new.prev[2].next[2] = new

def remove_from_z(old):
    old.prev[2].next[2] = old.next[2]
    old.next[2].prev[2] = old.prev[2]


def setup_z_and_closest(head, new):
    closest1 = head
    closest0 = head.next[2]

    q = head.next[2].next[2]
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
                    remove_from_z(p) 
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
    return sorted(list, key=cmp_to_key(compare_points_3d))

def sort_4d(list):
    return sorted(list, key=cmp_to_key(compare_points_4d))

"Auxiliary function for printing elements of cdllist"
def print_cdllist(head, di):
    print("Circular Doubly-Linked List:")
    current = head.next[di]
    while current is not None and current != head:
        print(current.x)
        current = current.next[di] if current.next[di] != head else None


"""Sets up a circular doubly-linked list"""
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

def free_cdllist(head):
    del head

# ------------------------- Hyperovlume Indicator Algorithms ---------------------------------------
def restart_list_y(head): 
    # resets the cnext pointers for the y-dimension.
    head.next[2].cnext[1] = head
    head.cnext[0] = head.next[2]
    
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

def restart_base_setup_z_and_closest(head, new):
    # Sets up closest[0] and closest[1] for the new node
    p = head.next[2].next[2]
    closest1 = head
    closest0 = head.next[2]

    newx = new.x

    restart_list_y(head)

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

def one_contribution_3d(head, new):
    restart_base_setup_z_and_closest(head, new)
    if new.ndomr > 0:
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
    return volume

"""Main function for computing the hypervolume in 3-D"""
def hv3dplus(head):
    p = head
    area = 0
    volume = 0

    restart_list_y(head)
    p = p.next[2].next[2]

    stop = head.prev[2]

    while p != stop:
        if p.ndomr < 1:
            p.cnext[0] = p.closest[0]
            p.cnext[1] = p.closest[1]

            #print("Current p", (p.x if p!= None else None))
            #print("p ndomr", p.ndomr)
            #print("p.closest[0]", p.closest[0].x)
            #print("p.closest[1]", p.closest[1].x)
            #print("p.cnext[0].cnext[1]", p.cnext[0].cnext[1].x, "\n")

            area += compute_area_simple(p.x, 1, p.cnext[0], p.cnext[0].cnext[1])
            #print("Area:", area)

            p.cnext[0].cnext[1] = p
            p.cnext[1].cnext[0] = p
        else:
            remove_from_z(p)

        #print(f"Contribution of {p.x} is {area * (p.next[2].x[2] - p.x[2])}")
        volume += area * (p.next[2].x[2] - p.x[2])
        #print("Volume:", volume)

        p = p.next[2]

    return volume

        
"""Compute the hypervolume indicator in d=4 by iteratively
   computing the hypervolume indicator in d=3 (using hv3d+) """

def hv4dplusR(head):
    height = 0
    volume = 0
    hv = 0
    
    stop = head.prev[3]
    new = head.next[3].next[3]
    
    while new != stop:
        setup_z_and_closest(head, new)           # Compute cx and cy of 'new' and determine next and prev in z
        add_to_z(new)                            # Add 'new' to list sorted by z
        update_links(head, new, new.next[2])   # Update cx and cy of the points above 'new' in z
                                                # and remove dominated points
        
        volume = hv3dplus(head)               # Compute hv indicator in d=3 in linear time

        height = new.next[3].x[3] - new.x[3]
        #print("Hypervolume contribution of node", new.x, "is", volume * height)
        hv += volume * height                  # Update hypervolume in d=4
        
        new = new.next[3]
        
    return hv


"""
Compute the hypervolume indicator in d=4 by iteratively
computing the one contribution problem in d=3.
"""

def hv4dplusU(head):
    height = 0
    volume = 0
    hv = 0
    
    last = head.prev[3]
    new = head.next[3].next[3]
    
    while new != last:
        volume += one_contribution_3d(head, new)
        add_to_z(new)
        update_links(head, new, new.next[2])
        
        height = new.next[3].x[3] - new.x[3]
        hv += volume * height
        
        new = new.next[3]
        
    return hv

from sortedcontainers import SortedList

"""
Function for preprocessing nodes in 3-D.
Sets up closest[0] and closest[1] for each node.
Input for preprocessing is the output from setup_cdllist (head node).
"""

def preprocessing(head, d):
    di = d - 1  # Dimension index for sorting (z-axis in 3D)
    current = head.next[di]
    stop = head.prev[di]

    # Using SortedList to manage nodes by their y-coordinate, supporting custom sorting needs
    avl_tree = SortedList(key=lambda node: (node.x[1], node.x[0]))

    # Include sentinel nodes to manage edge conditions
    avl_tree.add(head)  # head is a left sentinel
    avl_tree.add(head.prev[di])  # right sentinel

    while current != stop:
        avl_tree.add(current)
        index = avl_tree.index(current)

        # Check if current node is dominated by any previous node in avl_tree
        dominated = False
        for node in avl_tree:
            if node != current and all(node.x[i] <= current.x[i] for i in range(3)) and any(node.x[i] < current.x[i] for i in range(3)):
                dominated = True
                break

        if dominated:
            current.ndomr = 1
            avl_tree.remove(current)
        else:
            # Remove nodes dominated by the current node
            nodes_to_remove = [node for node in avl_tree if node != current and all(current.x[i] <= node.x[i] for i in range(3)) and any(current.x[i] < node.x[i] for i in range(3))]
            for node in nodes_to_remove:
                avl_tree.remove(node)
                node.ndomr = 1

        # Determine closest[0]: smallest q such that q_x > p_x and q_y < p_y
        x_candidates = [node for node in avl_tree if node.x[0] > current.x[0] and node.x[1] < current.x[1]]
        if x_candidates:
            current.closest[0] = min(x_candidates, key=lambda node: node.x[0])
        else:
            current.closest[0] = head  # Fallback to sentinel if no valid candidate

        # Determine closest[1]: smallest q such that q_x < p_x and q_y > p_y
        y_candidates = [node for node in avl_tree if node.x[0] < current.x[0] and node.x[1] > current.x[1]]
        if y_candidates:
            current.closest[1] = min(y_candidates, key=lambda node: node.x[1])
        else:
            current.closest[1] = head.prev[di]  # Fallback to sentinel if no valid candidate

        # Adjust closest if it points to itself
        if current.closest[0] == current:
            current.closest[0] = head
        if current.closest[1] == current:
            current.closest[1] = head.prev[di]

        current = current.next[di]

    avl_tree.clear()  # Clean up AVL tree after processing



