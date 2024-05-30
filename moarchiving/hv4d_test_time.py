import time
from hv_plus import hv4dplusR, setup_cdllist, free_cdllist, hv4dplusU
import random
import numpy as np
import matplotlib.pyplot as plt

# Cache to store the read points to avoid reading the same file multiple times
points_cache = {}

def read_4d_points(n):
    if n in points_cache:
        return points_cache[n]
    else:
        filename = f"points_4d_{n}.txt"
        data_points = []
        with open(filename, 'r') as file:
            for line in file:
                point = list(map(float, line.strip().split()))
                data_points.extend(point)
        points_cache[n] = data_points
        return data_points  

def hv4d_time(n):
    points = read_4d_points(n)
    ref_point = [1, 1, 1, 1]
    tic = time.perf_counter()
    head = setup_cdllist(points, n, 4, ref_point)
    hv4d = hv4dplusU(head)
    toc = time.perf_counter()
    t = toc - tic
    free_cdllist(head)
    return t, hv4d

def average_time(n, m):
    times = []
    for _ in range(m):
        t, _ = hv4d_time(n)
        times.append(t)
    avg = sum(times) / m
    return avg

m = 10
times = []
n_list = np.linspace(100, 10000, 20).astype(int)
print(n_list)

for n in n_list:
    avg_time = average_time(n, m)
    times.append(avg_time)

plt.plot(n_list, times, 'o-')
plt.title("Average time for setting up cdllist and computing the hypervolume in 4-D")
plt.xlabel("Number of points")
plt.ylabel("Average time [s]")
plt.xscale('log')
plt.yscale('log')
plt.show()
