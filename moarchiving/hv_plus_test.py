from hv_plus import DLNode, lexicographic_less, init_sentinels, clear_point, point2struct, add_to_z, remove_from_z, setup_z_and_closest, update_links, compare_points_3d, compare_points_4d, sort_3d, sort_4d, setup_cdllist, free_cdllist, restart_list_y, compute_area_simple, restart_base_setup_z_and_closest, one_contribution_3d, hv3dplus


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
print_node_details(sentinel, "Sentinel1")
print_node_details(sentinel.next[2], "Sentinel2")
print_node_details(sentinel.prev[2], "Sentinel3")
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
sentinel_start = DLNode([-15, -15, -15]) # Minimum possible values
sentinel_end = DLNode([10, 10, 10]) # Maximum possible values

# Manually link the sentinel nodes
sentinel_start.next[2] = sentinel_end
sentinel_end.prev[2] = sentinel_start


new_node = DLNode()
new_node.x = [0, 0, 0]
setup_z_and_closest(sentinel_start, new_node)

# Output the results
print("sentinel_start's next is new_node:", sentinel_start.next[2] is new_node)
print("new_node's next is sentinel_end:", new_node.next[2] is sentinel_end)
print("sentinel_end's prev is new_node:", sentinel_end.prev[2] is new_node)
print("new_node closest[0]:", new_node.closest[0].x)
print("new_node closest[1]:", new_node.closest[1].x)
print("\n")


new_node2 = DLNode([5.0, 5.0, 5.0, 5.0])

setup_z_and_closest(new_node, new_node2)
print("new_node closest[0]:", new_node.closest[0].x)
print("new_node closest[1]:", new_node.closest[1].x)

print("new_node2 closest[0]:", new_node2.closest[0].x)
print("new_node2 closest[1]:", new_node2.closest[1].x)

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

