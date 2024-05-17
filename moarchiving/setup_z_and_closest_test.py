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

def lexicographic_less(a, b):
    return (a[2] < b[2] or (a[2] == b[2] and (a[1] < b[1] or (a[1] == b[1] and a[0] <= b[0]))))

def setup_z_and_closest(list, new):
    closest1 = list
    closest0 = list.next[2]

    q = list.next[2].next[2]
    newx = new.x

    while q and lexicographic_less(q.x, newx):
        if q.x[0] <= newx[0] and q.x[1] <= newx[1]:
            new.ndomr += 1
        elif q.x[1] < newx[1] and (q.x[0] < closest0.x[0] or (q.x[0] == closest0.x[0] and q.x[1] < closest0.x[1])):
            closest0 = q
        elif q.x[0] < newx[0] and (q.x[1] < closest1.x[1] or (q.x[1] == closest1.x[1] and q.x[0] < closest1.x[0])):
            closest1 = q

        q = q.next[2]

    new.closest[0] = new.cnext[0] = closest0
    new.closest[1] = new.cnext[1] = closest1
    new.prev[2] = q.prev[2] if q else None
    new.next[2] = q

# Initializing nodes
nodes = [DLNode([10 - i, i * 2, (i % 3) * 5, 0]) for i in range(10)]

# Linking nodes manually
for i in range(9):
    nodes[i].next[2] = nodes[i + 1]
    nodes[i + 1].prev[2] = nodes[i]

# Test setup and print
print("Test for setupZandClosest:")
for i in range(1, 9):  # Skip the first and last for meaningful output
    setup_z_and_closest(nodes[0], nodes[i])

# Print results for each node
for i in range(1, 9):
    print(f"Node {i}:")
    if nodes[i].closest[0]:
        print(f"  Closest X: [{nodes[i].closest[0].x[0]}, {nodes[i].closest[0].x[1]}, {nodes[i].closest[0].x[2]}]")
    else:
        print("  Closest X: [None]")

    if nodes[i].closest[1]:
        print(f"  Closest Y: [{nodes[i].closest[1].x[0]}, {nodes[i].closest[1].x[1]}, {nodes[i].closest[1].x[2]}]")
    else:
        print("  Closest Y: [None]")
