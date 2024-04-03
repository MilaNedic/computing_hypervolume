import bisect


class DLNode:
    def __init__(self):
        self.x = [0.0, 0.0, 0.0, 0.0]  # The data vector
        self.closest = [None, None]  # closest[0] == cx, closest[1] == cy
        self.cnext = [None, None]  # current next

        # keeps the points sorted according to coordinates 2,3, and 4
        # (in the case of 2 and 3, only the points swept by 4 are kept)
        self.next = [None, None, None, None]

        # keeps the points sorted according to coordinates 2 and 3 (except the sentinel 3)
        self.prev = [None, None, None, None]

        self.ndomr = 0  # number of dominators


def compare_tree_asc_y(node1, node2):
    # Assuming the DLNode class includes an attribute x which is a list of coordinates
    return node1.x[1] - node2.x[1]

def preprocessing(list, d):
    sorted_nodes = []
    p = list.next[d-1]  # Start with the first node after the head sentinel
    stop = list.prev[d-1]  # Stop at the tail sentinel

    while p != stop:
        # Find the position where the node should be inserted
        idx = bisect.bisect_left(sorted_nodes, p, key=lambda node: node.x[1])

        # Insert the node into the sorted list
        sorted_nodes.insert(idx, p)

        # Update closest nodes if needed
        if idx > 0:
            p.closest[0] = sorted_nodes[idx - 1].x  # Previous node in sorted order
        if idx < len(sorted_nodes) - 1:
            p.closest[1] = sorted_nodes[idx + 1].x  # Next node in sorted order

        p = p.next[d-1]

# Example usage:
# Assuming 'list' is the head of your circular doubly-linked list of DLNode instances

# Call preprocessing on your list
dimension = 3  # Replace with the correct dimension you are using
preprocessing(list, dimension)

# Print the list to check if preprocessing worked
current = list.next[dimension-1]
while current != list:
    print(f"Node: {current.x}, Closest lower y: {current.closest[0]}, Closest higher y: {current.closest[1]}")
    current = current.next[dimension-1]