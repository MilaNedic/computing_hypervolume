import time
from hv_plus import hv3dplus, setup_cdllist, free_cdllist, preprocessing
import random
import numpy as np
import matplotlib.pyplot as plt

# Cache to store the read points to avoid reading the same file multiple times
points_cache = {}

def read_3d_points(n):
    if n in points_cache:
        return points_cache[n]
    else:
        filename = f"points_3d_{n}.txt"
        data_points = []
        with open(filename, 'r') as file:
            for line in file:
                # Split each line into components, convert to integers, and extend the list
                point = list(map(float, line.strip().split()))
                data_points.extend(point)
        points_cache[n] = data_points
        return data_points

def hv3d_time(n):
    points = read_3d_points(n)
    ref_point = [1, 1, 1]
    tic = time.perf_counter()
    head = setup_cdllist(points, n, 3, ref_point)
    preprocessing(head, 3)
    hv3d = hv3dplus(head)
    toc = time.perf_counter()
    t = toc - tic
    free_cdllist(head)
    return t, hv3d

def average_time(n, m):
    times = []
    for _ in range(m):
        t, _ = hv3d_time(n)
        times.append(t)
    avg = sum(times) / m
    return avg

m = 10
times = []
n_list = np.linspace(10000, 100000, 10).astype(int)
print(n_list)

for n in n_list:
    avg_time = average_time(n, m)
    times.append(avg_time)

plt.plot(n_list, times, 'o-')
plt.title("Average time for setting up cdllist, preprocessing and computing the hypervolume in 3-D")
plt.xlabel("Number of points")
plt.ylabel("Average time [s]")
plt.xscale('log')
plt.yscale('log')
plt.show()
