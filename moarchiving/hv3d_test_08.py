from hv_plus import setup_cdllist, hv3dplus
from hv_plus import preprocessing

# non-dominated
data_points = [
0.321071,  0.311353,  0.393575,
0.017068,  3.037504,  8.512918,
6.336256,  0.041417,  0.058611,
1.067864,  6.025091,  0.134439,
0.220168,  6.751231,  0.668980,
0.786688,  0.091531,  0.586794,
6.958852,  2.063041,  0.029574,
1.915318,  2.974692,  0.289630,
0.298925,  5.898856,  0.960939,
0.285940,  8.796881,  0.466729,
0.070468,  3.106956,  3.511412,
0.138312,  1.314707,  6.587315,
0.071663,  2.023205,  2.612011,
0.071438,  2.801673,  4.692152,
0.220260,  1.103089,  5.849278,
4.165027,  2.262418,  0.036311,
0.003404,  7.430941,  1.841891,
2.631531,  3.259264,  0.258122,
1.234662,  4.993808,  0.019447,
0.131787,  1.450127,  5.607500,
1.645518,  3.999309,  0.337714,
8.574930,  1.905466,  0.041919,
0.634707,  0.012193,  4.222139,
0.628252,  6.738954,  0.057282,
3.577681,  0.143396,  0.486561,
0.226398,  0.138848,  3.066002,
0.101540,  7.728331,  0.988025,
2.677188,  0.874450,  0.102941,
0.027716,  4.556780,  4.091664,
2.811290,  2.434905,  0.022108
]
ref_point = [10, 10, 10]
n_points = int(len(data_points)/3)
dimension = 3

# Set up the circular doubly linked list
head = setup_cdllist(data_points, n_points, dimension, ref_point)

preprocessing(head, 3)

# Print results
current = head.next[2]  # Start from the first real node
print("Closest nodes after preprocessing")
while current != head:
    print(f"Node: {current.x}, \nClosest[0]: {current.closest[0].x if current.closest[0] else 'None'}, \nClosest[1]: {current.closest[1].x if current.closest[1] else 'None'}, \n")
    current = current.next[2]
print("--------------------------------------------------------------")
print("\n")
hv3d = hv3dplus(head)
print("--------------------------------------------------------------")
print("Hypervolume in 3d:", hv3d)
