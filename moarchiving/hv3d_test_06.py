import numpy as np
from hv_plus import DLNode, setup_cdllist, hv3dplus
from hv_plus import preprocessing

# dominated
data_points = [
9.935781,  8.186692,  3.913727,
8.942203,  7.368023,  3.522354,
9.707677,  3.820528,  2.443415,
7.766142,  3.056422,  1.954732,
2.985011,  6.940039,  9.587260,
2.089508,  4.858027,  6.711082,
1.002156,  3.109259,  8.525376,
0.601294,  1.865555,  5.115226,
1.588715,  8.452066,  5.562064,
0.794358,  4.226033,  2.781032,
5.329772,  3.869561,  7.146149,
9.804438,  0.655432,  9.713949,
9.307049,  2.970831,  6.839144,
9.466491,  6.093767,  3.404261,
3.257853,  1.916640,  7.474628,
3.515879,  5.455772,  6.350767,
1.543637,  6.467723,  9.747642,
6.341563,  0.015614,  7.881273,
7.745688,  1.567509,  8.052475,
7.058775,  1.935831,  3.595841
]
ref_point = [10, 10, 10]
n_points = int(len(data_points)/3)
dimension = 3

# Set up the circular doubly linked list
head = setup_cdllist(data_points, n_points, dimension, ref_point)

preprocessing(head, 3)

# Print results
current = head.next[2]  # Start from the first real node
print("Closest nodes after preprocessing")
while current != head:
    print(f"Node: {current.x}, \nClosest[0]: {current.closest[0].x if current.closest[0] else 'None'}, \nClosest[1]: {current.closest[1].x if current.closest[1] else 'None'}, \n")
    current = current.next[2]
print("--------------------------------------------------------------")
print("\n")
hv3d = hv3dplus(head)
print("--------------------------------------------------------------")
print("Hypervolume in 3d:", hv3d)
