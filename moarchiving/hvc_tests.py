import hvc

print(hvc.compare_points_3d([0,0,0],[1,1,1]))
print(hvc.compare_points_4d([0,0,0,0],[1,1,1,1]))

print(hvc.compare_points_3d([0,0,0],[-1,-1,-1]))
print(hvc.compare_points_4d([0,0,0,0],[-1,-1,-1,-1]))

# ------------------- auxiliary functions --------------------------
print(hvc.lexicographic_less([0,1,2],[1,0,2]))
print(hvc.lexicographic_less_4d([0,1,2,3],[1,0,2,3]))

# ----------------- data structure functions ------------------------

p1 = hvc.Dlnode([1.0, 2.0, 3.0, 4.0],4)
p2 = hvc.Dlnode([2.0, 3.0, 4.0, 5.0], 4)
print(hvc.join(p1.x, p2.x))
print(hvc.lexicographic_less(p1.x, p2.x))

