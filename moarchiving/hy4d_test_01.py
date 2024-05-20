from hv_plus import setup_cdllist, hv4dplusR

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

d = 4
n = 10
new_ref = [11, 11, 41, 46]
head = setup_cdllist(new_points, n, d, new_ref)
print("Hyperovlume in 4d:", hv4dplusR(head))  


