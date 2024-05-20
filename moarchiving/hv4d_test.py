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






