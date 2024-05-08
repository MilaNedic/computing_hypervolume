from hv_plus import DLNode, lexicographic_less, init_sentinels, clear_point, point2struct, add_to_z, remove_from_z, setup_z_and_closest, update_links, compare_points_3d, compare_points_4d, sort_3d, sort_4d, free_cdllist, restart_list_y, compute_area_simple, restart_base_setup_z_and_closest, one_contribution_3d


# -------------------- Example for the DLNode class -------------------
print("Example for setting up the DLNode class")
# Create instances of DLNode
node1 = DLNode([1.0, 2.0, 3.0, 4.0])
node2 = DLNode([5.0, 6.0, 7.0, 8.0])
node3 = DLNode([9.0, 10.0, 11.0, 12.0])


# Link nodes together
node1.next[0] = node2  # Node1's next is Node2
node2.prev[0] = node1  # Node2's prev is Node1

node2.next[0] = node3  # Node2's next is Node3
node3.prev[0] = node2  # Node3's prev is Node2

# Set closest and cnext for demonstration
node1.closest[0] = node2
node2.cnext[0] = node3

# Print some attributes to test
print("Node1 next x:", node1.next[0].x)
print("Node2 prev x:", node2.prev[0].x)
print("Node2 closest[0] x:", node1.closest[0].x)
print("Node3 cnext[0] x:", node2.cnext[0].x) 

print("\n")

# -------------------- Example for the init_sentinels fucntion ------------------------
print("Example for the init_sentinels fucntion")
# Reference point and dimension
ref_point = [1.0, 2.0, 3.0, 4.0]
dimension = 4

# Initialize the sentinel nodes
sentinel = init_sentinels(ref_point, dimension)

# Function to print node details for demonstration
def print_node_details(node, node_name):
    print(f"{node_name} x: {node.x}")
    print(f"{node_name} closest[0] x: {node.closest[0].x if node.closest[0] else 'None'}")
    print(f"{node_name} closest[1] x: {node.closest[1].x if node.closest[1] else 'None'}")
    print(f"{node_name} next[2] x: {node.next[2].x if node.next[2] else 'None'}")
    print(f"{node_name} next[3] x: {node.next[3].x if node.next[3] else 'None'}")
    print(f"{node_name} prev[2] x: {node.prev[2].x if node.prev[2] else 'None'}")
    print(f"{node_name} prev[3] x: {node.prev[3].x if node.prev[3] else 'None'}")
    print("---")
    
# Printing details of the sentinel nodes
print_node_details(sentinel, "Reference point")
print_node_details(sentinel.next[2], "next[2]")
print_node_details(sentinel.prev[2], "prev[2]")
print("\n")

# ---------------------- Example for the clear_point function -------------------
# Initialize the sentinel nodes with a reference point and dimension
print("Example for the clear_point function")
ref_point = [1.0, 2.0, 3.0, 4.0]
dimension = 4
sentinels = init_sentinels(ref_point, dimension)


# Create a new point node p
p = DLNode([5.0, 6.0, 7.0, 8.0]) # Arbitrary values for demonstration
p.closest[0] = p  # Initially point to itself for demonstration
p.closest[1] = p
p.ndomr = 5  # Assume it dominates 5 other nodes for demonstration

# Print the state of node p before clearing
print("Before clearing:")
print("p.closest[0].x:", p.closest[0].x)
print("p.closest[1].x:", p.closest[1].x)
print("p.ndomr:", p.ndomr)

# Use clear_point to reset p
clear_point(sentinels, p)

# Print the state of node p after clearing
print("\nAfter clearing:")
print("p.closest[0].x:", p.closest[0].x if p.closest[0] else "None")
print("p.closest[1].x:", p.closest[1].x if p.closest[1] else "None")
print("p.ndomr:", p.ndomr)

print("\n")

# ----------------- point2struct test ----------------
print("Example for point2struct")
list_node = DLNode()
list_node.next[2] = list_node  # assuming some self-referencing for simplicity
# Initialize a point
point = DLNode()
values = [1.1, 2.2, 3.3, 4.4]
# Convert array to struct
point2struct(list_node, point, values, 4)
# Print the values to check
print("Point values:")
for i in range(4):
    print(f"x[{i}] = {point.x[i]:.2f}")
print("\n")


# --------- Example ------------------
#Create a simple linked structure with 3 nodes for demonstration
print("Example case for add_to_z")
node1 = DLNode([1.0, 1.0, 1.0, 1.0])
node2 = DLNode([2.0, 2.0, 2.0, 2.0 ])
node3 = DLNode([3.0, 3.0, 3.0, 3.0]) # Is used only to set node2.next

# Manually link nodes
node1.next[2] = node2
node2.prev[2] = node1
node2.next[2] = node3
node3.prev[2] = node2

# Create a new node to add
new_node = DLNode([1.5, 1.5, 1.5, 1.5])

# Set up new_node's prev[2] to node1 to insert it between node1 and node2
new_node.prev[2] = node1

# Add new_node to the list
add_to_z(new_node)

# Verify the linkage
print("After adding new_node:")
print("node1 next:", node1.next[2].x)
print("node2 prev:", node2.prev[2].x)
print("new_node next:", new_node.next[2].x)
print("new_node prev:", new_node.prev[2].x)
print("node1 next:", node1.next[2] == new_node)
print("new_node next:", new_node.next[2] == node2)
print("new_node prev:", new_node.prev[2] == node1)


print("Example case for add_to_z and remove_from_z")
# Now remove node2
remove_from_z(node2)
# Verify the linkage after removal
print("\nAfter removing node2:")
print("new_node next:", new_node.next[2].x)
print("node3 prev:", node3.prev[2].x)
print("new_node next:", new_node.next[2] == node3)
print("node3 prev:", node3.prev[2] == new_node)
print("\n")


# ----------------------------  Example usage for setup z and closest -----------------------------------
print("Example case for setup_z_and_closest")
def print_node(label, node):
    if node:
        print(f"{label}: ({node.x[0]}, {node.x[1]}, {node.x[2]}, {node.x[3]})")
    else:
        print(f"{label}: (None)")

# Initialize nodes with specified values
list_node = DLNode([-15, -15, -15, -15])
next_node = DLNode([10, 10, 10, 10])
new_node = DLNode([0, 0, 0, 0])

# Link nodes
list_node.next[2] = next_node
next_node.prev[2] = list_node
next_node.next[2] = None  # End of list

# Print initial setup
print("Before setup:")
print_node("listNode", list_node)
print_node("nextNode", next_node)

# Perform setup
setup_z_and_closest(list_node, new_node)

# Print after setup
print("After setup:")
print_node("newNode", new_node)
print_node("newNode closest[0]", new_node.closest[0])
print_node("newNode closest[1]", new_node.closest[1])
print_node("newNode next[2]", new_node.next[2])
print_node("newNode prev[2]", new_node.prev[2])

print_node("list_node closest[0]", list_node.closest[0])
print_node("list_node closest[1]", list_node.closest[1])
print_node("list_node next[2]", list_node.next[2])
print_node("list_node prev[2]", list_node.prev[2])

print_node("next_node closest[0]", next_node.closest[0])
print_node("next_node closest[1]", next_node.closest[1])
print_node("next_node next[2]", next_node.next[2])
print_node("next_node prev[2]", next_node.prev[2])

print("\n")

print("Example case for update_links")
head = DLNode([5, 5, 5, 5])
new_node = DLNode([1, 1, 1, 1])
node1 = DLNode([2, 2, 2, 2])
node2 = DLNode([3, 3, 3, 3])
node3 = DLNode([4, 4, 4, 4])

# Linking nodes
head.next[2] = node1
node1.prev[2] = head
node1.next[2] = node2
node2.prev[2] = node1
node2.next[2] = node3
node3.prev[2] = node2
node3.next[2] = None  # End of the list
new_node.prev[2] = node3

# Assume node3 is the last before the stop node
head.prev[2] = node3

# Execute update_links and print results
ndom = update_links(head, new_node, head.next[2])
print("Number of dominators updated:", ndom)
print("\n")



print("Example case for compare_points_3d and compare_point_4d")
point1_3d = [1.0, 2.0, 3.0]
point2_3d = [4.0, 5.0, 6.0]
result_3d = compare_points_3d(point1_3d, point2_3d)
print("Result for compare_point3d:", result_3d)
print("\n")

# Example usage for sorting lists of 3D and 4D points:
print('Example for sorting points in 3D and 4D in ascending order of the last coordinate')
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
#Sort the lists
sorted_points_3d = sort_3d(points_3d) # Ascending order of the last coodinate
sorted_points_4d = sort_4d(points_4d) 

print("Sorted 3D points:", sorted_points_3d)
print("Sorted 4D points:", sorted_points_4d)

# example for init sentinels
from hv_plus import init_sentinels_new
# Nontrivial example
ref = [5.0, 10.0, 15.0, 20.0]  # Reference values for the dimensions
d = 4  # Number of dimensions
list_nodes = [DLNode() for _ in range(3)]  # Create 3 nodes


# Example nodes with non-trivial values
# Let's say we have three additional nodes in the list with non-empty coordinates
list_nodes[0].x = [1.0, 2.0, 3.0, 4.0]
list_nodes[1].x = [6.0, 7.0, 8.0, 9.0]
list_nodes[2].x = [11.0, 12.0, 13.0, 14.0]

# Initialize sentinels
sentinel = init_sentinels_new(list_nodes, ref, d)
print(sentinel.x)


# Print coordinates of all nodes
for i, node in enumerate(list_nodes):
    print(f"Node {i+1}: {node.x}")
    
    
# Initialize the sentinel nodes with a reference point and dimension
ref_point = [1.0, 2.0, 3.0, 4.0]
dimension = 4
sentinels = init_sentinels(ref_point, dimension)
print(sentinels.x)

#sentinels = init_sentinels(ref_point, dimension)
#print(sentinels.x)

print("\n")

from hv_plus import setup_cdllist_new, print_cdllist
from random import uniform
print('Example for setup_cdlist and setup_cdlist_new')

# Define a small set of 3D points as flat data
data = [
    [1.0, 2.0, 3.0, 2.0],  # Point 1
    [4.0, 5.0, 6.0, 1.0],  # Point 2
    [7.0, 8.0, 9.0, -1.0]   # Point 3
]

# Set the reference point for initializing sentinels
ref_point = [0.0, 0.0, 0.0, 0.0]

# Define the number of points and dimension
n = 3  # Number of points
d = 4  # Dimension


# Example 4D data
data_4d = [
    1.0, 2.0, 3.0, 1.0,  # Point 1
    4.0, 5.0, 6.0, 0.5,  # Point 2
    7.0, 8.0, 9.0, 0.7,  # Point 3
    2.0, 1.0, 0.5, 0.6   # Point 4
]

ref_4d = [0.0, 0.0, 0.0, 0.0]

# Call setup_cdllist function for 4D data
head_node_4d = setup_cdllist_new(data_4d, 4, 4, 4, ref_4d)

# Let's print out the list to check
current = head_node_4d.next[3]
while current is not None and current != head_node_4d:
    print(current.x)
    current = current.next[3] if current.next[3] != head_node_4d else None
    
print('\n')


# ---------------- Example for compute_area_simple -------------------
print("Example for compute_area_simple")
point0_data = [3.0, 2.0, 2.0, 0.0]
point1_data = [2.0, 3.0, 3.0, 0.0]
p_data = [5.0, 3.0, 3.0, 0.0]
# Create DLNode instances for the points
point0 = DLNode(point0_data)
point1 = DLNode(point1_data)
# Create DLNode instance for p
p = DLNode(p_data)
# Compute area for di = 0
di = 0
area_di_0 = compute_area_simple(p_data, di, point0, point1)
print("Area for di = 0:", area_di_0)
# Compute area for di = 1
di = 1
area_di_1 = compute_area_simple(p_data, di, point0, point1)
print("Area for di = 1:", area_di_1)

print("\n")


# example for restart bas esetup z and closest
print('Example for restart_base_setup_z_and_closest')

# Example setup
list_node = DLNode([-1.0, -1.0, -1.0, -1.0])
node1 = DLNode([0.0, 0.0, 0.0, 0.0])
node2 = DLNode([5.0, 5.0, 5.0, 5.0])


# Link the nodes in the list for z coordinates (third coordinate, index 2)
list_node.next[2] = node1
node1.next[2] = node2
node2.next[2] = None


# New node to be inserted
new_node = DLNode([1.0, 1.0, 1.0, 1.0])

#list_nodes = [node1, node2, node3]
#init_sentinels_new(list_nodes, list_node.x, 4)

# Call the function to setup z and closest
restart_base_setup_z_and_closest(list_node, new_node)

# Check if the new node's closest and prev/next are correctly set
print("New node dominators count:", new_node.ndomr)
print("New node closest[0]:", new_node.closest[0].x)
print("New node closest[1]:", new_node.closest[1].x)
#print(f"New node's closest in x: {new_node.closest[0].x if new_node.closest[0] else None}")
#print(f"New node's closest in y: {new_node.closest[1].x if new_node.closest[1] else None}")
#print(f"New node's previous node in z: {new_node.prev[2].x if new_node.prev[2] else None}")
#print(f"New node's next node in z: {new_node.next[2].x if new_node.next[2] else None}")
print('\n')


from hv_plus import compare_tree_asc_y, hv3dplus

print('Example for hv3dplus - points are the same as in test.inp')
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

ref_p = [1.0, 1.0, 1.0]


# Call setup_cdllist function - this seorts the node in ascending z coordinate
dlnode_cdllist = setup_cdllist_new(points, 10, 10, d, ref_p)
print_cdllist(dlnode_cdllist, d - 1)
print("\n")

from hv_plus import cdllist_preprocessing

cdllist_preprocessing(dlnode_cdllist, d - 1, 12)
hypervolume = hv3dplus(dlnode_cdllist)
print("Hypervolume in 3D:", hypervolume)


points_4d = [
    1.0, 2.0, 3.0, 1.0,
    4.0, 5.0, 6.0, 0.5,
    7.0, 8.0, 9.0, 0.7,
    2.0, 1.0, 0.5, 0.6,
    3.0, 4.0, 5.0, 0.8,
    6.0, 7.0, 8.0, 0.3,
    9.0, 1.0, 2.0, 0.9,
    5.0, 6.0, 7.0, 0.2,
    8.0, 9.0, 1.0, 0.4,
    0.0, 1.0, 2.0, 0.1
]

dim4d = 4

n4d = 10

ref_point_4d = [10.0, 10.0, 10.0, 10.0]

cdllist_4d = setup_cdllist_new(points_4d, n4d, n4d, dim4d, ref_point_4d)

from hv_plus import hv4dplusR

print("\nHypervolume in 4d - hv4dplusR", hv4dplusR(cdllist_4d))


#def hv4dplusU(list_):
#    height = 0
#    volume = 0
#    hv = 0
#    
#    last = list_.prev[3]
#    new = list_.next[3].next[3]
#    
#    while new != last:
#        volume += one_contribution_3d(list_, new)
#        add_to_z(new)
#        update_links(list_, new, new.next[2])
#        
#        height = new.next[3].x[3] - new.x[3]
#        hv += volume * height
#        
#        new = new.next[3]
#        
#    return hv
#
#print("\nHypervolume in 4d - hv4dplusU", hv4dplusU(cdllist_4d))
