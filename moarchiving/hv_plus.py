# -------------------- AVL Tree ---------------
from avltree import AvlTree, _avl_tree_node
from functools import cmp_to_key
import numpy as np

# --------------- Auxiliary Functions ---------------------

def lexicographic_less(a, b):
    return a[2] < b[2] or (a[2] == b[2] and (a[1] < b[1] or (a[1] == b[1] and a[0] <= b[0])))

# for 4D points
def lexicographic_less_4d(a, b):
    return a[3] < b[3] or (a[3] == b[3] and (a[2] < b[2] or (a[2] == b[2] and (a[1] < b[1] or (a[1] == b[1] and a[0] <= b[0])))))

# ------------------- Data Structure ------------------------

class DLNode:
    def __init__(self, x=None):
        self.x = x if x else [0.0, 0.0, 0.0, 0.0]
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

def clear_point(list, p):
    p.closest[1] = list
    p.closest[0] = list.next[2]

    p.cnext[1] = list
    p.cnext[0] = list.next[2]
    
    p.ndomr = 0
    

def point2struct(list, p, v, d):
    # Update the node p with values from v based on dimension d
    for i in range(d):
        p.x[i] = v[i]
    
    # Reset the node's properties
    clear_point(list, p)
    
    return p



# --------------------- Updating Data Structures --------------------------

def add_to_z(new):
    if new.prev[2] is not None:
        new.next[2] = new.prev[2].next[2] if new.prev[2].next[2] is not None else None  # in case new->next[2] was removed for being dominated
    else:
        new.next[2] = None
        
    if new.next[2] is not None:
        new.next[2].prev[2] = new
    if new.prev[2] is not None:
        new.prev[2].next[2] = new

def remove_from_z(old):
    if old.prev[2] is not None and old.prev[2].next[2] is not None:
        old.prev[2].next[2] = old.next[2] if old.next[2] is not None else None
    if old.next[2] is not None and old.next[2].prev[2] is not None:
        old.next[2].prev[2] = old.prev[2] if old.prev[2] is not None else None



def setup_z_and_closest(head, new):
    # Find closest nodes in the dimensions 0 and 1
    closest0 = head.next[2]  
    closest1 = head  

    q = head.next[2] # Start from the node after sentinel_start in the z dimension

    # Traverse the list to find the correct position for new_node
    while q and lexicographic_less(q.x, new.x):
        # Check dominance in dimensions 0 and 1
        if q.x[0] <= new.x[0] and q.x[1] <= new.x[1]:
            new.ndomr += 1  # Increment dominator count
        elif q.x[1] < new.x[1] and (q.x[0] < closest0[0] or (q.x[0] == closest0[0] and q.x[1] < closest0[1])):
            # Update closest0 if q is lexicographically less than the current closest0
            closest0 = q
        elif q.x[0] < new.x[0] and (q.x[1] < closest1[1] or (q.x[1] == closest1[1] and q.x[0] < closest1[0])):
            # Update closest1 if q is lexicographically less than the current closest1
            closest1 = q
        q = q.next[2]

    # Set the closest and cnext pointers
    new.closest[0] = new.cnext[0] = closest0
    new.closest[1] = new.cnext[1] = closest1

    # Insert new_node before q in the z dimension
    new.prev[2] = q.prev[2]
    new.next[2] = q
    
    #q.prev[2].next[2] = new  # Link the previous node's next to new_node
    #q.prev[2] = new  # Link q's prev to new_node
#
    #q.next[2].prev[2] = new  # Link the previous node's next to new_node
    #q.next[2] = new  # Link q's prev to new_node

    return new  # Return the newly inserted node for verification if needed



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
def cdllist_to_list(head, di): # head = setup_cdllist_new(points, nalloc, n, d, ref_p) the output of setup_cdlllist
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
def setup_cdllist_new(data, naloc, n, d, ref):
    head = [DLNode() for _ in range(naloc + 3)]
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



"The function compute_area_simple seems to return weird answers for d = 2 (if points are 3-dimensional)"
"Maybe i should try setting up a 4d case"

# ----------------------------------------------------------------




def restart_base_setup_z_and_closest(head, new_node):
    p = head.next[2]  # Skipping the first sentinel.
    closest0 = closest1 = None
    
    # Prepare to iterate through the list to find the correct position for the new_node
    # and update closest0 and closest1 accordingly.
    while p != head:
        # Ensure we're operating within valid nodes.
        if lexicographic_less(p.x, new_node.x):
            if p.x[0] < new_node.x[0] and (closest0 is None or p.x[0] > closest0.x[0]):
                closest0 = p
            if p.x[1] < new_node.x[1] and (closest1 is None or p.x[1] > closest1.x[1]):
                closest1 = p
        else:
            # Found the insertion point or a node not less than new_node lexicographically.
            break
        p = p.next[2]
    
    # Ensure closest0 and closest1 are not incorrectly pointing to the same node
    # unless it's the only valid choice.
    if closest0 == closest1 and closest0 is not None and p != head:
        # Attempt to adjust closest1 to a better fitting node if possible.
        if closest1.x[1] < new_node.x[1]:
            # Look ahead for a better match for closest1.
            next_p = closest1.next[2]
            while next_p != head and next_p.x[1] < new_node.x[1]:
                closest1 = next_p
                next_p = next_p.next[2]

    # Link the new_node into the list
    new_node.prev[2] = p.prev[2]
    new_node.next[2] = p
    if p.prev[2]:
        p.prev[2].next[2] = new_node
    p.prev[2] = new_node
    
    new_node.closest[0] = closest0
    new_node.closest[1] = closest1
    new_node.cnext[0] = closest0
    new_node.cnext[1] = closest1


# --------------- one contribution 3d ------------------

def one_contribution_3d(list_node, new_node):
    restart_base_setup_z_and_closest(list_node, new_node)
    print(f"New Node: {new_node.x}, Closest[0]: {new_node.closest[0].x if new_node.closest[0] else 'None'}, Closest[1]: {new_node.closest[1].x if new_node.closest[1] else 'None'}, ndomr: {new_node.ndomr}")

    if new_node.ndomr > 0:
        return 0

    # These checks may not be necessary if restart_base_setup_z_and_closest always sets closest.
    if not new_node.closest[0] or not new_node.closest[1]:
        return 0

    new_node.cnext[0] = new_node.closest[0]
    new_node.cnext[1] = new_node.closest[1]

    # This needs to check that new_node.cnext[0] and new_node.cnext[0].cnext[1] are not None
    area = compute_area_simple(new_node.x, 1, new_node.cnext[0], new_node.cnext[0].cnext[1])

    p = new_node.next[2]
    lastz = new_node.x[2]
    volume = 0.0

    # The loop and conditions inside it should mirror the logic in the C code exactly.
    while p and (p.x[0] > new_node.x[0] or p.x[1] > new_node.x[1]):
        volume += area * (p.x[2] - lastz)
        p.cnext[0] = p.closest[0]
        p.cnext[1] = p.closest[1]

        # This early break may be too simplistic; the C code logic is more nuanced.
        if p.x[0] >= new_node.x[0] and p.x[1] >= new_node.x[1]:
            #x = [p.x[0], new_node.x[1], p.x[2]]
            area -= compute_area_simple(p.x, 1, new_node.cnext[0], new_node.cnext[0].cnext[1])
            p.cnext[0] = p.closest[0]
            p.cnext[1] = p.closest[1]

        # Updates to area should be performed with proper checks as in the C code.
        # These checks should match the conditions in the C code.
        elif p.x[0] >= new_node.x[0]:
            if p.x[0] <= new_node.cnext[0].x[0]:
                #x = [p.x[0], new_node.x[1], p.x[2]]
                area -= compute_area_simple(p.x, 1, new_node.cnext[0], new_node.cnext[0].cnext[1])
        else:
            if p.x[1] >= new_node.x[1]:
                #x = [new_node.x[0], p.x[1], p.x[2]]
                area -= compute_area_simple(p.x, 0, new_node.cnext[1], new_node.cnext[1].cnext[0])

        lastz = p.x[2]
        p = p.next[2]

    # Ensure that the last node's z-value is being used correctly.
    # The C code uses p->x[2], which at this point would be list_tail.x[2] in Python.
    if p is not None:
        volume += area * (p.x[2] - lastz)
    
    return volume


" this is very straightfoward and same as the c code "
" the problem occrus when seeting up examples "
def hv3dplus(list_node):
    p = list_node # list of DLNodes or DLNode?
    area = 0
    volume = 0

    restart_list_y(list_node)
    p = p.next[2].next[2]

    stop = list_node.prev[2]

    while p != stop:
        if p.ndomr < 1:
            p.cnext[0] = p.closest[0]
            p.cnext[1] = p.closest[1]

            area += compute_area_simple(p.x, 1, p.cnext[0], p.cnext[0].cnext[1])

            p.cnext[0].cnext[1] = p
            p.cnext[1].cnext[0] = p
        else:
            remove_from_z(p)

        volume += area * (p.next[2].x[2] - p.x[2])

        p = p.next[2]

    return volume


#def preprocessing(node_list): # input is a lsit of dlnodes
#    avl_tree = AvlTree()  # Initialize an empty AVL tree
#
#    for idx, node in enumerate(node_list[1:-1]):  # Skip the head and tail sentinels
#        # The node's coordinates are reversed before being inserted into the AVL tree,
#        # because the last coordinate is supposed to be the most significant for sorting
#        point = tuple(reversed(node.x))
#        avl_tree[point] = str(idx)  # Use the index as the key, and the point as the value

def preprocessing(node_list):
    # Assuming the list_node is the start of a linked list of DLNodes

    # Create an AVL tree with a custom comparator for the y-coordinate
    avl_tree = AvlTree()
    
    def find_le(tree, point):
        le_node = None
        for node_point in tree:
            if node_point <= point:
                if le_node is None or node_point > le_node:
                    le_node = node_point
        return le_node

    for idx, node in enumerate(node_list[1:-1], start=1):  # Skip sentinel nodes
        point = tuple(node.x)  # No need to reverse since we're using the avl_tree package
        avl_tree[point] = idx  # Index in node_list as key, point as value
        
    p = node_list[1].next[2]  # Skip the head sentinel
    stop = node_list[-2]  # Stop before the tail sentinel


    while p != stop:
        #print("curent point in preprocessing", p)
        point = tuple(p.x)
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
                p.closest[1] = le_idx

        # The point is not dominated, insert it into the tree
        if p.ndomr == 0:
            avl_tree[point] = idx
        
        p = p.next[2]

    return avl_tree


def preprocessing_new(head_node):
    # Assuming head_node is the head of a circular doubly linked list of DLNodes
    # and the first two and the last node are sentinels

    # Create an AVL tree with a custom comparator for the y-coordinate
    avl_tree = AvlTree()
    
    def find_le(tree, point):
        le_node = None
        for node_point in tree:
            if node_point <= point:
                if le_node is None or node_point > le_node:
                    le_node = node_point
        return le_node

    # Start from the node next to the head sentinel
    p = head_node.next[2]

    # Continue until we reach the head sentinel again (full circle)
    while p != head_node and p.next[2] != head_node:
        point = tuple(p.x)
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
                p.closest[1] = le_idx

        # The point is not dominated, insert it into the tree
        if p.ndomr == 0:
            avl_tree[point] = p  # Here we insert the node itself instead of the index

        # Move to the next node in the list
        p = p.next[2]

    return avl_tree




