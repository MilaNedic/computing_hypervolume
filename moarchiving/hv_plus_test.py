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

# ---------------------- Example for the clear_point function
# Initialize the sentinel nodes with a reference point and dimension
ref_point = [1.0, 2.0, 3.0, 4.0]
dimension = 4
sentinels = init_sentinels(ref_point, dimension)


# Create a new point node p
p = DLNode()
p.x = [5.0, 6.0, 7.0, 8.0]  # Arbitrary values for demonstration
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
p = DLNode([1.0, 1.0, 1.0, 1.0])

# New values to assign to p
new_values = [10.0, 20.0, 30.0, 40.0]

# Update/initialize p with new_values
p_updated = point2struct(sentinels, p, new_values, dimension)

# Print the updated state of p to verify
print("Updated p.x:", p_updated.x)
print("\n")
