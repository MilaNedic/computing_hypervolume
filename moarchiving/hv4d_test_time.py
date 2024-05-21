import time
from hv_plus import hv4dplusR, setup_cdllist, free_cdllist
import random
import numpy as np

"Function that generates a list of lists, each list represent a four dimensional point"
def generate_4d_points(n):
    dimension_ranges = [(0, 1), (0, 1), (0, 1), (0, 1)]  # Example ranges for each dimension
    # Generates a list of 4-dimensional points  where each point is a list of 4 coordinates
    points = []
    for _ in range(n):
        point = [random.uniform(min_dim, max_dim) for min_dim, max_dim in dimension_ranges]
        points.append(point)
    return points    

"Function that computes the time needed for setting up the circular doubly linked list as well as computing the hypervolume"
def hv4d_time(n):
    points = generate_4d_points(n)
    ref_point = [1, 1, 1, 1]
    points_np =  np.array([np.array(x) for x in points])
    points_list = points_np.flatten()
    head =  setup_cdllist(points_list, n, 4, ref_point)
    tic = time.perf_counter()
    hv4d = hv4dplusR(head)
    toc = time.perf_counter()
    t = toc - tic
    free_cdllist(head)
    #print("Hypervolume in 4D for", n, "points is:", hv4d)
    #print(f"Setting up cdllist and computing the hypervolume was executed in {t:0.9f} seconds \n")
    return t, hv4d

"Function that computes the average time for the hyperovlume computation in 4d"
def average_time(n, m):
    # n is the number of points
    # m is the number of repetitions
    # return the mean time needed for computation of hypervolume in 4d with m repetitions
    times = []
    for _ in range(m):
        t, _ = hv4d_time(n)
        times.append(t)
    avg = sum(times)/m
    return avg

m = 10
times = []
n_list = np.linspace(100, 10000, 20).astype(int)
print(n_list)

for n in n_list:
    avg_time = average_time(n, m)
    times.append(avg_time)

import matplotlib.pyplot as plt

plt.plot(n_list, times, 'o-')
plt.title("Average time for computing the hypervolume in 4-D")
plt.xlabel("Number of points")
plt.ylabel("Average time [s]")
plt.xscale('log')
plt.yscale('log')
plt.show()
