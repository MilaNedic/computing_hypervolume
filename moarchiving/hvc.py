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
def lexicographic_less_3d(a, b):
    return a[0] < b[0] or (a[0] == b[0] and (a[1] < b[1] or (a[1] == b[1] and a[2] <= b[2])))

# for 4D points
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
    def __init__(self, d):
        self.x = [0.0] * d  # Point coordinates
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

# ---------------- test1 -------------------------
#if __name__ == "__main__":
#    # Example usage for init_sentinels
#    list_head = Dlnode(4)  # Assuming 4 dimensions
#    reference_point = [1.0, 2.0, 3.0, 4.0]  # Example reference point
#    sentinel_head = init_sentinels(list_head, reference_point, 4)
#    print("Sentinel nodes initialized.")
#
#    # Example usage for clear_point
#    point_to_clear = Dlnode(4)  # Assuming 4 dimensions
#    clear_point(list_head, point_to_clear)
#    print("Point cleared.")
#
#    # Example usage for point_to_struct
#    new_point = Dlnode(4)  # Assuming 4 dimensions
#    point_values = [2.0, 3.0, 4.0, 5.0]  # Example point values
#    point_to_struct(list_head, new_point, point_values)
#    print("New point initialized with values:", new_point.x)

# ------------------------ test2 -----------------------------
if __name__ == "__main__":
    # Example usage for add_to_history and remove_from_history
    list_head = Dlnode(3)  # Assuming 3 dimensions
    list_head.next[0] = list_head
    list_head.prev[0] = list_head
    point1 = Dlnode(3)
    point2 = Dlnode(3)
    point3 = Dlnode(3)

    # Add points to history
    add_to_history(list_head, point1)
    add_to_history(list_head, point2)
    add_to_history(list_head, point3)

    # Print the order of points in the history
    current_node = list_head.next[0]
    print("Points in history after addition:")
    while current_node != list_head:
        print("Point coordinates:", current_node.x)
        current_node = current_node.next[0]

    # Remove point2 from history
    remove_from_history(point2)

    # Print the order of points in the history after removal
    current_node = list_head.next[0]
    print("\nPoints in history after removal of point2:")
    while current_node != list_head:
        print("Point coordinates:", current_node.x)
        current_node = current_node.next[0]









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





