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

    # Timing setup_cdllist
    tic_setup = time.perf_counter()
    head = setup_cdllist(points, n, 4, ref_point)
    toc_setup = time.perf_counter()
    setup_time = toc_setup - tic_setup

    # Timing hv4dplusU
    tic_hv = time.perf_counter()
    hv4d = hv4dplusU(head)
    toc_hv = time.perf_counter()
    hv_time = toc_hv - tic_hv

    total_time = setup_time + hv_time

    free_cdllist(head)
    return setup_time, hv_time, total_time, hv4d

def average_time(n, m):
    setup_times = []
    hv_times = []
    total_times = []
    for _ in range(m):
        setup_time, hv_time, total_time, _ = hv4d_time(n)
        setup_times.append(setup_time)
        hv_times.append(hv_time)
        total_times.append(total_time)

    avg_setup = sum(setup_times) / m
    avg_hv = sum(hv_times) / m
    avg_total = sum(total_times) / m

    return avg_setup, avg_hv, avg_total

m = 10
setup_times = []
hv_times = []
total_times = []
n_list = np.linspace(100, 10000, 20).astype(int)

for n in n_list:
    avg_setup, avg_hv, avg_total = average_time(n, m)
    setup_times.append(avg_setup)
    hv_times.append(avg_hv)
    total_times.append(avg_total)

fig, axs = plt.subplots(3, 1, figsize=(7, 10))

axs[0].plot(n_list, setup_times, 'o-', color='blue')
axs[0].set_title("Average time for setup_cdllist")
axs[0].set_xlabel("Number of points")
axs[0].set_ylabel("Average time [s]")
axs[0].set_xscale('log')
axs[0].set_yscale('log')

axs[1].plot(n_list, hv_times, 'o-', color='green')
axs[1].set_title("Average time for hv4dplusU")
axs[1].set_xlabel("Number of points")
axs[1].set_ylabel("Average time [s]")
axs[1].set_xscale('log')
axs[1].set_yscale('log')

axs[2].plot(n_list, total_times, 'o-', color='purple')
axs[2].set_title("Total Average Time")
axs[2].set_xlabel("Number of points")
axs[2].set_ylabel("Average time [s]")
axs[2].set_xscale('log')
axs[2].set_yscale('log')

plt.tight_layout()
plt.show()
