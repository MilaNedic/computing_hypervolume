from hv_plus import setup_cdllist, hv3dplus
from hv_plus import preprocessing

# dominated
data_points = [
9.403817,  1.778662,  4.082965,
8.463436,  1.600796,  3.674669,
8.291762,  8.205226,  0.608960,
6.633409,  6.564181,  0.487168,
0.963083,  0.183416,  7.999340,
0.674158,  0.128391,  5.599538,
2.172026,  3.374039,  8.194574,
1.303216,  2.024423,  4.916744,
3.901520,  1.690770,  5.906138,
1.950760,  0.845385,  2.953069,
5.904668,  4.741440,  7.578790,
7.317906,  6.585265,  9.919116,
9.298346,  8.356541,  2.172677,
4.074129,  4.080314,  7.410727,
6.981625,  0.808262,  6.051634,
6.205540,  6.933527,  4.042976,
7.731164,  3.289242,  2.452128,
1.556358,  9.403568,  1.130155,
5.966847,  3.201024,  3.140566,
3.502641,  8.342753,  0.426316,
3.311608,  5.539727,  0.517548,
0.654173,  6.631439,  0.057801,
0.151299,  7.702269,  4.702134,
5.748510,  0.821958,  4.325907,
1.091095,  3.481755,  4.616955,
8.975492,  6.157797,  4.126930,
1.420046,  8.641384,  4.352387,
7.112568,  5.936834,  1.599016,
3.111448,  4.196386,  5.308118,
3.933648,  4.066587,  7.455543
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
