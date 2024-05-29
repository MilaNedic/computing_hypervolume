import numpy as np
from hv_plus import DLNode, setup_cdllist, hv3dplus
from sortedcontainers import SortedList
from hv_plus import preprocessing


data_points = [
    3, 4, 18, 
    1, 10, 16, 
    5, 2, 20, 
    8, 1, 19,
    4, 5, 19
]
ref_point = [20, 20, 20]
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

