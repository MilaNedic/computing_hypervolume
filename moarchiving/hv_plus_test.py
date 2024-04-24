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
p = DLNode([1.0, 1.0, 1.0, 1.0])

# New values to assign to p
new_values = [10.0, 20.0, 30.0, 40.0]

# Update/initialize p with new_values
p_updated = point2struct(sentinels, p, new_values, dimension)

# Print the updated state of p to verify
print("Updated p.x:", p_updated.x)
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
# Create sentinel nodes to simulate the start and end of the list
sentinel_start = DLNode([-15, -15, -15, -15]) # Minimum possible values
sentinel_end = DLNode([10, 10, 10, 10]) # Maximum possible values

# Manually link the sentinel nodes
sentinel_start.next[2] = sentinel_end
sentinel_end.prev[2] = sentinel_start


new_node = DLNode()
new_node.x = [0, 0, 0, 0]
setup_z_and_closest(sentinel_start, new_node)

# Output the results
print("sentinel_start's next is new_node:", sentinel_start.next[2] is new_node)
print("new_node's next is sentinel_end:", new_node.next[2] is sentinel_end)  
print("sentinel_end's prev is new_node:", sentinel_end.prev[2] is new_node)
print("new_node closest[0]:", new_node.closest[0].x)
print("new_node closest[1]:", new_node.closest[1].x)
print("\n")


#new_node2 = DLNode([5.0, 5.0, 5.0, 5.0])
#
#setup_z_and_closest(new_node, new_node2)
#print("new_node closest[0]:", new_node.closest[0].x)
#print("new_node closest[1]:", new_node.closest[1].x)
#
#print("new_node2 closest[0]:", new_node2.closest[0].x)
#print("new_node2 closest[1]:", new_node2.closest[1].x)

print("\n")

## Reference point to define sentinel boundaries
#ref_point = [1.0, 1.0, 1.0, 1.0]
#
## Dimension we're working with (3 in this case)
#dimension = 4
#
## Initialize the sentinels based on the reference point and dimension
#sentinels = init_sentinels(ref_point, dimension)
#
#print_node_details(sentinels, "s1")
#print_node_details(sentinels.next[2], "s2") 
#print_node_details(sentinels.prev[2], "s3")
#
#
## Step 1: Initial Setup
## Assume 'sentinels' is the initial list with the sentinel nodes already set up
#node1 = DLNode([1, 2, 3, 4])  # Example node
#node2 = DLNode([5, 6, 7, 8])  # Example node
#
## Insert 'node1' into the structure
#setup_z_and_closest(sentinels, node1)
#print("node1 closest[0]:", node1.closest[0].x)
#print("node1 closest[1]:", node1.closest[1].x)
#
## Insert 'node2', expecting it to correctly position itself based on its values
#setup_z_and_closest(sentinels, node2)
#print("node2 closest[0]:", node2.closest[0].x)
#print("node2 closest[1]:", node2.closest[1].x)
#
## Step 2: Insert another new node
#new_node = DLNode([3, 4, 5, 6])  # This node should fit between 'node1' and 'node2' based on its values
#setup_z_and_closest(sentinels, new_node)
#print("new_node closest[0]:", new_node.closest[0].x)
#print("new_node closest[1]:", new_node.closest[1].x)

# The structure now contains the nodes in their correct positions.


# Assuming the `init_sentinels` function is correctly implemented,
# you now have three sentinel nodes (s1, s2, s3) properly set up and linked.

## Initialize start and end nodes
#sentinel_start = DLNode([-float('inf'), -float('inf'), -float('inf')])
#sentinel_end = DLNode([float('inf'), float('inf'), float('inf')])
##sentinel_start.next[2] = sentinel_end
##sentinel_end.prev[2] = sentinel_start
#
## Create some nodes to form a list
#p1 = DLNode([2.0, 2.0, 2.0])
#p2 = DLNode([3.0, 3.0, 3.0])
#p3 = DLNode([4.0, 4.0, 4.0])
#
## Link the nodes
#sentinel_start.next[2] = p1
#p1.prev[2] = sentinel_start
#p1.next[2] = p2
#p2.prev[2] = p1
#p2.next[2] = p3
#p3.prev[2] = p2
#p3.next[2] = sentinel_end
#sentinel_end.prev[2] = p3
#
## Create a new node that will be checked against the existing nodes
#new_node = DLNode()
#new_node.x = [2.5, 2.5, 2.5]
#
## Call update_links
#number_of_dominators = update_links(sentinel_start, new_node, sentinel_start.next[2])
#
## Output the number of dominators found
#print("Number of dominators:", number_of_dominators)
##

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

# Create the sentinel nodes for the list
sentinel_start = DLNode()
sentinel_end = DLNode()
sentinel_start.x = [-float('inf'), -float('inf'), -float('inf'), -float('inf')]
sentinel_end.x = [float('inf'), float('inf'), float('inf'), float('inf')]


# Link the sentinel nodes
sentinel_start.next[2] = sentinel_end  # Assume dimension 2 is y-dimension
sentinel_end.prev[2] = sentinel_start

# Create a few DLNode instances and link them in the list
node1 = DLNode([4.0, 1.0, 1.0])
node2 = DLNode([3.0, 2.0, 2.0])
node3 = DLNode([2.0, 3.0, 3.0])


nodes = [node1, node2, node3]

# Link the nodes into the list
prev_node = sentinel_start
for node in nodes:
    node.next[2] = sentinel_end
    node.prev[2] = prev_node
    prev_node.next[2] = node
    prev_node = node
    
# Close the circular doubly-linked list
sentinel_end.prev[2] = nodes[-1]

# Initialize cnext pointers using restart_list_y function
restart_list_y(sentinel_start)

# Now you can call compute_area_simple with these nodes
# For example, let's compute the area for the first node in the list
p = [5.0, 3.0, 3.0]  # Some point p
q = [0.0, 1.0, 3.0] # Some point q
di = 0  # Dimension to compute the area over
#s = nodes[0]
#u = nodes[1]

area = compute_area_simple(p, di, nodes[0], nodes[1])
print(f"The computed area for p, node1 and node2 is: {area}")

area = compute_area_simple(p, di, nodes[1], nodes[2])
print(f"The computed area for p, node2 and node3 is: {area}")

area = compute_area_simple(p, di, nodes[0], nodes[2])
print(f"The computed area for p, node1 and node3 is: {area}")

print("\n")

area = compute_area_simple(p, di+1, nodes[2], nodes[1])
print(f"The computed area for p, node1 and node2 is: {area}")

area = compute_area_simple(p, di+1, nodes[1], nodes[0])
print(f"The computed area for p, node2 and node3 is: {area}")

area = compute_area_simple(p, di+1, nodes[2], nodes[0])
print(f"The computed area for p, node1 and node3 is: {area}")

print("\n")


# example for restart bas esetup z and closest
print('Example for restart_base_setup_z_and_closest')

# Example setup
list_node = DLNode([0.0, 0.0, 0.0, 0.0])
node1 = DLNode([1.0, 1.0, 1.0, 1.0])
node2 = DLNode([2.0, 2.0, 2.0, 2.0])
node3 = DLNode([3.0, 3.0, 3.0, 3.0])

# Link the nodes in the list for z coordinates (third coordinate, index 2)
list_node.next[2] = node1
node1.prev[2] = list_node
node1.next[2] = node2
node2.prev[2] = node1
node2.next[2] = node3
node3.prev[2] = node2

# Set closest for node1 and node2 (arbitrarily for this example)
node1.closest = [list_node, list_node]
node2.closest = [node1, node1]

# New node to be inserted
new_node = DLNode([2.8, 1.8, 1.8, 1.8])

#list_nodes = [node1, node2, node3]
#init_sentinels_new(list_nodes, list_node.x, 4)

# Call the function to setup z and closest
restart_base_setup_z_and_closest(list_node, new_node)

# Check if the new node's closest and prev/next are correctly set
print(f"New node's closest in x: {new_node.closest[0].x if new_node.closest[0] else None}")
print(f"New node's closest in y: {new_node.closest[1].x if new_node.closest[1] else None}")
print(f"New node's previous node in z: {new_node.prev[2].x if new_node.prev[2] else None}")
print(f"New node's next node in z: {new_node.next[2].x if new_node.next[2] else None}")
print('\n')






## -------- example 1 ----------------

# Create a list and populate it with nodes. This is an example for a 3D case.
# Define a list with sentinel nodes
#ref_point = [1.0 for i in range(4 )]
#head = DLNode()
#head.next[2] = DLNode([-float('inf'), 10.0, -float('inf'), -float('inf')])  # Sentinel
#head.next[2].next[2] = DLNode([ref_point[0], -float('inf'), -float('inf'), -float('inf')])  # Sentinel
#head.next[2].next[2].next[2] = head  # Make it circular
#
## Define a new node with coordinates
#new_node = DLNode([1.0, 1.0, 2.0, 3.0])
#new_node2 = DLNode([5.0, 0.0, 1.0, 1.0])
##Now call the function with the list and the new node.
#
#restart_base_setup_z_and_closest(head, new_node)
#restart_base_setup_z_and_closest(head, new_node2)
#
## Print the results
#print(f"New node's closest[0]: {new_node.closest[0].x if new_node.closest[0] else None}")
#print(f"New node's closest[1]: {new_node.closest[1].x if new_node.closest[1] else None}")
#print(f"New node's ndomr: {new_node.ndomr}")
#
#print("\n")
#
#print(f"New node2's closest[0]: {new_node2.closest[0].x if new_node2.closest[0] else None}")
#print(f"New node2's closest[1]: {new_node2.closest[1].x if new_node2.closest[1] else None}")
#print(f"New node2's ndomr: {new_node2.ndomr}")
#
#print("\n")
#
## ------------------ example 2 ----------------------
#
## Create the sentinel nodes for the list
#ref_point = [10.0, 10.0, 10.0, 10.0]
#sentinel_start = DLNode([-float('inf'), ref_point[1], -float('inf'), -float('inf')])
#sentinel_end = DLNode([ref_point[0], -float('inf'), -float('inf'), -float('inf')])
#
## Link sentinel nodes to form a circular list in the z-dimension
#sentinel_start.next[2] = sentinel_end
#sentinel_end.prev[2] = sentinel_start
#
## Initialize a list with some DLNode objects representing 3D points
## The points are sorted in increasing z order
#points = [
#    [1.0, 1.0, 1.0, 4.0],  
#    [2.0, 2.0, 2.0, 4.0],  
#    [3.0, 3.0, 3.0, 4.0],  
#    [4.0, 4.0, 4.0, 4.0],  
#    [5.0, 5.0, 5.0, 4.0]   
#]
#
## Create the nodes and link them into the list
#current = sentinel_start
#
#for point in points:
#    idx = points.index(point)
#    node = DLNode(point)
#    node.next[2] = sentinel_end
#    node.prev[2] = current
#    current.next[2] = node
#    current = node
#
#
## Close the circular doubly-linked list in the z-dimension
#sentinel_end.prev[2] = current
#
## Define a new node with coordinates that is supposed to be inserted
#new_node = DLNode([6.1, 0.1, 2.1, 4.0]) 
#" the closest node in x coordinate is [2.0, 2.0, 2.0, 4.0] and the closest node in y coordinate is [3.0, 3.0, 3.0, 4.0]"
#
## Call the function to insert the new_node into the list
#restart_base_setup_z_and_closest(sentinel_start, new_node)
#
#
## Function to print the list for debugging purposes
#def print_list(node):
#    while node:
#        print(f"Node: {node.x}, Closest[0]: {node.closest[0].x if node.closest[0] else 'None'}, Closest[1]: {node.closest[1].x if node.closest[1] else 'None'}")
#        node = node.next[2] if node.next[2] != sentinel_start else None
#
#
## Print the list starting from the first sentinel node
#print_list(sentinel_start.next[2])
## Print the details of the new_node
#print(f"New Node: {new_node.x}, Closest[0]: {new_node.closest[0].x if new_node.closest[0] else 'None'}, Closest[1]: {new_node.closest[1].x if new_node.closest[1] else 'None'}, ndomr: {new_node.ndomr}")
#
##print(new_node.closest[0].x == [2.0, 2.0, 2.0, 4.0])
##print(new_node.closest[1].x == [3.0, 3.0, 3.0, 4.0])
#print("\n")
#
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

from hv_plus import cdllist_to_list
from hv_plus import preprocessing
        
from hv_plus import preprocessing_new
avl_tree_new = preprocessing_new(dlnode_cdllist)
print("List of preprocessed nodes")
print(list(avl_tree_new))
#hypervolume = hv3dplus(dlnode_cdllist)






















#nodes_list = cdllist_to_list(dlnode_cdllist, d-1) # list of dlnodes which we feed into preprocessing, after that we can call hv3dplus
#print("List of nodes in nodes list:")
#for node in nodes_list:
#    print(node.x)
#    
#preprocessed_list = list(preprocessing(nodes_list))
#print("List of nodes after preprocessing")
#print(preprocessed_list)
#print("\n")    

#hypervolume = hv3dplus(dlnode_cdllist)
#print("Hypervolume:", hypervolume)

#"Auxiliary function that reverses points in the list so that the z coordinate comes first"
#def reverse_list_z(dlnode_list):
#    points_list = []
#    for dlnode in dlnode_list:
#        point = dlnode.x
#        point.reverse()
#        points_list.append(point)
#    return [DLNode(point) for point in points_list]
#
#print("\n")
#print("List of nodes with reversed order, coordinates  are now (z,y,x)")
#nodes_list_z = reverse_list_z(nodes_list)
#for node in nodes_list_z:
#    print(node.x)
#
#preprocessing(nodes_list_z)
#print("List of nodes after preprocessing")
#print(list(preprocessing(nodes_list_z)))