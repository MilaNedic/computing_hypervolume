import numpy as np
from hv_plus import DLNode, setup_cdllist, hv3dplus
from hv_plus import preprocessing

# dominated
data_points = [
6.004880,  6.496723,  0.027096,
6.979226,  8.819977,  0.632567,
0.042235,  5.431784,  9.187109,
7.659001,  7.150049,  1.980560,
1.474021,  4.659168,  2.460924,
5.144871,  5.188114,  7.782582,
2.439585,  3.412151,  1.090158,
9.309574,  7.865394,  4.287836,
4.277942,  6.017614,  7.115128,
2.217251,  0.518201,  3.325386
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
