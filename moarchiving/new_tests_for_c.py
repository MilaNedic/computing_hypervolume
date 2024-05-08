class DLNode:
    def __init__(self, x):
        self.x = x
        self.closest = [None, None]  # closest in x and y coordinates
        self.cnext = [None, None]  # current next pointers for rebuild
        self.next = [None] * 4  # next pointers for various dimensions
        self.prev = [None] * 4  # previous pointers for various dimensions
        self.ndomr = 0  # number of dominators

def lexicographic_less(a, b):
    return a[2] < b[2] or (a[2] == b[2] and (a[1] < b[1] or (a[1] == b[1] and a[0] <= b[0])))

def restart_listy(list_node):
    list_node.next[2].cnext[1] = list_node
    list_node.cnext[0] = list_node.next[2]

def restart_base_setup_z_and_closest(list_node, new_node):
    p = list_node.next[2].next[2]
    closest1 = list_node
    closest0 = list_node.next[2]

    newx = new_node.x
    
    restart_listy(list_node)
    
    while p and lexicographic_less(p.x, newx):
        p.cnext[0] = p.closest[0]
        p.cnext[1] = p.closest[1]
        
        p.cnext[0].cnext[1] = p
        p.cnext[1].cnext[0] = p
        
        if p.x[0] <= newx[0] and p.x[1] <= newx[1]:
            new_node.ndomr += 1
        elif p.x[1] < newx[1] and (p.x[0] < closest0.x[0] or (p.x[0] == closest0.x[0] and p.x[1] < closest0.x[1])):
            closest0 = p
        elif p.x[0] < newx[0] and (p.x[1] < closest1.x[1] or (p.x[1] == closest1.x[1] and p.x[0] < closest1.x[0])):
            closest1 = p
        
        p = p.next[2]
    
    new_node.closest[0] = closest0
    new_node.closest[1] = closest1
    
    if p:
        new_node.prev[2] = p.prev[2]
        new_node.next[2] = p
        if p.prev[2]:
            p.prev[2].next[2] = new_node
        p.prev[2] = new_node

# Setting up the nodes
list_node = DLNode([-1, -1, -1, -1])
new_node = DLNode([1, 1, 2, 2])
node1 = DLNode([0, 0, 0, 0])
node2 = DLNode([5, 5, 5, 5])

# Linking nodes
list_node.next[2] = node1
node1.next[2] = node2
node2.next[2] = None  # End of the list

# Simulate list setup and new node integration
restart_base_setup_z_and_closest(list_node, new_node)

print("New node dominators count:", new_node.ndomr)
print("New node closest[0]:", (new_node.closest[0].x if new_node.closest[0] else "None"))
print("New node closest[1]:", (new_node.closest[1].x if new_node.closest[1] else "None"))
