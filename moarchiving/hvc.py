""" 
    This file contains functions needed for the moarchiving class. 
    It is a transcription of the original hvc class, which is written in c.
    
"""

# --------------------------- auxiliary functions ------------------------

" max and min functions are already defined in python "

def join(p1, p2, p):
    p[0] = max(p1[0], p2[0])
    p[1] = max(p1[1], p2[1])

# for 3D points    
def lexicographicLess3d(a, b):
    return a[0] < b[0] or (a[0] == b[0] and (a[1] < b[1] or (a[1] == b[1] and a[2] <= b[2])))

# for 4D points
def lexicographicLess4d(a, b):
    return a[0] < b[0] or (a[0] == b[0] and (a[1] < b[1] or (a[1] == b[1] and (a[2] < b[2] or (a[2] == b[2] and a[3] <= b[3])))))

# -------------------------------- sort -----------------------------------

# compare two points in 3D with coordinates (x1, y1, z1) and (x2, y2, z2)
def compare_points3d(p1, p2):
    for i in range(3):
        c1 = p1[i] # current coordinate of the first point
        c2 = p2[i] # current coordnate of the second point
        if c1 < c2:
            return -1 # p1 comes before p2
        elif c2 < c1:
            return 1 # p2 comes before p1
    return 0 # p1 and p2 are equal
        
        
# compare two points in 4D with coordinates (x1, y1, z1, w1) and (x2, y2, z2, w2)
def compare_points4d(p1, p2):
    for i in range(4):
        c1 = p1[i] # current coordinate of the first point
        c2 = p2[i] # current coordnate of the second point
        if c1 < c2:
            return -1
        elif c2 < c1:
            return 1
    return 0