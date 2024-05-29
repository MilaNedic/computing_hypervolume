import time
from hv_plus import hv3dplus, setup_cdllist, free_cdllist, preprocessing
import random
import numpy as np

"Function that generates a list of lists, each list represent a three dimensional point"
def generate_3d_points(n):
    dimension_ranges = [(0, 1), (0, 1), (0, 1)]  # Example ranges for each dimension
    # Generates a list of 4-dimensional points  where each point is a list of 3 coordinates
    points = []
    for _ in range(n):
        point = [random.uniform(min_dim, max_dim) for min_dim, max_dim in dimension_ranges]
        points.append(point)
    return points    

"Function that computes the time needed for setting up the circular doubly linked list as well as computing the hypervolume"
def hv3d_time(n):
    points = generate_3d_points(n)
    ref_point = [1, 1, 1]
    points_np =  np.array([np.array(x) for x in points])
    points_list = points_np.flatten()
    head =  setup_cdllist(points_list, n, 3, ref_point)
    preprocessing(head, 3)
    tic = time.perf_counter()
    hv3d = hv3dplus(head)
    toc = time.perf_counter()
    t = toc - tic
    free_cdllist(head)
    return t, hv3d

"Function that computes the average time for the hyperovlume computation in 3d"
def average_time(n, m):
    # n is the number of points
    # m is the number of repetitions
    # return the mean time needed for computation of hypervolume in 3d with m repetitions
    times = []
    for _ in range(m):
        t, _ = hv3d_time(n)
        times.append(t)
    avg = sum(times)/m
    return avg

m = 10
times = []
n_list = np.linspace(10000, 100000, 10).astype(int)
print(n_list)

for n in n_list:
    avg_time = average_time(n, m)
    times.append(avg_time)

import matplotlib.pyplot as plt

plt.plot(n_list, times, 'o-')
plt.title("Average time for computing the hypervolume in 3-D")
plt.xlabel("Number of points")
plt.ylabel("Average time [s]")
plt.xscale('log')
plt.yscale('log')
plt.show()
