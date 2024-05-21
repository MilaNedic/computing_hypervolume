import random
import time
from hv_plus import hv4dplusR, setup_cdllist, free_cdllist
import numpy as np


def generate_4d_points(n):
    points = [[random.randint(1, 10), random.randint(1, 10), random.randint(1, 10), random.randint(1, 10)] for _ in range(n)]
    print(points) 
    return points


"Function that computes the time needed for setting up the circular doubly linked list as well as computing the hypervolume"
def hv4d(n):
    points = generate_4d_points(n)
    ref_point = [11, 11, 11, 11]
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
    return hv4d

print(hv4d(10))

