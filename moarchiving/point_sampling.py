import math
import random
import numpy as np


def next_gaussian_double():
    factor = 2.0
    while True:
        result = random.gauss(0, 1)
        if result < -factor:
            continue
        if result > factor:
            continue
        if result >= 0:
            result = result / (2 * factor)
        else:
            result = (2 * factor + result) / (2 * factor)
        return result


def spherical_front(distance, num_points, normalized=True):
    vectors = []

    if normalized:
        v1 = np.array([0, 0, distance])
        v2 = np.array([0, distance, 0])
        v3 = np.array([distance, 0, 0])
        vectors = [v1, v2, v3]

    while len(vectors) < num_points:
        x, y, z = 1, 1, 1

        while (math.sqrt(x * x + y * y + z * z) > 1) or (x < 0.5 and y < 0.5 and z < 0.5):
            x = next_gaussian_double()
            y = next_gaussian_double()
            z = next_gaussian_double()

        r1 = math.sqrt(x * x + y * y + z * z)
        alpha = math.acos(z / r1)
        beta = math.atan2(y, x)

        vect = [distance * math.sin(alpha) * math.cos(beta),
                distance * math.sin(alpha) * math.sin(beta),
                distance * math.cos(alpha)]
        vectors.append(vect)

    return np.array(vectors)


def linear_front(distance, num_points, normalized):
    vectors = []

    if normalized:
        v1 = np.array([0, 0, distance])
        v2 = np.array([0, distance, 0])
        v3 = np.array([distance, 0, 0])
        vectors = [v1, v2, v3]
    while len(vectors) < num_points:
        array = [0.0]
        for _ in range(2):
            array.append(distance * random.random())
        array.append(distance)
        array.sort()

        x = array[1] - array[0]
        y = array[2] - array[1]
        z = array[3] - array[2]

        v = [x, y, z]
        vectors.append(np.array(v))

    vectors = np.array([1, 1, 1]) - vectors
    return vectors
