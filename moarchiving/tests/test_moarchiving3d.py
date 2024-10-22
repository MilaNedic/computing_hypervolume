from moarchiving.moarchiving3d import MOArchive3d
from moarchiving.moarchiving_utils import DLNode, my_lexsort
from moarchiving.moarchiving2d import BiobjectiveNondominatedSortedList as MOArchive2D
from moarchiving.tests.point_sampling import (get_non_dominated_points, get_random_points,
                                              get_stacked_points)

import unittest
import itertools
import math


def list_to_set(lst):
    return set([tuple(p) for p in lst])


class MyTestCase(unittest.TestCase):
    def test_hypervolume_easy(self):
        """ test the hypervolume calculation for a simple case """
        points = [[1, 2, 3], [2, 3, 1], [3, 1, 2]]
        moa = MOArchive3d(points, reference_point=[4, 4, 4], infos=["A", "B", "C"])
        self.assertEqual(moa.hypervolume, 13)

    def test_hypervolume(self):
        """ test the hypervolume calculation, by comparing to the result of original
        implementation in C"""
        points = [
            [0.16, 0.86, 0.47],
            [0.66, 0.37, 0.29],
            [0.79, 0.79, 0.04],
            [0.28, 0.99, 0.29],
            [0.51, 0.37, 0.38],
            [0.92, 0.62, 0.07],
            [0.16, 0.53, 0.70],
            [0.01, 0.98, 0.94],
            [0.67, 0.17, 0.54],
            [0.79, 0.72, 0.05]
        ]
        moa = MOArchive3d(points, reference_point=[1, 1, 1])
        self.assertAlmostEqual(moa.hypervolume, 0.318694, places=6)

    def test_infos_non_dominated(self):
        """ test if the infos are stored correctly - if the points are non dominated,
        the infos should be the same"""
        points = [
            [1, 2, 3],
            [3, 2, 1],
            [2, 3, 1],
            [1, 3, 2]
        ]
        infos = [str(p) for p in points]

        moa = MOArchive3d(points, [6, 6, 6], infos)
        # assert that the infos are stored in the same order as the points
        self.assertEqual([str(p[:3]) for p in moa.points], moa.infos)
        # assert that all the points in the archive are non dominated and thus have the same info
        self.assertSetEqual(set([str(p) for p in points]), set(moa.infos))

    def test_infos_dominated(self):
        """ test if the infos about dominated points are removed """
        points = [
            [1, 2, 3],
            [3, 2, 1],
            [2, 3, 4],
            [2, 1, 0]
        ]
        infos = ["A", "B", "C", "D"]

        moa = MOArchive3d(points, [6, 6, 6], infos)
        # assert that only points A and D are stored in the archive
        self.assertSetEqual({"A", "D"}, set(moa.infos))

    def test_in_domain(self):
        """ test if the in_domain function works correctly for 3D points"""
        ref_point = [6, 6, 6]
        moa = MOArchive3d([[1, 1, 1]], ref_point)

        # test if the points are in the domain
        self.assertTrue(moa.in_domain([1, 2, 3]))
        self.assertTrue(moa.in_domain([5.9, 5.9, 5.9]))
        # test if the point is not in the domain
        self.assertFalse(moa.in_domain([7, 8, 9]))
        self.assertFalse(moa.in_domain([6, 6, 6]))
        self.assertFalse(moa.in_domain([0, 0, 6]))

    def test_add(self):
        """ test if the add_points function works correctly for 3D points"""
        ref_point = [6, 6, 6]
        start_points = [[1, 2, 5], [3, 5, 1], [5, 1, 4]]
        moa = MOArchive3d(start_points, ref_point)

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

    def test_hypervolume_after_add(self):
        ref_point = [1, 1, 1]

        pop_size = 100
        n_gen = 10
        points = get_non_dominated_points(pop_size * n_gen)

        for gen in range(1, n_gen + 1):
            moa_true = MOArchive3d(points[:(gen * pop_size)], ref_point)
            true_hv = moa_true.hypervolume

            moa_add = MOArchive3d([], ref_point)
            for i in range(gen * pop_size):
                moa_add.add(points[i])

            moa_add_gen = MOArchive3d([], ref_point)
            for i in range(gen):
                moa_add_gen.add_list(points[(i * pop_size):((i + 1) * pop_size)])

            self.assertAlmostEqual(moa_add.hypervolume, true_hv, places=6)
            self.assertAlmostEqual(moa_add_gen.hypervolume, true_hv, places=6)

    def test_dominates(self):
        ref_point = [6, 6, 6]
        points = [[1, 3, 5], [5, 3, 1], [4, 4, 4]]
        moa = MOArchive3d(points, ref_point)

        # test that the points that are already in the archive are dominated
        for p in points:
            self.assertTrue(moa.dominates(p))

        # test other dominated points
        self.assertTrue(moa.dominates([5, 5, 5]))
        self.assertTrue(moa.dominates([2, 4, 5]))

        # test non dominated points
        self.assertFalse(moa.dominates([3, 3, 3]))
        self.assertFalse(moa.dominates([2, 5, 4]))
        self.assertFalse(moa.dominates([5, 1, 3]))

    def test_dominators(self):
        ref_point = [6, 6, 6]
        points = [[1, 2, 3], [3, 1, 2], [2, 3, 1], [3, 2, 1], [2, 1, 3], [1, 3, 2]]
        moa = MOArchive3d(points, ref_point)

        # test that the points that are already in the archive are dominated by itself
        for p in points:
            self.assertEqual([p], moa.dominators(p))
            self.assertEqual(1, moa.dominators(p, number_only=True))

        # test other dominated points
        self.assertEqual(list_to_set([[1, 2, 3], [2, 3, 1], [2, 1, 3], [1, 3, 2]]),
                         list_to_set(moa.dominators([2, 3, 4])))
        self.assertEqual(4, moa.dominators([2, 3, 4], number_only=True))

        self.assertEqual([], moa.dominators([2, 2, 2]))
        self.assertEqual(0, moa.dominators([2, 2, 2], number_only=True))

        self.assertEqual(list_to_set(points), list_to_set(moa.dominators([3, 3, 3])))
        self.assertEqual(6, moa.dominators([3, 3, 3], number_only=True))

    def test_distance_to_hypervolume_area(self):
        moa = MOArchive3d()
        self.assertEqual(0, moa.distance_to_hypervolume_area([1, 1, 1]))

        moa.reference_point = [2, 2, 2]
        # for points in the hypervolume area, the distance should be 0
        self.assertEqual(0, moa.distance_to_hypervolume_area([0, 0, 0]))
        self.assertEqual(0, moa.distance_to_hypervolume_area([1, 1, 1]))
        self.assertEqual(0, moa.distance_to_hypervolume_area([2, 2, 2]))
        self.assertEqual(0, moa.distance_to_hypervolume_area([0, 1, 2]))

        # for points outside the hypervolume area, the distance should be the Euclidean distance
        # to the hypervolume area
        self.assertEqual(1, moa.distance_to_hypervolume_area([2, 2, 3]))
        self.assertEqual(1, moa.distance_to_hypervolume_area([2, 0, 3]))
        self.assertEqual(10, moa.distance_to_hypervolume_area([0, 0, 12]))

        self.assertAlmostEqual(math.sqrt(2), moa.distance_to_hypervolume_area([0, 3, 3]), places=6)
        self.assertAlmostEqual(math.sqrt(2), moa.distance_to_hypervolume_area([2, 3, 3]), places=6)
        self.assertAlmostEqual(math.sqrt(3), moa.distance_to_hypervolume_area([3, 3, 3]), places=6)
        self.assertAlmostEqual(math.sqrt(75), moa.distance_to_hypervolume_area([7, 7, 7]), places=6)

    def test_distance_to_pareto_front_simple(self):
        points = [[1, 2, 3], [2, 3, 1], [3, 1, 2]]
        moa = MOArchive3d(points, reference_point=[6, 6, 6])

        self.assertEqual(0, moa.distance_to_pareto_front([1, 1, 1]))
        self.assertEqual(3 ** 0.5, moa.distance_to_pareto_front([4, 4, 4]))
        self.assertEqual((1 + 1 + 6 ** 2) ** 0.5, moa.distance_to_pareto_front([7, 7, 7]))
        self.assertEqual(0, moa.distance_to_pareto_front([2, 4, 3]))
        self.assertEqual(0, moa.distance_to_pareto_front([3, 2, 4]))
        self.assertEqual(1, moa.distance_to_pareto_front([3, 3, 4]))

    def test_distance_to_pareto_front_compare_2d(self):
        # first make a pseudo 3D pareto front and compare it to 2D pareto front
        n_points = 100
        n_test_points = 100
        points = get_stacked_points(n_points, ['random', 'random', 0])

        moa3d = MOArchive3d(points, reference_point=[1, 1, 1])
        moa2d = MOArchive2D([[p[0], p[1]] for p in points], reference_point=[1, 1])
        moa3d_no_ref = MOArchive3d(points)

        new_points = get_stacked_points(n_test_points, ['random', 'random', 1])
        for point in new_points:
            d2 = moa2d.distance_to_pareto_front(point[:2])
            d3 = moa3d.distance_to_pareto_front(point)
            d3_no_ref = moa3d_no_ref.distance_to_pareto_front(point)
            self.assertAlmostEqual(d2, d3, places=8)
            self.assertAlmostEqual(d3, d3_no_ref, places=8)

    def test_copy_DLNode(self):
        n1 = DLNode([1, 2, 3, 4], "node 1")
        n2 = DLNode([5, 6, 7, 8], "node 2")
        n1.closest[1] = n2
        n2.closest[0] = n1

        n1_copy = n1.copy()
        n2_copy = n2.copy()
        n2_copy.x = [-1, -2, -3, -4]

        n1.x[0] = 10
        n1.closest[1] = n1
        self.assertEqual(n1_copy.x[0], 1)
        self.assertEqual(n1_copy.closest[1].x[0], 5)
        self.assertEqual(n2.x[0], 5)
        self.assertEqual(n2_copy.x[0], -1)

    def test_copy_MOArchive(self):
        points = [[1, 2, 3], [2, 3, 1], [3, 1, 2]]
        moa = MOArchive3d(points, reference_point=[6, 6, 6])
        moa_copy = moa.copy()

        self.assertEqual(moa.hypervolume, moa_copy.hypervolume)

        moa.add([2, 2, 2])

        self.assertEqual(len(moa.points), 4)
        self.assertEqual(len(moa_copy.points), 3)

        self.assertFalse(moa.hypervolume == moa_copy.hypervolume)

    def test_remove(self, n_points=100, n_points_remove=50):
        points = [[1, 2, 3], [2, 3, 1], [3, 1, 2]]
        moa_remove = MOArchive3d(points, reference_point=[6, 6, 6])
        moa_remove.remove([1, 2, 3])
        self.assertEqual(len(moa_remove.points), 2)
        self.assertSetEqual(list_to_set(moa_remove.points), list_to_set(points[1:]))
        self.assertEqual(moa_remove.hypervolume,
                         MOArchive3d(points[1:], reference_point=[6, 6, 6]).hypervolume)

        points = get_non_dominated_points(n_points)

        remove_idx = list(range(n_points_remove))
        keep_idx = [i for i in range(n_points) if i not in remove_idx]

        moa_true = MOArchive3d([points[i] for i in keep_idx], reference_point=[1, 1, 1])
        moa_remove = MOArchive3d(points, reference_point=[1, 1, 1])
        for i in remove_idx:
            moa_remove.remove(points[i])
        moa_add = MOArchive3d([], reference_point=[1, 1, 1])
        for i in keep_idx:
            moa_add.add(points[i])

        # assert that the points are the same in all archives and the hypervolume is the same
        self.assertEqual(len(moa_add.points), len(moa_true.points))
        self.assertEqual(len(moa_remove.points), len(moa_true.points))

        self.assertSetEqual(list_to_set(moa_remove.points), list_to_set(moa_true.points))
        self.assertSetEqual(list_to_set(moa_add.points), list_to_set(moa_true.points))

        self.assertEqual(moa_remove.hypervolume, moa_true.hypervolume)
        self.assertEqual(moa_add.hypervolume, moa_true.hypervolume)

        moa = MOArchive3d([[1, 2, 3], [2, 3, 1], [3, 1, 2]], reference_point=[6, 6, 6])
        moa.add([1, 1, 1])
        moa.remove([1, 1, 1])
        self.assertEqual(len(moa.points), 0)

    def test_lexsort(self):
        # TODO: test the lexsort function without using numpy
        pass

    def test_contributing_hypervolume(self):
        points = [[1, 2, 3], [2, 3, 1], [3, 1, 2]]
        moa = MOArchive3d(points, reference_point=[4, 4, 4])
        self.assertEqual(moa.contributing_hypervolume([1, 2, 3]), 3)
        self.assertEqual(moa.contributing_hypervolume([2, 3, 1]), 3)
        self.assertEqual(moa.contributing_hypervolume([3, 1, 2]), 3)

        points = list(itertools.permutations([1, 2, 3]))
        moa = MOArchive3d(points, reference_point=[4, 4, 4])
        for p in points:
            self.assertEqual(moa.contributing_hypervolume(list(p)), 1)

        points = get_stacked_points(100, ['random', 'random', 0])
        moa = MOArchive3d(points, reference_point=[1, 1, 1])
        moa2d = MOArchive2D([[p[0], p[1]] for p in points], reference_point=[1, 1])
        for p in moa2d:
            self.assertAlmostEqual(moa.contributing_hypervolume(p + [0]),
                                   moa2d.contributing_hypervolume(p), places=8)

    def test_hypervolume_improvement(self):
        points = [[1, 2, 3], [2, 3, 1], [3, 1, 2]]
        moa = MOArchive3d(points, reference_point=[4, 4, 4])
        self.assertEqual(moa.hypervolume_improvement([1, 2, 3]), 0)
        self.assertEqual(moa.hypervolume_improvement([2, 3, 1]), 0)
        self.assertEqual(moa.hypervolume_improvement([3, 1, 2]), 0)
        self.assertEqual(moa.hypervolume_improvement([4, 4, 4]),
                         -moa.distance_to_pareto_front([4, 4, 4]))
        self.assertEqual(moa.hypervolume_improvement([1, 1, 1]), 14)
        self.assertEqual(moa.hypervolume_improvement([2, 2, 2]), 1)

        points = get_stacked_points(100, ['random', 'random', 0])
        moa = MOArchive3d(points, reference_point=[1, 1, 1])
        moa2d = MOArchive2D([[p[0], p[1]] for p in points], reference_point=[1, 1])

        new_points = get_random_points(100, 2)

        hv_start = moa.hypervolume
        for p in new_points:
            hv_imp2d = float(moa2d.hypervolume_improvement(p))
            if hv_imp2d > 0:
                self.assertAlmostEqual(hv_imp2d, moa.hypervolume_improvement(p + [0]), places=8)
            else:
                self.assertAlmostEqual(hv_imp2d, moa.hypervolume_improvement(p + [1]), places=8)

        # make sure this doesn't change the hypervolume of the archive
        hv_end = moa.hypervolume
        self.assertAlmostEqual(hv_start, hv_end, places=8)

    def test_get_non_dominated_points(self):
        n_points = 1000
        for mode in ['spherical', 'linear']:
            points = get_non_dominated_points(n_points, mode=mode)
            self.assertEqual(len(points), n_points)
            moa = MOArchive3d(points, reference_point=[1, 1, 1])
            self.assertEqual(len(moa.points), n_points)
            self.assertSetEqual(list_to_set(points), list_to_set(moa.points))


if __name__ == '__main__':
    unittest.main()
