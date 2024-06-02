from hv_plus import setup_cdllist, hv3dplus, free_cdllist
from hv_plus import preprocessing


data_points = [
    13, 3, 15,
    7, 15, 2,
    1, 17, 16,
    12, 9, 1,
    4, 5, 15
]
ref_point = [20, 20, 20]
n_points = int(len(data_points)/3)
dimension = 3

# Set up the circular doubly linked list
head = setup_cdllist(data_points, n_points, dimension, ref_point)

from hv_plus import print_cdllist
print_cdllist(head, 2)
print("--------------------------------------------------------------\n")

preprocessing(head, 3)

# Print results
current = head.next[2].next[2]  # Start from the first real node
print("Closest nodes after preprocessing")
while current != head.prev[2]:
    print(f"Node: {current.x}, \nClosest[0]: {current.closest[0].x if current.closest[0] else 'None'}, \nClosest[1]: {current.closest[1].x if current.closest[1] else 'None'}, \n")
    current = current.next[2]
print("--------------------------------------------------------------\n")
hv3d = hv3dplus(head)
print("Hypervolume in 3d:", hv3d)

free_cdllist(head)
