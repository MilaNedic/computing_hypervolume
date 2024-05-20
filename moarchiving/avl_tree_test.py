from avltree import AvlTree
from hv_plus import setup_cdllist, cdllist_to_list, print_cdllist


# points from the example case
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

ref_p = [0.0, 0.0, 0.0]
avl_tree: AvlTree[tuple, str] = AvlTree[tuple, str]({tuple(ref_p): "reference_point"})

# Call setup_cdllist function - this seorts the node in ascending z coordinate
head_node = setup_cdllist(points, 10, 3, ref_p)
print_cdllist(head_node, d-1)
print("\n")
        
nodes_list = cdllist_to_list(head_node, d-1) # list of dlnodes which we feed into preprocessing, after that we can call hv3dplus

for node in nodes_list[1:-1]: # first and last dlnode indicate the start and end of the list and are not needed in the sorting process
    idx = nodes_list.index(node)
    point = node.x
    avl_tree[tuple(point)] = str(idx) # keys must be immutable and have a less-than comparison, to we turn a list into a tuple

del avl_tree[tuple(ref_p)] # delete the reference point


print("Minimum element in the AVL tree")
print(avl_tree.minimum()) # min in the first corodinate
print("Maximum element in the AVL tree")
print(avl_tree.maximum()) # max in the first coordinate

print("\n")
from hv_plus import preprocessing
preprocessing(nodes_list)
for node in nodes_list:
    print("closest[0]", node.closest[0])
    print("closest[1]:", node.closest[1])
print("List of nodes in the AVL tree after preprocessing")
print(list(preprocessing(nodes_list)))
print("\n")

