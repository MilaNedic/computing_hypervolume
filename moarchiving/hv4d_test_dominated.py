from hv_plus import setup_cdllist, hv4dplusR

new_points = [
1, 10, 20, 30,
2, 9, 25, 29,
3, 8, 30, 28,
4, 7, 35, 27,
5, 6, 40, 26,
50, 50, 50, 50,  # this point is now dominated by others, the results is corect
7, 4, 22, 34,
8, 5, 28, 35,
9, 2, 16, 40,
10, 1, 15, 45
]
new_d = 4
new_n = 10

new_ref = [51, 51, 51, 51]

new_head = setup_cdllist(new_points, new_n, new_d, new_ref)
print("Hypervolume in 4D:", hv4dplusR(new_head), "\n")