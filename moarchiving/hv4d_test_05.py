from hv_plus import setup_cdllist, preprocessing, hv4dplusR

points = [
0.0651, 0.0465, 0.0206, 0.1705,
0.1560, 0.0977, 0.0581, 0.1834,
0.3042, 0.1395, 0.1818, 0.2912,
0.3046, 0.1560, 0.1997, 0.3664,
0.3745, 0.2123, 0.2921, 0.4402,
0.4561, 0.5248, 0.4319, 0.5142,
0.5924, 0.7081, 0.6075, 0.5987,
0.6011, 0.7852, 0.6842, 0.8084,
0.6119, 0.9489, 0.7320, 0.8662,
0.8324, 0.9507, 0.9656, 0.9699
]

d = 4
ref = [1, 1, 1, 1]
n = int(len(points)/d)
head = setup_cdllist(points, n, d, ref)
preprocessing(head, d)
print("Hypervolume in 4-D:", hv4dplusR(head))