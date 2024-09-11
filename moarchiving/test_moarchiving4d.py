from moarchiving3d import MOArchive3d
from moarchiving4d import MOArchive4d
from moarchiving_utils import DLNode
from moarchiving2d import BiobjectiveNondominatedSortedList as MOArchive2D
from hv_plus import calc_hypervolume_4D
from point_sampling import get_non_dominated_points

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
    def test_hypervolume_easy(self):
        # easy :)
        points = [[0, 1, 2, 3], [1, 2, 3, 0], [2, 3, 0, 1], [3, 0, 1, 2]]
        moa = MOArchive4d(points, reference_point=[4, 4, 4, 4], infos=["A", "B", "C", "D"])
        self.assertEqual(71, moa.hypervolume)


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

    def test_add(self):
        """ test if the add_points function works correctly for 4D points"""
        ref_point = [6, 6, 6, 6]
        start_points = [[1, 2, 5, 4], [2, 3, 5, 1], [3, 5, 1, 4]]
        moa = MOArchive4d(start_points, ref_point, infos=["A", "B", "C"])

        moa.print_cdllist()
        moa.print_cxcy()

        # add point that is not dominated and does not dominate any other point
        u1 = [3, 3, 3, 3]
        moa.add(u1, "D")
        self.assertSetEqual(list_to_set(start_points + [u1]), list_to_set(moa.points_list))

        moa.print_cdllist()
        moa.print_cxcy()

        # add point that is dominated by another point in the archive
        u2 = [4, 5, 2, 4]
        moa.add(u2, "E")
        self.assertSetEqual(list_to_set(start_points + [u1]), list_to_set(moa.points_list))

        moa.print_cdllist()
        moa.print_cxcy()

        # add point that dominates another point in the archive
        u3 = [2, 3, 1, 4]
        moa.add(u3, "F")
        self.assertSetEqual(list_to_set(start_points[:2] + [u1, u3]), list_to_set(moa.points_list))

    def test_hypervolume_after_add(self, n_points=1000, n_tests=10):
        ref_point = [1, 1, 1, 1]

        pop_size = 100
        n_gen = 4
        points = get_non_dominated_points(pop_size * n_gen, n_dim=4)
        points = points.tolist()

        for gen in range(1, n_gen + 1):
            print(f"gen: {gen}")
            moa_true = MOArchive4d(points[:(gen * pop_size)], ref_point)
            true_hv = moa_true.hypervolume

            moa_add = MOArchive4d([], ref_point)
            for i in range(gen * pop_size):
                moa_add.add(points[i])

            self.assertAlmostEqual(moa_add.hypervolume, true_hv, places=6)

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

    def test_distance_to_pareto_front_compare_2d(self):
        # first make a pseudo 4D pareto front and compare it to 2D pareto front
        n_points = 100
        n_test_points = 100
        # set random seed
        np.random.seed(0)
        points = np.hstack([np.random.rand(n_points, 2), np.zeros((n_points, 2))])

        moa4d = MOArchive4d(points, reference_point=[1, 1, 1, 1])
        moa2d = MOArchive2D(points[:, :2], reference_point=[1, 1])
        moa4d_no_ref = MOArchive4d(points)

        permutations = [[0, 1, 2, 3], [1, 2, 0, 3], [2, 0, 1, 3], [3, 2, 1, 0], [2, 3, 0, 1]]
        for indices in permutations:
            perm_points = points[:, [indices]].reshape(-1, 4)
            moa4d_perm = MOArchive4d(perm_points, reference_point=[1, 1, 1, 1])

            new_points = np.hstack([np.random.rand(n_test_points, 2), np.ones((n_test_points, 2))])
            for point in new_points:
                d2 = moa2d.distance_to_pareto_front(point[:2].tolist())
                d4 = moa4d.distance_to_pareto_front(point.tolist())
                d4_no_ref = moa4d_no_ref.distance_to_pareto_front(point.tolist())
                d4_perm = moa4d_perm.distance_to_pareto_front(point[indices].tolist())
                self.assertAlmostEqual(d2, d4, places=8)
                self.assertAlmostEqual(d4, d4_no_ref, places=8)
                self.assertAlmostEqual(d4, d4_perm, places=8)

    def test_distance_to_pareto_front_compare_3d(self):
        # first make a pseudo 4D pareto front and compare it to 3D pareto front
        n_points = 100
        n_test_points = 10
        # set random seed
        np.random.seed(0)
        points = np.hstack([np.random.rand(n_points, 3), np.zeros((n_points, 1))])

        moa4d = MOArchive4d(points, reference_point=[1, 1, 1, 1])
        moa3d = MOArchive3d(points[:, :3], reference_point=[1, 1, 1])
        moa4d_no_ref = MOArchive4d(points)

        permutations = [[0, 1, 2, 3], [1, 2, 3, 0], [2, 0, 1, 3], [3, 2, 1, 0], [2, 3, 0, 1]]
        for indices in permutations:
            perm_points = points[:, [indices]].reshape(-1, 4)
            moa4d_perm = MOArchive4d(perm_points, reference_point=[1, 1, 1, 1])

            new_points = np.hstack([np.random.rand(n_test_points, 3), np.ones((n_test_points, 1))])
            for point in new_points:
                d3 = moa3d.distance_to_pareto_front(point[:3].tolist())
                d4 = moa4d.distance_to_pareto_front(point.tolist())
                d4_no_ref = moa4d_no_ref.distance_to_pareto_front(point.tolist())
                d4_perm = moa4d_perm.distance_to_pareto_front(point[indices].tolist())
                self.assertAlmostEqual(d3, d4, places=8)
                self.assertAlmostEqual(d4, d4_no_ref, places=8)
                self.assertAlmostEqual(d4, d4_perm, places=8)

    def test_remove(self, n_points=100, n_points_remove=50):
        points = [[1, 2, 3, 4], [2, 3, 4, 1], [3, 4, 1, 2]]
        moa_remove = MOArchive4d(points, reference_point=[6, 6, 6, 6])
        moa_remove.remove([1, 2, 3, 4])
        self.assertEqual(len(moa_remove.points_list), 2)
        self.assertSetEqual(list_to_set(moa_remove.points_list), list_to_set(points[1:]))
        self.assertEqual(moa_remove.hypervolume,
                         MOArchive4d(points[1:], reference_point=[6, 6, 6, 6]).hypervolume)

        points = get_non_dominated_points(n_points, n_dim=4)

        remove_idx = np.random.choice(range(n_points), n_points_remove, replace=False)
        keep_idx = [i for i in range(n_points) if i not in remove_idx]

        moa_true = MOArchive4d(points[keep_idx, :], reference_point=[1, 1, 1, 1])
        moa_remove = MOArchive4d(points, reference_point=[1, 1, 1, 1])
        for i in remove_idx:
            moa_remove.remove(points[i].tolist())
        moa_add = MOArchive4d([], reference_point=[1, 1, 1, 1])
        for i in keep_idx:
            moa_add.add(points[i].tolist())

        # assert that the points are the same in all archives and the hypervolume is the same
        self.assertEqual(len(moa_add.points_list), len(moa_true.points_list))
        self.assertEqual(len(moa_remove.points_list), len(moa_true.points_list))

        self.assertSetEqual(list_to_set(moa_remove.points_list), list_to_set(moa_true.points_list))
        self.assertSetEqual(list_to_set(moa_add.points_list), list_to_set(moa_true.points_list))

        self.assertEqual(moa_remove.hypervolume, moa_true.hypervolume)
        self.assertEqual(moa_add.hypervolume, moa_true.hypervolume)

        moa = MOArchive4d([[1, 2, 3, 4], [2, 3, 4, 1], [3, 4, 1, 2]],
                          reference_point=[6, 6, 6, 6])
        moa.add([1, 1, 1, 1])
        moa.remove([1, 1, 1, 1])
        self.assertEqual(len(moa.points_list), 0)

    def _test_contributing_hypervolume(self):
        pass

    def _test_hypervolume_improvement(self):
        pass


if __name__ == '__main__':
    unittest.main()
