# -------------------- AVL Tree ---------------
from avltree import AvlTree
from functools import cmp_to_key

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
        self.closest = [None, None]  # closest[0] == cx, closest[1] == cy
        self.cnext = [None, None]  # current next

        # keeps the points sorted according to coordinates 2,3, and 4
        # (in the case of 2 and 3, only the points swept by 4 are kept)
        self.next = [None, None, None, None]

        # keeps the points sorted according to coordinates 2 and 3 (except the sentinel 3)
        self.prev = [None, None, None, None]

        self.ndomr = 0  # number of dominators


# -------------------- Example for the Class DLNode -------------------
## Create instances of DLNode
#node1 = DLNode()
#node2 = DLNode()
#node3 = DLNode()
#
## Set some data vectors for demonstration
#node1.x = [1.0, 2.0, 3.0, 4.0]
#node2.x = [5.0, 6.0, 7.0, 8.0]
#node3.x = [9.0, 10.0, 11.0, 12.0]
#
## Link nodes together
#node1.next[0] = node2  # Node1's next is Node2
#node2.prev[0] = node1  # Node2's prev is Node1
#
#node2.next[0] = node3  # Node2's next is Node3
#node3.prev[0] = node2  # Node3's prev is Node2
#
## Set closest and cnext for demonstration
#node1.closest[0] = node2
#node2.cnext[0] = node3
#
## Print some attributes to test
#print("Node1 next x:", node1.next[0].x)
#print("Node2 prev x:", node2.prev[0].x)
#print("Node2 closest[0] x:", node1.closest[0].x)
#print("Node3 cnext[0] x:", node2.cnext[0].x) 


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

# -------------------- Example for the init_sentinels fucntion ------------------------
## Reference point and dimension
#ref_point = [1.0, 2.0, 3.0, 4.0]
#dimension = 4
#
## Initialize the sentinel nodes
#sentinel1 = init_sentinels(ref_point, dimension)
#
## Function to print node details for demonstration
#def print_node_details(node, node_name):
#    print(f"{node_name} x: {node.x}")
#    print(f"{node_name} closest[0] x: {node.closest[0].x if node.closest[0] else 'None'}")
#    print(f"{node_name} closest[1] x: {node.closest[1].x if node.closest[1] else 'None'}")
#    print(f"{node_name} next[2] x: {node.next[2].x if node.next[2] else 'None'}")
#    print(f"{node_name} next[3] x: {node.next[3].x if node.next[3] else 'None'}")
#    print(f"{node_name} prev[2] x: {node.prev[2].x if node.prev[2] else 'None'}")
#    print(f"{node_name} prev[3] x: {node.prev[3].x if node.prev[3] else 'None'}")
#    print("---")
#    
## Printing details of the sentinel nodes
#print_node_details(sentinel1, "Sentinel1")
#print_node_details(sentinel1.next[2], "Sentinel2")
#print_node_details(sentinel1.prev[2], "Sentinel3")

# ------------

def clear_point(list, p):
    p.closest[1] = list
    p.closest[0] = list.next[2]
    
    # Assuming the comments regarding printfs imply some form of debugging or state checking,
    # the same assignments are made here as above, mirroring the C function's behavior.
    p.cnext[1] = list
    p.cnext[0] = list.next[2]
    
    p.ndomr = 0
    
# ------------------- clear_point example
## Initialize the sentinel nodes with a reference point and dimension
#ref_point = [1.0, 2.0, 3.0, 4.0]
#dimension = 4
#sentinels = init_sentinels(ref_point, dimension)
#
## Create a new point node p
#p = DLNode()
#p.x = [5.0, 6.0, 7.0, 8.0]  # Arbitrary values for demonstration
#p.closest[0] = p  # Initially point to itself for demonstration
#p.closest[1] = p
#p.ndomr = 5  # Assume it dominates 5 other nodes for demonstration
#
## Print the state of node p before clearing
#print("Before clearing:")
#print("p.closest[0].x:", p.closest[0].x)
#print("p.closest[1].x:", p.closest[1].x)
#print("p.ndomr:", p.ndomr)
#
## Use clear_point to reset p
#clear_point(sentinels, p)
#
## Print the state of node p after clearing
#print("\nAfter clearing:")
#print("p.closest[0].x:", p.closest[0].x if p.closest[0] else "None")
#print("p.closest[1].x:", p.closest[1].x if p.closest[1] else "None")
#print("p.ndomr:", p.ndomr)

def point2struct(list, p, v, d):
    # Update the node p with values from v based on dimension d
    for i in range(d):
        p.x[i] = v[i]
    
    # Reset the node's properties
    clear_point(list, p)
    
    return p

# Initialize the sentinel nodes with a reference point and dimension
ref_point = [1.0, 2.0, 3.0, 4.0]
dimension = 3
sentinels = init_sentinels(ref_point, dimension)

# -------- point2struct test ------------------------

## Assume p is a node we wish to update or initialize
#p = DLNode()
#
## New values to assign to p
#new_values = [10.0, 20.0, 30.0, 40.0]
#
## Update/initialize p with new_values
#p_updated = point2struct(sentinels, p, new_values, dimension)
#
## Print the updated state of p to verify
#print("Updated p.x:", p_updated.x)


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

# --------- Example ------------------
# Create a simple linked structure with 3 nodes for demonstration
#node1 = DLNode()
#node2 = DLNode()
#node3 = DLNode()
#
## Manually link nodes
#node1.next[2] = node2
#node2.prev[2] = node1
#node2.next[2] = node3
#node3.prev[2] = node2
#
## Create a new node to add
#new_node = DLNode()
#
## Set up new_node's prev[2] to node1 to insert it between node1 and node2
#new_node.prev[2] = node1
#
## Add new_node to the list
#add_to_z(new_node)
#
## Verify the linkage
#print("After adding new_node:")
#print("node1 next:", node1.next[2] == new_node)
#print("new_node next:", new_node.next[2] == node2)
#print("new_node prev:", new_node.prev[2] == node1)
#
## Now remove node2
#remove_from_z(node2)
#
## Verify the linkage after removal
#print("\nAfter removing node2:")
#print("new_node next:", new_node.next[2] == node3)
#print("node3 prev:", node3.prev[2] == new_node)



def setup_z_and_closest(list, new):
    # Find closest nodes in the dimensions 0 and 1
    closest0 = list  # Closest in dimension 0
    closest1 = list  # Closest in dimension 1

    q = list.next[2]  # Start from the node after sentinel_start in the z dimension

    # Traverse the list to find the correct position for new_node
    while q and lexicographic_less(q.x, new.x):
        # Check dominance in dimensions 0 and 1
        if q.x[0] <= new.x[0] and q.x[1] <= new.x[1]:
            new.ndomr += 1  # Increment dominator count
        elif q.x[1] < new.x[1]:
            # Update closest0 if q is lexicographically less than the current closest0
            closest0 = q
        elif q.x[0] < new.x[0]:
            # Update closest1 if q is lexicographically less than the current closest1
            closest1 = q
        q = q.next[2]

    # Set the closest and cnext pointers
    new.closest[0] = new.cnext[0] = closest0
    new.closest[1] = new.cnext[1] = closest1

    # Insert new_node before q in the z dimension
    new.prev[2] = q.prev[2]
    new.next[2] = q
    q.prev[2].next[2] = new  # Link the previous node's next to new_node
    q.prev[2] = new  # Link q's prev to new_node

    return new  # Return the newly inserted node for verification if needed

# ----------------------------  Example usage -----------------------------------
# Create sentinel nodes to simulate the start and end of the list
#sentinel_start = DLNode()
#sentinel_end = DLNode()
#
## Setting up the sentinel nodes
#sentinel_start.x = [-float('inf'), -float('inf'), -float('inf')]  # Minimum possible values
#sentinel_end.x = [float('inf'), float('inf'), float('inf')]  # Maximum possible values
#
## Manually link the sentinel nodes
#sentinel_start.next[2] = sentinel_end
#sentinel_end.prev[2] = sentinel_start
#
#
#new_node = DLNode()
#new_node.x = [1.0, 2.0, 3.0]
#setup_z_and_closest(sentinel_start, new_node)
#
## Output the results
#print("sentinel_start next is new_node:", sentinel_start.next[2] is new_node)
#print("new_node next is sentinel_end:", new_node.next[2] is sentinel_end)
#print("sentinel_end prev is new_node:", sentinel_end.prev[2] is new_node)
#print("new_node closest[0]:", new_node.closest[0].x)
#print("new_node closest[1]:", new_node.closest[1].x)


# ------------------- Update Links --------------------

def update_links(list, new, p):
    stop = list.prev[2]
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

# ----------------------------- Example usage ------------------------------

# Assume the DLNode class is defined, and nodes are set up similarly as before
#sentinel_start = DLNode()
#sentinel_end = DLNode()
#sentinel_start.x = [-float('inf'), -float('inf'), -float('inf')]
#sentinel_end.x = [float('inf'), float('inf'), float('inf')]
#sentinel_start.next[2] = sentinel_end
#sentinel_end.prev[2] = sentinel_start
#
## Create some nodes to form a list
#p1 = DLNode()
#p1.x = [2.0, 2.0, 2.0]
#p2 = DLNode()
#p2.x = [3.0, 3.0, 3.0]
#
## Link the nodes
#sentinel_start.next[2] = p1
#p1.prev[2] = sentinel_start
#p1.next[2] = p2
#p2.prev[2] = p1
#p2.next[2] = sentinel_end
#sentinel_end.prev[2] = p2
#
## Create a new node that will be checked against the existing nodes
#new_node = DLNode()
#new_node.x = [1.0, 1.0, 1.0]
#
## Call update_links
#number_of_dominators = update_links(sentinel_start, new_node, sentinel_start.next[2])
#
## Output the number of dominators found
#print("Number of dominators:", number_of_dominators)
#

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


# --------- Auxiliary function that compares points in 3d or in 4d and sorts them in ascending order of the last coorinate ---------------

#def key_point3d(point):
#    # Return a tuple that Python can use to sort the points
#    return (point[2], point[1], point[0])
#
#def key_point4d(point):
#    # Return a tuple that Python can use to sort the points
#    return (point[3], point[2], point[1], point[0])

def sort_3d(list):
    #return sorted(list, key=key_point3d)
    return sorted(list, key=cmp_to_key(compare_points_3d))

def sort_4d(list):
    #return sorted(list, key=key_point4d)
    return sorted(list, key=cmp_to_key(compare_points_4d))

# Example usage for sorting lists of 3D and 4D points:
points_3d = [
    [1.0, 3.0, 5.0],
    [2.0, 2.0, 4.0],
    [3.0, 1.0, 3.0],
]

points_4d = [
    [1.0, 3.0, 5.0, 7.0],
    [2.0, 2.0, 4.0, 6.0],
    [3.0, 1.0, 3.0, 5.0],
]

# Sort the lists
#sorted_points_3d = sort_3d(points_3d) # Ascending order of the last coodinate
#sorted_points_4d = sort_4d(points_4d) 
#
#print("Sorted 3D points:", sorted_points_3d)
#print("Sorted 4D points:", sorted_points_4d)

def setup_cdllist(data, naloc, n, d, ref):
    head = init_sentinels(ref, d)
    di = d - 1

    if n > 0:
        # Sort the points based on dimensionality
        data.sort(key=cmp_to_key(compare_points_3d if d == 3 else compare_points_4d))

        # Initialize nodes and update them with the sorted data
        nodes = [DLNode() for _ in range(n)]
        for i, point in enumerate(data):
            nodes[i] = point2struct(head, nodes[i], point, d)

        # Link the nodes into a circular doubly-linked list
        s = head.prev[di]  # Sentinel tail node
        for i in range(n):
            nodes[i].prev[di] = s
            s.next[di] = nodes[i]
            s = nodes[i]
        s.next[di] = head  # Close the loop
        head.prev[di] = nodes[-1]

    return head

def free_cdllist(list):
    # In Python, garbage collection handles memory deallocation
    del list

# Define a small set of 3D points as flat data
#data = [
#    [1.0, 2.0, 3.0],  # Point 1
#    [4.0, 5.0, 6.0],  # Point 2
#    [7.0, 8.0, 9.0]   # Point 3
#]
#
## Set the reference point for initializing sentinels
#ref_point = [0.0, 0.0, 0.0]
#
## Define the number of points and dimension
#n = 3  # Number of points
#d = 3  # Dimension
#
## Call the function to setup the CDLL
#head = setup_cdllist(data, n + 3, n, d, ref_point)
##
## Function to print the circular doubly-linked list
#def print_cdllist(head, di):
#    print("Circular Doubly-Linked List:")
#    current = head.next[di]
#    while current != head:
#        print(current.x)
#        current = current.next[di]
#
## Print the list to check if it's set up correctly
#print_cdllist(head, d - 1)

    
#free_cdllist(head)


# ------------------------------ Preprocessing -----------------------------------

#def compare_tree_asc_y(p1, p2):
#    y1 = p1[1]
#    y2 = p2[1]
#    if y1 < y2:
#        return -1
#    elif y1 > y2:
#        return 1
#    else:
#        return 0
#
#def node_point(node):
#    # Helper function to get the point from an AVL node
#    return node.value
#
#def find_closest(avl_tree, point, compare):
#    closest = None
#    for node in avl_tree.inorder():
#        if not closest or compare(node, point):
#            closest = node
#        else:
#            break
#    return closest
#
#def is_dominated(p1, p2):
#    # Define the domination logic here
#    return p1[0] <= p2[0] and p1[1] <= p2[1] and p1[2] <= p2[2]
#
#def preprocessing(list):
#    avl_tree = AvlTree(compare_tree_asc_y)
#
#    p = list.next[2]  # Start from the node after the head sentinel
#    stop = list.prev[2]  # The sentinel node before the head is the stop node
#    
#    while p != stop:
#        point = tuple(p.x)  # Convert to a tuple, if necessary
#        avl_tree.insert(point)  # Insert the point to the AVL tree
#
#        # Find the closest point after the inserted point
#        closest_next = find_closest(avl_tree, point, lambda node, pt: node[1] >= pt[1])
#        # Find the closest point before the inserted point
#        closest_prev = find_closest(avl_tree, point, lambda node, pt: node[1] <= pt[1])
#        
#        # Assuming we have a function that returns True if the node is dominated by the point
#        if closest_prev and is_dominated(closest_prev, point):
#            p.ndomr += 1  # Increment dominator count
#            avl_tree.remove(closest_prev)  # Remove the dominated point from the AVL tree
#        elif closest_next and is_dominated(point, closest_next):
#            avl_tree.remove(point)  # Remove the newly inserted point if it's dominated by the closest_next
#
#        # Store the closest points
#        p.closest[0] = closest_prev if closest_prev else None
#        p.closest[1] = closest_next if closest_next else None
#
#        p = p.next[2]
#
#    # Clean up the AVL tree
#    #avltree.clear()
#

## Sample data points (list of lists)
#data = [
#    [1.0, 2.0, 3.0],  # Point 1
#    [2.0, 3.0, 1.0],  # Point 2
#    [3.0, 1.0, 2.0],  # Point 3
#]
#
## Reference point and dimension
#ref_point = [0.0, 0.0, 0.0]
#dimension = 3
#
## Initialize the list with sentinels
#head = init_sentinels(ref_point, dimension)
#
## Populate the list with data points
#current = head
#for point in data:
#    new_node = DLNode()
#    point2struct(head, new_node, point, dimension)
#    # Link new_node into the list
#    current.next[dimension - 1] = new_node
#    new_node.prev[dimension - 1] = current
#    current = new_node
#
## Now call the preprocessing function on the list
#preprocessing(head)
#
## Traverse the list and print out the results to check
#current = head.next[dimension - 1]
#while current != head:
#    print(current.x, current.ndomr, current.closest)
#    current = current.next[dimension - 1]






# ------------------------- Hyperovlume Indicator Algorithms ---------------------------------------
def restart_list_y(list):
    list.next[2].cnext[1] = list  # Link the y-dimension sentinel
    list.cnext[0] = list.next[2]  # Link the x-dimension sentinel


def compute_area_simple(p, di, s, u):
    dj = 1 - di
    area = 0
    q = s
    if q and u:  # Check that q and u are not None
        area += (q.x[dj] - p[dj]) * (u.x[di] - p[di])
    
    while u and p[dj] < u.x[dj]:  # Check that u is not None before accessing u.x
        q = u
        u = u.cnext[di]
        if u:  # Check that the next u is not None before trying to calculate the area
            area += (q.x[dj] - p[dj]) * (u.x[di] - q.x[di])
    
    return area

# ----------------------------- example -----------------------------

## Create the sentinel nodes for the list
#sentinel_start = DLNode()
#sentinel_end = DLNode()
#sentinel_start.x = [-float('inf'), -float('inf'), -float('inf'), -float('inf')]
#sentinel_end.x = [float('inf'), float('inf'), float('inf'), float('inf')]
#
#
## Link the sentinel nodes
#sentinel_start.next[2] = sentinel_end  # Assume dimension 2 is y-dimension
#sentinel_end.prev[2] = sentinel_start
#
## Create a few DLNode instances and link them in the list
#node1 = DLNode()
#node2 = DLNode()
#node3 = DLNode()
#
#node1.x = [4.0, 1.0, 1.0]
#node2.x = [3.0, 2.0, 2.0]
#node3.x = [2.0, 3.0, 3.0]
#
#nodes = [node1, node2, node3]
#
## Link the nodes into the list
#prev_node = sentinel_start
#for node in nodes:
#    node.next[2] = sentinel_end
#    node.prev[2] = prev_node
#    prev_node.next[2] = node
#    prev_node = node
#    
## Close the circular doubly-linked list
#sentinel_end.prev[2] = nodes[-1]
#
## Initialize cnext pointers using restart_list_y function
#restart_list_y(sentinel_start)
#
## Now you can call compute_area_simple with these nodes
## For example, let's compute the area for the first node in the list
#p = [5.0, 3.0, 3.0]  # Some point p
#q = [0.0, 1.0, 3.0] # Some point q
#di = 0  # Dimension to compute the area over
##s = nodes[0]
##u = nodes[1]
#
#area = compute_area_simple(p, di, nodes[0], nodes[1])
#print(f"The computed area for p, node1 and node2 is: {area}")
#
#area = compute_area_simple(p, di, nodes[1], nodes[2])
#print(f"The computed area for p, node2 and node3 is: {area}")
#
#area = compute_area_simple(p, di, nodes[0], nodes[2])
#print(f"The computed area for p, node1 and node3 is: {area}")
#
# -----------------------------------


def restart_list_y(list):
    # This function resets the cnext pointers for the y-dimension.
    list.next[2].cnext[1] = list
    list.cnext[0] = list.next[2]

def restart_base_setup_z_and_closest(head, new_node):
    p = head.next[2].next[2]  # Start from the node after the first sentinel.
    closest0 = closest1 = None
    
    while p != head:
        if lexicographic_less(p.x, new_node.x):
            if closest0 is None or (p.x[0] > closest0.x[0] and p.x[0] < new_node.x[0]):
                closest0 = p
            if closest1 is None or (p.x[1] > closest1.x[1] and p.x[1] < new_node.x[1]):
                closest1 = p
            p = p.next[2]
        else:
            break

    # Check to correct closest1 if it points to the same node as closest0 but shouldn't.
    if closest0 == closest1:
        # Try to find a better match for closest1 if it's not accurately reflecting the y dimension.
        q = closest0.next[2] 
        while q != head and not lexicographic_less(new_node.x, q.x):
            if q.x[1] > closest1.x[1] and q.x[1] < new_node.x[1]:
                closest1 = q
            q = q.next[2]

    restart_list_y(head)
    
    # Insert the new node into the list at the identified position.
    new_node.prev[2] = p.prev[2]
    new_node.next[2] = p
    if p.prev[2]:
        p.prev[2].next[2] = new_node
    p.prev[2] = new_node
    
    # Update the new node's closest pointers.
    new_node.closest[0] = closest0
    new_node.closest[1] = closest1
    new_node.cnext[0] = closest0
    new_node.cnext[1] = closest1





## -------- example 1 ----------------
#ref_point = [10.0, 10.0, 10.0, 10.0]
#
## Create a list and populate it with nodes. This is an example for a 3D case.
## Define a list with sentinel nodes
#head = DLNode()
#head.next[2] = DLNode([-float('inf'), ref_point[1], -float('inf'), -float('inf')])  # Sentinel
#head.next[2].next[2] = DLNode([ref_point[0], -float('inf'), -float('inf'), -float('inf')])  # Sentinel
#head.next[2].next[2].next[2] = head  # Make it circular
#
## Define a new node with coordinates
#new_node = DLNode([1.0, 1.0, 2.0, 3.0])
#
##Now call the function with the list and the new node.
#
#restart_base_setup_z_and_closest(head, new_node)
#
## Print the results
#print(f"New node's closest[0]: {new_node.closest[0].x if new_node.closest[0] else None}")
#print(f"New node's closest[1]: {new_node.closest[1].x if new_node.closest[1] else None}")
#print(f"New node's ndomr: {new_node.ndomr}")


#def print_list(head):
#    current = head.next[2]
#    while current != head:
#        print(f"Node: {current.x}, Closest[0]: {current.closest[0].x if current.closest[0] else 'None'}, Closest[1]: {current.closest[1].x if current.closest[1] else 'None'}")
#        current = current.next[2]
#
#print_list(head)

# Assuming the DLNode class, restart_list_y, and lexicographic_less are already defined

# Create the sentinel nodes for the list
ref_point = [10.0, 10.0, 10.0, 10.0]
sentinel_start = DLNode([-float('inf'), ref_point[1], -float('inf'), -float('inf')])
sentinel_end = DLNode([ref_point[0], -float('inf'), -float('inf'), -float('inf')])

# Link sentinel nodes to form a circular list in the z-dimension
sentinel_start.next[2] = sentinel_end
sentinel_end.prev[2] = sentinel_start

# Initialize a list with some DLNode objects representing 3D points
# The points are sorted in increasing z order
points = [
    [1.0, 1.0, 1.0, 4.0],  # Point closer to the origin than the new point
    [2.0, 2.0, 2.0, 4.0],  # Point closer to the origin than the new point
    [3.0, 3.0, 3.0, 4.0],  # Point closer to the origin than the new point
    [4.0, 4.0, 4.0, 4.0],  # Point at the same z as the new point
    [5.0, 5.0, 5.0, 4.0]   # Point further from the origin than the new point
]

# Create the nodes and link them into the list
current = sentinel_start
for point in points:
    node = DLNode(point)
    node.next[2] = sentinel_end
    node.prev[2] = current
    current.next[2] = node
    current = node

# Close the circular doubly-linked list in the z-dimension
sentinel_end.prev[2] = current

# Define a new node with coordinates that is supposed to be inserted
new_node = DLNode([3.5, 3.5, 3.5, 4.0])

# Call the function to insert the new_node into the list
#restart_base_setup_z_and_closest(sentinel_start, new_node)

## Function to print the list for debugging purposes
#def print_list(node):
#    while node:
#        print(f"Node: {node.x}, Closest[0]: {node.closest[0].x if node.closest[0] else 'None'}, Closest[1]: {node.closest[1].x if node.closest[1] else 'None'}")
#        node = node.next[2] if node.next[2] != sentinel_start else None
#
## Print the list starting from the first sentinel node
#print_list(sentinel_start.next[2])

# Print the details of the new_node
#print(f"New Node: {new_node.x}, Closest[0]: {new_node.closest[0].x if new_node.closest[0] else 'None'}, Closest[1]: {new_node.closest[1].x if new_node.closest[1] else 'None'}, ndomr: {new_node.ndomr}")

" this is currently not working correctly, closest[1] is not being updates as it should be"


# ------------------------ one contribution ---------------------

