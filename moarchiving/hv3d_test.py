from hv_plus import setup_cdllist_new, hv3dplus, cdllist_preprocessing, print_cdllist

print('Example for hv3dplus - points are the same as in test.inp')
points = [
    0.16, 0.86, 0.47,  
    0.66, 0.37, 0.29,
    0.79, 0.79, 0.04,
    0.28, 0.99, 0.29,
    0.51, 0.37, 0.38,
    0.92, 0.62, 0.07,
    0.16, 0.53, 0.70,
    0.01, 0.98, 0.94,
    0.67, 0.17, 0.54,
    0.79, 0.72, 0.05
]

d = 3

ref_p = [1.0, 1.0, 1.0]


# Call setup_cdllist function - this seorts the node in ascending z coordinate
dlnode_cdllist = setup_cdllist_new(points, 10, 10, d, ref_p)
print_cdllist(dlnode_cdllist, d - 1)
print("\n")

from hv_plus import cdllist_preprocessing

cdllist_preprocessing(dlnode_cdllist, d - 1, 12)

hypervolume = hv3dplus(dlnode_cdllist)
print("Hypervolume in 3D:", hypervolume)