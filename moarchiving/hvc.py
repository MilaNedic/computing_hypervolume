""" 
    This file contains functions needed for the moarchiving class. 
    It is a transcription of the original hvc class, which is written in c.
    
"""
# --------------------------- auxiliary functions ------------------------

" max and min functions are already defined in python "

def minimum(a, b):
    return a if a < b else b

def maximum(a, b):
    return a if a > b else b

def join(p1, p2):
    return [max(p1[0], p2[0]), max(p1[1], p2[1])]

# for 3D points    
def lexicographic_less(a, b):
    return a[0] < b[0] or (a[0] == b[0] and (a[1] < b[1] or (a[1] == b[1] and a[2] <= b[2])))

## for 4D points
def lexicographic_less_4d(a, b):
    return a[0] < b[0] or (a[0] == b[0] and (a[1] < b[1] or (a[1] == b[1] and (a[2] < b[2] or (a[2] == b[2] and a[3] <= b[3])))))

# -------------------------- class definition ------------------------------------- 
#class Dlnode:
#    def __init__(self, x, d): # d is a parameter, specifying the dimensionality of the problem
#        self.x = x if x else [0.0] * d  # Point coordinates
#        self.closest = [None, None]  # Closest points
#        self.area = 0
#        self.volume = 0
#        self.hvolume = 0  # Hypervolume
#        self.lastSlicez = 0
#        self.ndomr = 0  # Number of points that dominate this one
#        self.domr = None  # Dominator
#        # Next and previous pointers for different dimensions
#        self.next = [None] * (d + 1)
#        self.prev = [None] * (d + 1)
#        self.cnext = [None, None]  # Next in chain for different dimensions
#        self.head = [None, None]  # Head in list for different dimensions
        
class Dlnode:
    def __init__(self, x, d):
        self.x = x if x else [0.0] * d  # Point coordinates
        self.closest = [None, None]  # Closest points
        self.area = 0
        self.volume = 0
        self.hvolume = 0  # Hypervolume
        self.lastSlicez = 0
        self.ndomr = 0  # Number of points that dominate this one
        self.domr = None  # Dominator
        # Next and previous pointers for different dimensions
        self.next = [None] * (d + 1)
        self.prev = [None] * (d + 1)
        self.cnext = [None, None]  # Next in chain for different dimensions
        self.head = [None, None]  # Head in list for different dimensions
        self.id = 0  # Identifier



# ------------------------------ data structure functions ------------------------------------

def add_to_history(list_head, new_node):
    new_node.next[0] = list_head.next[0]
    new_node.prev[0] = list_head
    
    list_head.next[0] = new_node
    new_node.next[0].prev[0] = new_node

def remove_from_history(old_node):
    old_node.prev[0].next[0] = old_node.next[0]
    old_node.next[0].prev[0] = old_node.prev[0]
    
def init_sentinels(list_head, ref, d):
    s1 = list_head
    s2 = Dlnode(d)
    s3 = Dlnode(d)
    
    s1.x[0] = -float('inf')
    s1.x[1] = ref[1]
    s1.x[2] = -float('inf')
    s1.x[3:] = [-float('inf')] * (d - 3)
    s1.closest[0] = s2
    s1.closest[1] = s1
    
    s1.area = 0
    s1.volume = 0
    s1.head[0] = s1
    s1.head[1] = s1
    
    s1.next[2] = s2
    s1.next[3:] = [s2] * (d - 2)
    
    s1.cnext[0] = None
    
    s1.prev[2] = s3
    s1.prev[3:] = [s3] * (d - 2)
    s1.ndomr = 0
    s1.domr = None
    s1.id = -1
    
    s2.x[0] = ref[0]
    s2.x[1] = -float('inf')
    s2.x[2:] = [-float('inf')] * (d - 2)
    s2.closest[0] = s2
    s2.closest[1] = s1
    s2.area = 0
    s2.volume = 0
    s2.head[0] = s2
    s2.head[1] = s2
    
    s2.next[2] = s3
    s2.next[3:] = [s3] * (d - 2)
    s2.cnext[1] = None
    s2.cnext[0] = None
    s2.prev[2] = s1
    s2.prev[3:] = [s1] * (d - 2)
    s2.ndomr = 0
    s2.domr = None
    s2.id = -2
    
    s3.x[:2] = [-float('inf')] * 2
    s3.x[2] = ref[2]
    s3.x[3:] = ref[3:]
    s3.closest[0] = s2
    s3.closest[1] = s1
    s3.area = 0
    s3.volume = 0
    s3.head[0] = s3
    s3.head[1] = s3
    
    s3.next[2] = s1
    s3.next[3] = None
    s3.cnext[1] = None
    s3.cnext[0] = None
    s3.prev[2] = s2
    s3.prev[3:] = [s2] * (d - 2)
    s3.ndomr = 0
    s3.domr = None
    s3.id = -3
    
    return s1

def clear_point(list_head, p):
    p.closest[1] = list_head
    p.closest[0] = list_head.next[2]
    p.cnext[1] = list_head
    p.cnext[0] = list_head.next[2]
    p.head[0] = p.cnext[0]
    p.head[1] = p.cnext[1]
    p.area = 0
    p.volume = 0
    p.hvolume = 0
    p.lastSlicez = p.x[2]
    p.ndomr = 0
    p.domr = None

def point_to_struct(list_head, p, v):
    p.x[:len(v)] = v
    clear_point(list_head, p)
    return p


# ------------------------ test (working correctly) ---------------------------------

## Example usage for add_to_history and remove_from_history
#list_head = Dlnode(None, 3)  # Assuming 3 dimensions
#list_head.next[0] = list_head
#list_head.prev[0] = list_head
#point1 = Dlnode(None, 3)
#point2 = Dlnode(None, 3)
#point3 = Dlnode(None, 3)
#
## Add points to history
#add_to_history(list_head, point1)
#add_to_history(list_head, point2)
#add_to_history(list_head, point3)
#
## Print the order of points in the history
#current_node = list_head.next[0]
#print("Points in history after addition:")
#while current_node != list_head:
#    print("Point coordinates:", current_node.x)
#    current_node = current_node.next[0]
#    
## Remove point2 from history
#remove_from_history(point2)
#
## Print the order of points in the history after removal
#current_node = list_head.next[0]
#print("\nPoints in history after removal of point2:")
#while current_node != list_head:
#    print("Point coordinates:", current_node.x)
#    current_node = current_node.next[0]
#        
#
## Example usage for point_to_struct - initialize a 3D point
#list_head = Dlnode(None,3) # Initialize list_head of appropriate dimensions 
#new_point = Dlnode(None,3)  # Assuming 3 dimensions
#point_values = [2.0, 7.5, 5.0]  # Example point values
#point_to_struct(list_head, new_point, point_values)
#print("New point initialized with values:", new_point.x)





# --------------------------- update data structures -----------------------------------

def add_to_z(new):
    if new.prev[2] is not None:
        new.next[2] = new.prev[2].next[2] if new.prev[2].next[2] is not None else None  # in case new->next[2] was removed for being dominated
    else:
        new.next[2] = None
        
    if new.next[2] is not None:
        new.next[2].prev[2] = new
    if new.prev[2] is not None:
        new.prev[2].next[2] = new

def remove_from_z(old):
    if old.prev[2] is not None and old.prev[2].next[2] is not None:
        old.prev[2].next[2] = old.next[2] if old.next[2] is not None else None
    if old.next[2] is not None and old.next[2].prev[2] is not None:
        old.next[2].prev[2] = old.prev[2] if old.prev[2] is not None else None


def setup_z_and_closest(list_head, new):
    closest1 = list_head if list_head is not None else None
    closest0 = list_head.next[2] if list_head is not None and list_head.next[2] is not None else None

    q = list_head.next[2].next[2] if list_head is not None and list_head.next[2] is not None and list_head.next[2].next[2] is not None else None
    newx = new.x if new is not None else None
    
    while q is not None and lexicographic_less(q.x, newx):
        if q.x[0] <= newx[0] and q.x[1] <= newx[1]:
            new.ndomr += 1
            new.domr = q
        elif q.x[1] < newx[1] and (q.x[0] < closest0.x[0] or (q.x[0] == closest0.x[0] and q.x[1] < closest0.x[1])):
            closest0 = q
        elif q.x[0] < newx[0] and (q.x[1] < closest1.x[1] or (q.x[1] == closest1.x[1] and q.x[0] < closest1.x[0])):
            closest1 = q
            
        q = q.next[2] if q is not None else None
        
    new.closest[0] = new.cnext[0] = closest0
    new.closest[1] = new.cnext[1] = closest1

    new.prev[2] = q.prev[2] if q is not None else None
    new.next[2] = q if q is not None else None

def add_to_data_structure(list_head, new, determine_insertion_points):
    if determine_insertion_points:
        setup_z_and_closest(list_head, new)
    add_to_z(new)
    
    p = new.next[2]
    stop = list_head.prev[2]
    ndom = 0
    all_delimiters_visited = 0
    while p != stop and all_delimiters_visited < 2:
        if p.x[0] <= new.x[0] and p.x[1] <= new.x[1] and (p.x[0] < new.x[0] or p.x[1] < new.x[1]):
            all_delimiters_visited += 1
        else:
            if all_delimiters_visited == 0 or p.ndomr > 0:
                if new.x[0] <= p.x[0]:
                    if new.x[1] <= p.x[1]:
                        p.ndomr += 1
                        p.domr = new
                        ndom += 1
                    elif new.x[0] < p.x[0] and (new.x[1] < p.closest[1].x[1] or (new.x[1] == p.closest[1].x[1] and (new.x[0] < p.closest[1].x[0] or (new.x[0] == p.closest[1].x[0] and new.x[2] < p.closest[1].x[2])))):
                        p.closest[1] = new
                elif new.x[1] < p.x[1] and (new.x[0] < p.closest[0].x[0] or (new.x[0] == p.closest[0].x[0] and (new.x[1] < p.closest[0].x[1] or (new.x[1] == p.closest[0].x[1] and new.x[2] < p.closest[0].x[2])))):
                    p.closest[0] = new

                if p.ndomr > 1:
                    remove_from_z(p)
        p = p.next[2]
    
    return ndom


# ------------------------------------------ test (working) -----------------------------

# Creating a list head
list_head = Dlnode([0.0, 0.0, 0.0], 3)  # Assuming 3 dimensions
list_head.next[0] = list_head
list_head.prev[0] = list_head

# Creating a new node
new_node = Dlnode([1, 2, 3], 3)  # Example coordinates

# Example usage of add_to_z
add_to_z(new_node)
print("Node added to z.")

add_to_data_structure(list_head, new_node, determine_insertion_points=True)
print("Node added to data structure.")

# Example usage of remove_from_z
# For this example, let's assume we have a node to remove called `node_to_remove`
node_to_remove = Dlnode([1, 2, 3], 3)
remove_from_z(node_to_remove)
print("Node removed from z.")

# Define the number of nodes
num_nodes = 5

# Create an empty list to hold the nodes
list_of_nodes = []

# Create nodes and append them to the list
for i in range(num_nodes):
    node = Dlnode([i, i, i], 3)  # Assuming 3 dimensions, with coordinates [i, i, i]
    list_of_nodes.append(node)

# Print the list of nodes
print("List of Nodes:")
for node in list_of_nodes:
    print(node)

# Example usage of setup_z_and_closest
# For this example, let's assume we have a list of nodes called `list_of_nodes`
for node in list_of_nodes:
    setup_z_and_closest(list_head, node)
print("Z and closest setup completed.")


# -------------------------------- sort -----------------------------------

# compare two points in 3D with coordinates (x1, y1, z1) and (x2, y2, z2)
def compare_points_3d(p1, p2):
    for i in range(3):
        c1 = p1[i] # current coordinate of the first point
        c2 = p2[i] # current coordnate of the second point
        if c1 < c2:
            return -1 # p1 comes before p2
        elif c2 < c1:
            return 1 # p2 comes before p1
    return 0 # p1 and p2 are equal
        
        
# compare two points in 4D with coordinates (x1, y1, z1, w1) and (x2, y2, z2, w2)
def compare_points_4d(p1, p2):
    for i in range(4):
        c1 = p1[i] # current coordinate of the first point
        c2 = p2[i] # current coordnate of the second point
        if c1 < c2:
            return -1
        elif c2 < c1:
            return 1
    return 0


def compare_tree_asc_y(p1, p2):
    y1 = p1[1]
    y2 = p2[1]

    if y1 < y2:
        return -1
    elif y1 > y2:
        return 1
    else:
        return 0





