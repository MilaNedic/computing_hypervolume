from moarchiving import MOArchive
from hv_plus import calc_hypervolume_3D

import unittest
import numpy as np
import os


def list_to_set(lst):
    return set([tuple(p) for p in lst])


class MyTestCase(unittest.TestCase):
    def test_hypervolume_3D(self):
        # loop over all files in the tests folder that contain "_3d_" in their name
        print(f"{'file name':20} |   new hv   |   old hv   |")

        for f_name in os.listdir('tests'):
            if "_3d_" not in f_name:
                continue
            # read the data points and the reference point from the file

            data_points = np.loadtxt(f"tests/{f_name}", delimiter=' ')
            infos = [str(p) for p in data_points.tolist()]
            ref_point = [1, 1, 1]

            # calculate the hypervolume using the new implementation
            moa = MOArchive(data_points, ref_point, infos)
            hv_new = moa.hypervolume

            # calculate the hypervolume using the old implementation
            hv_old = calc_hypervolume_3D(data_points, ref_point)

            # compare the hypervolumes
            print(f"{f_name:20} | {hv_new:.8f} | {hv_old:.8f} |")

            # assert hyper volumes are equal
            self.assertAlmostEqual(hv_new, hv_old, places=8)
            # assert infos are stored correctly
            self.assertEqual([str(p[:3]) for p in moa.points], moa.infos)

    def test_infos_non_dominated_3D(self):
        """ test if the infos are stored correctly - if the points are non dominated,
        the infos should be the same"""
        points = [
            [1, 2, 3],
            [3, 2, 1],
            [2, 3, 1],
            [1, 3, 2]
        ]
        infos = [str(p) for p in points]

        moa = MOArchive(points, [6, 6, 6], infos)
        # assert that the infos are stored in the same order as the points
        self.assertEqual([str(p[:3]) for p in moa.points], moa.infos)
        # assert that all the points in the archive are non dominated and thus have the same info
        self.assertSetEqual(set([str(p) for p in points]), set(moa.infos))

    def test_infos_dominated_3D(self):
        """ test if the infos about dominated points are removed """
        points = [
            [1, 2, 3],
            [3, 2, 1],
            [2, 3, 4],
            [2, 1, 0]
        ]
        infos = ["A", "B", "C", "D"]

        moa = MOArchive(points, [6, 6, 6], infos)
        # assert that only points A and D are stored in the archive
        self.assertSetEqual({"A", "D"}, set(moa.infos))

    def test_in_domain_3D(self):
        """ test if the in_domain function works correctly for 3D points"""
        ref_point = [6, 6, 6]
        moa = MOArchive([[1, 1, 1]], ref_point)

        # test if the points are in the domain
        self.assertTrue(moa.in_domain([1, 2, 3]))
        self.assertTrue(moa.in_domain([5.9, 5.9, 5.9]))
        # test if the point is not in the domain
        self.assertFalse(moa.in_domain([7, 8, 9]))
        self.assertFalse(moa.in_domain([6, 6, 6]))
        self.assertFalse(moa.in_domain([0, 0, 6]))

    def test_in_domain_4D(self):
        """ test if the in_domain function works correctly for 4D points"""
        ref_point = [6, 6, 6, 6]
        moa = MOArchive([[1, 1, 1, 1]], ref_point)

        # test if the points are in the domain
        self.assertTrue(moa.in_domain([1, 2, 3, 4]))
        self.assertTrue(moa.in_domain([5.9, 5.9, 5.9, 5.9]))
        # test if the point is not in the domain
        self.assertFalse(moa.in_domain([7, 8, 9, 10]))
        self.assertFalse(moa.in_domain([6, 6, 6, 6]))
        self.assertFalse(moa.in_domain([0, 0, 0, 6]))

    def test_add_3D(self):
        """ test if the add_points function works correctly for 3D points"""
        ref_point = [6, 6, 6]
        start_points = [[1, 2, 5], [3, 5, 1], [5, 1, 4]]
        moa = MOArchive(start_points, ref_point)

        # add point that is not dominated and does not dominate any other point
        u1 = [2, 3, 3]
        moa.add(u1)
        self.assertSetEqual(list_to_set(start_points + [u1]), list_to_set(moa.points))

        # add point that is dominated by another point in the archive
        u2 = [4, 5, 2]
        moa.add(u2)
        self.assertSetEqual(list_to_set(start_points + [u1]), list_to_set(moa.points))

        # add point that dominates another point in the archive
        u3 = [3, 1, 2]
        moa.add(u3)
        self.assertSetEqual(list_to_set(start_points[:2] + [u1, u3]), list_to_set(moa.points))

    def test_hypervolume_after_add_3D(self, n_points=1000, n_tests=10):
        ref_point = [1, 1, 1]

        for t in range(n_tests):
            np.random.seed(t)
            points = np.round(np.random.rand(n_points, 3), 3).tolist()
            infos = [str(p) for p in range(n_points)]
            moa = MOArchive(points, ref_point, infos=infos)
            true_hv = moa.hypervolume

            moa_add = MOArchive(points[:1], ref_point, infos=infos[:1])
            for i in range(1, n_points):
                moa_add.add(points[i], infos[i])

            self.assertAlmostEqual(moa_add.hypervolume, true_hv, places=6)


if __name__ == '__main__':
    unittest.main()
