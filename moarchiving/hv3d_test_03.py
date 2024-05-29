import numpy as np
from hv_plus import DLNode, setup_cdllist, hv3dplus
from hv_plus import preprocessing

# some points are dominated
data_points = [
6.065302,  9.935803,  0.057723,
5.458772,  8.942222,  0.051951,
9.021428,  8.957610,  9.484568,
7.217142,  7.166088,  7.587655,
9.977956,  5.982049,  5.050338,
6.984569,  4.187434,  3.535236,
2.482368,  4.216830,  2.333960,
6.699873,  4.403164,  5.164936,
2.941581,  1.768941,  8.103145,
7.449828,  0.908397,  7.228283
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
