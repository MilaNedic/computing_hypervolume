import random
import numpy as np
from hv_plus import hv4dplusR, setup_cdllist, free_cdllist
import time

points03 = [
10, 100, 200, 300,
20, 90, 250, 290,
30, 80, 300, 280,
40, 70, 350, 270,
50, 60, 400, 260,
60, 50, 180, 350,
70, 40, 220, 340,
80, 30, 280, 350, 
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
8, 3, 28, 35,
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
0.80, 0.30, 2.80, 3.50,
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
0.080, 0.030, 0.280, 0.350,
0.090, 0.020, 0.160, 0.400,
0.100, 0.010, 0.150, 0.450
]


ref04 = [0.11, 0.11, 0.41, 0.46]
head04 = setup_cdllist(points04, 10, 4, ref04)
print("Hypervolume in 4D:", hv4dplusR(head04))
toc = time.perf_counter()
print(f"Setting up cdllist and computing the hypervolume was executed in {toc - tic:0.9f} seconds \n")


"""
Test for hypervolume when we iteratively add dominated points to the list.
We want to ensure that the hypervolume remains unchanged when adding dominated points to the list.
"""

print("----------------------------------------------------------------")
print("-------------------- Hv4d dominance test -----------------------")
print("----------------------------------------------------------------")


points_dom = [
4, 1, 3, 35,
4, 2, 39, 26,
2, 2, 24, 38,
6, 9, 21, 36,
4, 5, 15, 26,
5, 7, 12, 46,
8, 3, 22, 46,
3, 6, 13, 35,
3, 5, 26, 45,
1, 9, 5, 29
#10, 10, 40, 50     
]

ref_dom = [11, 11, 41, 51]

head_dom = setup_cdllist(points_dom, 10, 4, ref_dom)
print("Hypervolume in 4d (non-dominated points):", hv4dplusR(head_dom))
free_cdllist(head_dom)

points_dom_02 = [
4, 1, 3, 35,
4, 2, 39, 26,
2, 2, 24, 38,
6, 9, 21, 36,
4, 5, 15, 26,
5, 7, 12, 46,
8, 3, 22, 46,
10, 10, 40, 50,     
3, 6, 13, 35,
3, 5, 26, 45,
1, 9, 5, 29
]

head_dom_02 = setup_cdllist(points_dom_02, 11, 4, ref_dom)
print("Hypervolume in 4d after adding a dominated point to the list:", hv4dplusR(head_dom_02))
free_cdllist(head_dom_02)


points_dom_03 = [
4, 1, 3, 35,
4, 2, 39, 26,
2, 2, 24, 38,
6, 9, 21, 36,
9, 4, 23, 47,
4, 5, 15, 26,
5, 7, 12, 46,
8, 3, 22, 46,
10, 10, 40, 50,     
3, 6, 13, 35,
3, 5, 26, 45,
1, 9, 5, 29
]

head_dom_03 = setup_cdllist(points_dom_03, 12, 4, ref_dom)
print("Hypervolume in 4d after adding another dominated point to the list:", hv4dplusR(head_dom_03))
free_cdllist(head_dom_03)

points_dom_04 = [
4, 1, 3, 35,
4, 2, 39, 26,
2, 2, 24, 38,
6, 9, 21, 36,
9, 4, 23, 47,
4, 5, 15, 26,
5, 7, 12, 46,
8, 3, 22, 46,
10, 10, 40, 50,     
3, 6, 13, 35,
4, 7, 14, 36,
3, 5, 26, 45,
1, 9, 5, 29
]

head_dom_04 = setup_cdllist(points_dom_04, 13, 4, ref_dom)
print("Hypervolume in 4d after adding another dominated point to the list:", hv4dplusR(head_dom_04))
free_cdllist(head_dom_04)




points_4d = [
    1.0, 2.0, 3.0, 1.0,
    4.0, 5.0, 6.0, 0.5,
    7.0, 8.0, 9.0, 0.7,
    2.0, 1.0, 0.5, 0.6,
    3.0, 4.0, 5.0, 0.8,
    6.0, 7.0, 8.0, 0.3,
    9.0, 1.0, 2.0, 0.9,
    5.0, 6.0, 7.0, 0.2,
    8.0, 9.0, 1.0, 0.4,
    0.0, 1.0, 2.0, 0.1
]

dim4d = 4

n4d = 10

ref_point_4d = [10.0, 10.0, 10.0, 10.0]


cdllist_4d = setup_cdllist(points_4d, n4d, dim4d, ref_point_4d)

from hv_plus import hv4dplusR

print("--------------------------------------------------------")
print("Hypervolume in 4d - hv4dplusR", hv4dplusR(cdllist_4d))
print("--------------------------------------------------------")