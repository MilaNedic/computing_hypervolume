from moarchiving3d import MOArchive3d
from moarchiving4d import MOArchive4d
from moarchiving_utils import DLNode
from moarchiving2d import BiobjectiveNondominatedSortedList as MOArchive2D
from hv_plus import calc_hypervolume_4D
from point_sampling import get_non_dominated_points
import matplotlib.pyplot as plt

import time
import unittest
import numpy as np
import os


def list_to_set(lst):
    return set([tuple(p) for p in lst])


def get_small_test_archive():
    points = [[1, 2, 3, 4], [4, 1, 2, 3], [3, 4, 1, 2], [2, 3, 4, 1]]
    infos = [str(p) for p in points]
    return MOArchive4d(points, [6, 6, 6, 6], infos)


class MyTestCase(unittest.TestCase):
    def test_hypervolume(self):
        # loop over all files in the tests folder that contain "_3d_" in their name
        print(f"{'file name':20} |   new hv   |   old hv   |")

        for f_name in os.listdir('tests'):
            if "_4d_" not in f_name:
                continue
            # read the data points and the reference point from the file

            data_points = np.loadtxt(f"tests/{f_name}", delimiter=' ')
            infos = [str(p) for p in data_points.tolist()]
            ref_point = [1, 1, 1, 1]

            # calculate the hypervolume using the new implementation
            moa = MOArchive4d(data_points, ref_point, infos)
            hv_new = moa.hypervolume

            # calculate the hypervolume using the old implementation
            hv_old = calc_hypervolume_4D(data_points, ref_point)

            # compare the hypervolumes
            print(f"{f_name:20} | {hv_new:.8f} | {hv_old:.8f} |")

            # assert hypervolumes are equal
            self.assertAlmostEqual(hv_new, hv_old, places=8)
            # assert infos are stored correctly
            self.assertEqual([str(p) for p in moa.points_list], moa.infos_list)

    def test_infos_non_dominated(self):
        """ test if the infos are stored correctly - if the points are non dominated,
        the infos should be the same"""
        moa = get_small_test_archive()
        # assert that the infos are stored in the same order as the points
        self.assertEqual([str(p) for p in moa.points_list], moa.infos_list)

    def test_infos_dominated(self):
        """ test if the infos about dominated points are removed """
        points = [[1, 2, 3, 4], [2, 2, 3, 5], [5, 4, 3, 2], [5, 5, 5, 5]]
        infos = [str(p) for p in points]
        moa = MOArchive4d(points, [6, 6, 6, 6], infos)
        moa.print_cdllist()

        non_dominated_points = [[1, 2, 3, 4], [5, 4, 3, 2]]
        self.assertSetEqual(set([str(p) for p in non_dominated_points]), set(moa.infos_list))
        self.assertEqual([str(p) for p in moa.points_list], moa.infos_list)

    def test_in_domain(self):
        """ test if the in_domain function works correctly for 3D points"""
        moa = get_small_test_archive()

        # test if the points are in the domain
        self.assertTrue(moa.in_domain([1, 2, 3, 4]))
        self.assertTrue(moa.in_domain([5.9, 5.9, 5.9, 5.9]))
        self.assertTrue(moa.in_domain([-1, -1, -1, -1]))
        self.assertTrue(moa.in_domain([-1, 1, -1, 1]))
        self.assertTrue(moa.in_domain([0, 0, 0, 0]))
        # test if the point is not in the domain
        self.assertFalse(moa.in_domain([7, 8, 9, 10]))
        self.assertFalse(moa.in_domain([6, 6, 6, 6]))
        self.assertFalse(moa.in_domain([0, 0, 6, 0]))

    def _test_add(self):
        """ test if the add_points function works correctly for 3D points"""
        pass

    def _test_hypervolume_after_add(self, n_points=1000, n_tests=10):
        pass

    def test_dominates(self):
        moa = get_small_test_archive()

        # test that the points that are already in the archive are dominated
        for p in moa.points_list:
            self.assertTrue(moa.dominates(p))

        # test other dominated points
        self.assertTrue(moa.dominates([5, 5, 5, 5]))
        self.assertTrue(moa.dominates([2, 3, 4, 5]))
        self.assertTrue(moa.dominates([4, 5, 2, 3]))

        # test non dominated points
        self.assertFalse(moa.dominates([3, 3, 3, 3]))
        self.assertFalse(moa.dominates([5, 3, 3, 2]))
        self.assertFalse(moa.dominates([0, 5, 5, 5]))

    def test_dominators(self):
        moa = get_small_test_archive()

        # test that the points that are already in the archive are dominated by itself
        for p in moa.points_list:
            self.assertEqual([p], moa.dominators(p))
            self.assertEqual(1, moa.dominators(p, number_only=True))

        # test other dominated points
        pass

    def _test_distance_to_hypervolume_area(self):
        pass

    def _test_kink_points(self):
        pass

    def _test_distance_to_pareto_front_simple(self):
        pass

    def _test_distance_to_pareto_front_compare_2d(self):
        pass

    def _test_copy_MOArchive(self):
        pass

    def _test_remove(self, n_points=100, n_points_remove=50):
        pass

    def _test_contributing_hypervolume(self):
        pass

    def _test_hypervolume_improvement(self):
        pass

    def _test_get_non_dominated_points(self):
        n_points = 1000
        for mode in ['spherical', 'linear']:
            points = get_non_dominated_points(n_points, n_dim=4, mode=mode)
            self.assertEqual(len(points), n_points)
            moa = MOArchive4d(points, reference_point=[1, 1, 1, 1])
            self.assertEqual(len(moa.points_list), n_points)
            self.assertSetEqual(list_to_set(points), list_to_set(moa.points_list))


if __name__ == '__main__':
    unittest.main()
