# -------------------- AVL Tree ---------------
from avltree import AvlTree

# --------------- Auxiliary Functions ---------------------

def lexicographic_less(a, b):
    return a[2] < b[2] or (a[2] == b[2] and (a[1] < b[1] or (a[1] == b[1] and a[0] <= b[0])))

# ------------------- Data Structure ------------------------

class DLNode:
    def __init__(self):
        self.x = [0.0, 0.0, 0.0, 0.0]  # The data vector
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
    # Link the new node into the list, considering its 'next' and 'prev' in dimension 2
    new.next[2] = new.prev[2].next[2]
    new.next[2].prev[2] = new
    new.prev[2].next[2] = new

def remove_from_z(old):
    # Remove the old node from the list by updating 'next' and 'prev' of neighboring nodes in dimension 2
    old.prev[2].next[2] = old.next[2]
    old.next[2].prev[2] = old.prev[2]

# --------- Example ------------------
## Create a simple linked structure with 3 nodes for demonstration
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
