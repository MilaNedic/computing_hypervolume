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
                point = list(map(float, line.strip().split()))
                data_points.extend(point)
        points_cache[n] = data_points
        return data_points

def hv3d_time(n):
    points = read_3d_points(n)
    ref_point = [1, 1, 1]

    tic_setup = time.perf_counter()
    head = setup_cdllist(points, n, 3, ref_point)
    toc_setup = time.perf_counter()

    tic_preprocessing = time.perf_counter()
    preprocessing(head, 3)
    toc_preprocessing = time.perf_counter()

    tic_hv3d = time.perf_counter()
    hv3d = hv3dplus(head)
    toc_hv3d = time.perf_counter()

    setup_time = toc_setup - tic_setup
    preprocessing_time = toc_preprocessing - tic_preprocessing
    hv_time = toc_hv3d - tic_hv3d
    total_time = setup_time + preprocessing_time + hv_time

    free_cdllist(head)
    return setup_time, preprocessing_time, hv_time, total_time, hv3d

def average_time(n, m):
    setup_times = []
    preprocessing_times = []
    hv_times = []
    total_times = []
    for _ in range(m):
        setup_time, preprocessing_time, hv_time, total_time, _ = hv3d_time(n)
        setup_times.append(setup_time)
        preprocessing_times.append(preprocessing_time)
        hv_times.append(hv_time)
        total_times.append(total_time)

    avg_setup = sum(setup_times) / m
    avg_preprocessing = sum(preprocessing_times) / m
    avg_hv = sum(hv_times) / m
    avg_total = sum(total_times) / m

    return avg_setup, avg_preprocessing, avg_hv, avg_total

m = 10
setup_times = []
preprocessing_times = []
hv_times = []
total_times = []
n_list = np.linspace(10000, 100000, 10).astype(int)

for n in n_list:
    avg_setup, avg_preprocessing, avg_hv, avg_total = average_time(n, m)
    setup_times.append(avg_setup)
    preprocessing_times.append(avg_preprocessing)
    hv_times.append(avg_hv)
    total_times.append(avg_total)

# Change the layout to 2x2 grid
fig, axs = plt.subplots(2, 2, figsize=(10, 10))

# Assign subplots to the grid
axs[0, 0].plot(n_list, setup_times, 'o-', color='blue')
axs[0, 0].set_title("Average time for setup_cdllist")
axs[0, 0].set_xlabel("Number of points")
axs[0, 0].set_ylabel("Average time [s]")
axs[0, 0].set_xscale('log')
axs[0, 0].set_yscale('log')

axs[0, 1].plot(n_list, preprocessing_times, 'o-', color='red')
axs[0, 1].set_title("Average time for preprocessing")
axs[0, 1].set_xlabel("Number of points")
axs[0, 1].set_ylabel("Average time [s]")
axs[0, 1].set_xscale('log')
axs[0, 1].set_yscale('log')

axs[1, 0].plot(n_list, hv_times, 'o-', color='green')
axs[1, 0].set_title("Average time for hv3dplus")
axs[1, 0].set_xlabel("Number of points")
axs[1, 0].set_ylabel("Average time [s]")
axs[1, 0].set_xscale('log')
axs[1, 0].set_yscale('log')

axs[1, 1].plot(n_list, total_times, 'o-', color='purple')
axs[1, 1].set_title("Total Average Time")
axs[1, 1].set_xlabel("Number of points")
axs[1, 1].set_ylabel("Average time [s]")
axs[1, 1].set_xscale('log')
axs[1, 1].set_yscale('log')

plt.tight_layout()  # Adjust layout to prevent overlap
plt.show()
