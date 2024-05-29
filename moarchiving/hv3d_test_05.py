from hv_plus import setup_cdllist, hv3dplus
from hv_plus import preprocessing

# non-dominated
data_points = [
1, 7, 2,
2, 6, 5,
3, 5, 6,
4, 4, 5,
5, 3, 7,
6, 2, 8,
7, 1, 9
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
