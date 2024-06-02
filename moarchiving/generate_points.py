import random
import numpy as np

"""
A script that generates points in 3- and 4-D with a fixed seed for reproducibility.
These test files are used to analyze the time-complexity of algorithms in C and Python.
"""
def generate_3d_points(n, seed=42):
    random.seed(seed)  # Setting the seed for reproducibility
    dimension_ranges = [(0, 1), (0, 1), (0, 1)]  # Example ranges for each dimension
    
    points = []
    filename = f"tests/points_3d_{n}.txt"  # Dynamic filename that includes the number of points and dimensionality

    for _ in range(n):
        point = [random.uniform(min_dim, max_dim) for min_dim, max_dim in dimension_ranges]
        points.append(point)
    
    # Writing points to a file in 'x y z' format
    with open(filename, 'w') as file:
        for point in points:
            file.write(" ".join(map(str, point)) + "\n")

    return points

def generate_4d_points(n, seed=42):
    random.seed(seed)  # Setting the seed for reproducibility
    dimension_ranges = [(0, 1), (0, 1), (0, 1), (0, 1)]  # Example ranges for each dimension
    
    points = []
    filename = f"tests/points_4d_{n}.txt"  # Dynamic filename that includes the number of points
    
    for _ in range(n):
        point = [random.uniform(min_dim, max_dim) for min_dim, max_dim in dimension_ranges]
        points.append(point)
    
    # Writing points to a file in 'x y z w' format
    with open(filename, 'w') as file:
        for point in points:
            file.write(" ".join(map(str, point)) + "\n")

    return points

n_list_3d = np.linspace(10000, 100000, 10).astype(int)
for n in n_list_3d:
    generate_3d_points(n)
    
n_list_4d = np.linspace(100, 10000, 20).astype(int)    
for n in n_list_4d:
    generate_4d_points(n)
    


