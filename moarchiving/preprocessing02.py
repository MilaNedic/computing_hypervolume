import numpy as np
from hv_plus import DLNode, setup_cdllist, hv3dplus
from sortedcontainers import SortedList

def preprocessing(head, d):
    di = d - 1
    current = head.next[di]
    stop = head.prev[di]
    
    # SortedList to maintain nodes in order based on y-coordinate, supports custom sorting needs
    avl_tree = SortedList(key=lambda node: (node.x[1], node.x[0]))
    
    # Adding sentinel nodes to handle edge conditions
    avl_tree.add(head)  # head is a left sentinel
    avl_tree.add(head.prev[di])  # right sentinel

    while current != stop:
        avl_tree.add(current)
        index = avl_tree.index(current)
        
        # Determine closest[0]
        x_candidates = [node for node in avl_tree if node.x[0] > current.x[0] and node.x[1] < current.x[1]]
        if x_candidates:
            current.closest[0] = min(x_candidates, key=lambda node: node.x[0])
        else:
            current.closest[0] = head  # Fallback to sentinel if no valid candidate

        # Determine closest[1]
        y_candidates = [node for node in avl_tree if node.x[0] < current.x[0] and node.x[1] > current.x[1]]
        if y_candidates:
            current.closest[1] = min(y_candidates, key=lambda node: node.x[1])
        else:
            current.closest[1] = head.prev[di]  # Fallback to sentinel if no valid candidate

        # Remove dominated nodes
        dominated = [node for node in avl_tree if node != current and all(node.x[i] <= current.x[i] for i in range(3))]
        for node in dominated:
            avl_tree.remove(node)
            node.ndomr = 1

        current = current.next[di]

    avl_tree.clear()  # Clear the AVL tree after processing


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

preprocessing(head, 3)

# Print results
current = head.next[2]  # Start from the first real node
print("Closest nodes after preprocessing")
while current != head:
    print(f"Node: {current.x}, \nClosest[0]: {current.closest[0].x if current.closest[0] else 'None'}, \nClosest[1]: {current.closest[1].x if current.closest[1] else 'None'}, \n")
    current = current.next[2]
print("---------------------------------------------")
print("\n")
hv3d = hv3dplus(head)
print("---------------------------------------------")
print("Hypervolume in 3d:", hv3d)