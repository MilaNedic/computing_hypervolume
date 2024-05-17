import random
import numpy as np
from hv_plus import hv4dplusR, setup_cdllist_new, free_cdllist

def generate_4d_points(num_points, dimension_ranges):
    """
    Generate a list of 4-dimensional points.

    Parameters:
    - num_points: int, number of points to generate
    - dimension_ranges: list of tuples, where each tuple represents the min and max range of each dimension

    Returns:
    - list of points, where each point is a list of 4 coordinates
    """
    points = []
    for _ in range(num_points):
        point = [random.uniform(min_dim, max_dim) for min_dim, max_dim in dimension_ranges]
        points.append(point)
    return points

# define the ranges for each dimension
dimension_ranges = [(0, 5), (0, 5), (0, 5), (0, 5)]  # Example ranges for each dimension

# generate 4D points
num = 10
points = generate_4d_points(num, dimension_ranges)
points_np =  np.array([np.array(x) for x in points])
points_list = points_np.flatten()
print(points_list)

reference_point = [5.0, 5.0, 5.0, 5.0]

list4d = setup_cdllist_new(points_list, num+2, num, 4, reference_point)
print("Hypervolume in 4D:", hv4dplusR(list4d))

#from hv_plus import hv4dplusU
#print("Hypervolume in 4D using contributions:", hv4dplusU(list4d))

free_cdllist(list4d)
