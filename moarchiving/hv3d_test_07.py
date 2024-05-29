import numpy as np
from hv_plus import DLNode, setup_cdllist, hv3dplus
from hv_plus import preprocessing

# dominated
data_points = [
5.291889,  8.588316,  9.984524,
0.238965,  9.399079,  8.053162,
0.396902,  1.901583,  5.552046,
6.063271,  0.109464,  9.871435,
9.065136,  3.861212,  3.688411,
8.193973,  1.823771,  2.424667,
9.265428,  6.498143,  0.790420,
3.075910,  9.895914,  2.016922,
4.315672,  0.526313,  3.351503,
8.705762,  0.502652,  6.269091,
0.697691,  5.706485,  0.588124,
6.703927,  3.806580,  1.450084,
4.565323,  4.923696,  0.677224,
7.478404,  0.791868,  0.638779,
1.380453,  4.231505,  3.948941,
3.844427,  0.625012,  6.318325,
0.413018,  0.096848,  6.127442,
6.425128,  2.558673,  3.140683,
0.347096,  7.692177,  3.195892,
6.018013,  4.658135,  1.009114,
3.845528,  1.700132,  3.968348,
3.804777,  0.732877,  2.229619,
2.014079,  8.603544,  0.035317,
8.431301,  1.056632,  0.210223,
3.543033,  3.217917,  1.506271,
6.889910,  0.817670,  1.711961,
2.812172,  1.169356,  0.111365,
6.780142,  0.029508,  8.567704,
1.755735,  4.464093,  1.582761,
1.520709,  4.979668,  1.297218
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
