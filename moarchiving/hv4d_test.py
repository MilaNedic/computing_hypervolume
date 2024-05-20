import random
import numpy as np
from hv_plus import hv4dplusR, setup_cdllist, free_cdllist
import time

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
dimension_ranges = [(0, 1), (0, 1), (0, 1), (0, 1)]  # Example ranges for each dimension

# generate 4D points
num = 1000
points = generate_4d_points(num, dimension_ranges)
points_np =  np.array([np.array(x) for x in points])
points_list = points_np.flatten()
#print(points_list)

reference_point = [1.0, 1.0, 1.0, 1.0]

tic = time.perf_counter()
list4d = setup_cdllist(points_list, num, 4, reference_point)
print("Hypervolume in 4D:", hv4dplusR(list4d))
toc = time.perf_counter()
print(f"Setting up cdllist and computing the hypervolume was executed in {toc - tic:0.9f} seconds \n")

#from hv_plus import hv4dplusU
#print("Hypervolume in 4D using contributions:", hv4dplusU(list4d))

free_cdllist(list4d)

points03 = [
10, 100, 200, 300,
20, 90, 250, 290,
30, 80, 300, 280,
40, 70, 350, 270,
50, 60, 400, 260,
60, 50, 180, 350,
70, 40, 220, 340,
80, 50, 280, 350, 
90, 20, 160, 400,
100, 10, 150, 450
]

ref03 = [110, 110, 410, 460]
tic = time.perf_counter()
head03 = setup_cdllist(points03, 10, 4, ref03)
print("Hypervolume in 4D:", hv4dplusR(head03))
toc = time.perf_counter()
print(f"Setting up cdllist and computing the hypervolume was executed in {toc - tic:0.9f} seconds \n")

new_points = [
1, 10, 20, 30,
2, 9, 25, 29,
3, 8, 30, 28,
4, 7, 35, 27,
5, 6, 40, 26,
6, 5, 18, 35,
7, 4, 22, 34,
8, 5, 28, 35,
9, 2, 16, 40,
10, 1, 15, 45
]
new_d = 4
new_n = 10

new_ref = [11, 11, 41, 46]

tic = time.perf_counter()
new_head = setup_cdllist(new_points, new_n, new_d, new_ref)
print("Hypervolume in 4D:", hv4dplusR(new_head))
toc = time.perf_counter()
print(f"Setting up cdllist and computing the hypervolume was executed in {toc - tic:0.9f} seconds \n")

points02 = [
0.10, 1.00, 2.00, 3.00,
0.20, 0.90, 2.50, 2.90,
0.30, 0.80, 3.00, 2.80,
0.40, 0.70, 3.50, 2.70,
0.50, 0.60, 4.00, 2.60,
0.60, 0.50, 1.80, 3.50,
0.70, 0.40, 2.20, 3.40,
0.80, 0.50, 2.80, 3.50,
0.90, 0.20, 1.60, 4.00,
1.00, 0.10, 1.50, 4.50
]
d02 = 4
n02 = 10
ref02 = [1.1, 1.1, 4.1, 4.6]
tic = time.perf_counter()
head02 = setup_cdllist(points02, n02, 4, ref02)
print("Hypervolume in 4D:", hv4dplusR(head02))
toc = time.perf_counter()
print(f"Setting up cdllist and computing the hypervolume was executed in {toc - tic:0.9f} seconds \n")

#from fractions import Fraction
#points02_frac = [Fraction(i) for i in points02]
#ref02_frac = [Fraction(i) for i in ref02]
#head02_frac = setup_cdllist(points02_frac, 10, 4, ref02_frac)
#print("Hypervolume in 4D using Fractions:", hv4dplusR(head02_frac).limit_denominator(), "\n")
#toc = time.perf_counter()
#print(f"Setting up cdllist and computing the hypervolume was executed in {toc - tic:0.9f} seconds")


points04 = [
0.010, 0.100, 0.200, 0.300,
0.020, 0.090, 0.250, 0.290,
0.030, 0.080, 0.300, 0.280,
0.040, 0.070, 0.350, 0.270,
0.050, 0.060, 0.400, 0.260,
0.060, 0.050, 0.180, 0.350,
0.070, 0.040, 0.220, 0.340,
0.080, 0.050, 0.280, 0.350,
0.090, 0.020, 0.160, 0.400,
0.100, 0.010, 0.150, 0.450
]


ref04 = [0.11, 0.11, 0.41, 0.46]
head04 = setup_cdllist(points04, 10, 4, ref04)
print("Hypervolume in 4D:", hv4dplusR(head04))
toc = time.perf_counter()
print(f"Setting up cdllist and computing the hypervolume was executed in {toc - tic:0.9f} seconds \n")






