class DLNode:
    def __init__(self, x=None):
        if x is None:
            x = [None] * 4
        self.x = x
        self.closest = [None, None]  # Closest in X and Y
        self.cnext = [None, None]  # Current next pointers for rebuild
        self.next = [None] * 4  # Sorted pointers
        self.prev = [None] * 4  # Sorted pointers
        self.ndomr = 0  # Number of dominators

def restart_listy(list):
    list.next[2].cnext[1] = list  # Link sentinels
    list.cnext[0] = list.next[2]  # Assume list.next[2] is a sentinel with smallest values

def lexicographic_less(a, b):
    return (a[2] < b[2] or (a[2] == b[2] and (a[1] < b[1] or (a[1] == b[1] and a[0] <= b[0]))))

def restart_base_setup_z_and_closest(list, new):
    p = list.next[2].next[2]
    closest1 = list
    closest0 = list.next[2]

    newx = new.x

    restart_listy(list)

    while p and lexicographic_less(p.x, newx):
        p.cnext[0] = p.closest[0]
        p.cnext[1] = p.closest[1]

        p.cnext[0].cnext[1] = p
        p.cnext[1].cnext[0] = p

        if p.x[0] <= newx[0] and p.x[1] <= newx[1]:
            new.ndomr += 1
        elif p.x[1] < newx[1] and (p.x[0] < closest0.x[0] or (p.x[0] == closest0.x[0] and p.x[1] < closest0.x[1])):
            closest0 = p
        elif p.x[0] < newx[0] and (p.x[1] < closest1.x[1] or (p.x[1] == closest1.x[1] and p.x[0] < closest1.x[0])):
            closest1 = p

        p = p.next[2]

    new.closest[0] = closest0
    new.closest[1] = closest1
    new.prev[2] = p.prev[2] if p else None
    new.next[2] = p

# Initializing nodes
nodes = [DLNode([i, i*2, i*3, 0]) for i in range(5)]

# Linking nodes manually
for i in range(4):
    nodes[i].next[2] = nodes[i + 1]
    nodes[i + 1].prev[2] = nodes[i]

# Print initial nodes
print("Initial nodes:")
for i, node in enumerate(nodes):
    print(f"Node {i}: {node.x}")

# Assume nodes[0] is the head of the list and nodes[4] is the tail
new_node = DLNode([1.5, 3.5, 5.5, 0])

# Running the function
restart_base_setup_z_and_closest(nodes[0], new_node)

# Output the closest nodes
print("\nNew node closest X:", (new_node.closest[0].x if new_node.closest[0] else None))
print("New node closest Y:", (new_node.closest[1].x if new_node.closest[1] else None))
