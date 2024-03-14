import hvc

print(hvc.compare_points3d([0,0,0],[1,1,1]))
print(hvc.compare_points4d([0,0,0,0],[1,1,1,1]))

print(hvc.compare_points3d([0,0,0],[-1,-1,-1]))
print(hvc.compare_points4d([0,0,0,0],[-1,-1,-1,-1]))

print(hvc.lexicographicLess3d([0,1,2],[1,0,2]))
print(hvc.lexicographicLess4d([0,1,2,3],[1,0,2,3]))
