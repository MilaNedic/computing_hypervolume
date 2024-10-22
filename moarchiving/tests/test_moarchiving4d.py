from moarchiving.moarchiving3d import MOArchive3d
from moarchiving.moarchiving4d import MOArchive4d
from moarchiving.moarchiving2d import BiobjectiveNondominatedSortedList as MOArchive2D
from moarchiving.tests.point_sampling import (get_non_dominated_points, get_stacked_points,
                                              get_random_points, permute_points)

import unittest
import itertools
import random
import math


def list_to_set(lst):
    return set([tuple(p) for p in lst])


def get_small_test_archive():
    points = [[1, 2, 3, 4], [4, 1, 2, 3], [3, 4, 1, 2], [2, 3, 4, 1]]
    infos = [str(p) for p in points]
    return MOArchive4d(points, [6, 6, 6, 6], infos)


class MyTestCase(unittest.TestCase):
    def test_hypervolume_easy(self):
        """ test the hypervolume calculation for a 'simple' case """
        points = [[0, 1, 2, 3], [1, 2, 3, 0], [2, 3, 0, 1], [3, 0, 1, 2]]
        moa = MOArchive4d(points, reference_point=[4, 4, 4, 4], infos=["A", "B", "C", "D"])
        self.assertEqual(71, moa.hypervolume)


    def test_hypervolume(self):
        """ test the hypervolume calculation, by comparing to the result of original
        implementation in C"""
        points = [
            [1.0, 2.0, 3.0, 1.0],
            [4.0, 5.0, 6.0, 0.5],
            [7.0, 8.0, 9.0, 0.7],
            [2.0, 1.0, 0.5, 0.6],
            [3.0, 4.0, 5.0, 0.8],
            [6.0, 7.0, 8.0, 0.3],
            [9.0, 1.0, 2.0, 0.9],
            [5.0, 6.0, 7.0, 0.2],
            [8.0, 9.0, 1.0, 0.4],
            [0.0, 1.0, 2.0, 0.1]
        ]
        moa = MOArchive4d(points, reference_point=[10, 10, 10, 10])
        self.assertEqual(8143.6, moa.hypervolume)

    def test_infos_non_dominated(self):
        """ test if the infos are stored correctly - if the points are non dominated,
        the infos should be the same"""
        moa = get_small_test_archive()
        # assert that the infos are stored in the same order as the points
        self.assertEqual([str(p) for p in moa.points], moa.infos)

    def test_infos_dominated(self):
        """ test if the infos about dominated points are removed """
        points = [[1, 2, 3, 4], [2, 2, 3, 5], [5, 4, 3, 2], [5, 5, 5, 5]]
        infos = [str(p) for p in points]
        moa = MOArchive4d(points, [6, 6, 6, 6], infos)
        moa.print_cdllist()

        non_dominated_points = [[1, 2, 3, 4], [5, 4, 3, 2]]
        self.assertSetEqual(set([str(p) for p in non_dominated_points]), set(moa.infos))
        self.assertEqual([str(p) for p in moa.points], moa.infos)

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
        self.assertSetEqual(list_to_set(start_points + [u1]), list_to_set(moa.points))

        moa.print_cdllist()
        moa.print_cxcy()

        # add point that is dominated by another point in the archive
        u2 = [4, 5, 2, 4]
        moa.add(u2, "E")
        self.assertSetEqual(list_to_set(start_points + [u1]), list_to_set(moa.points))

        moa.print_cdllist()
        moa.print_cxcy()

        # add point that dominates another point in the archive
        u3 = [2, 3, 1, 4]
        moa.add(u3, "F")
        self.assertSetEqual(list_to_set(start_points[:2] + [u1, u3]), list_to_set(moa.points))

    def test_hypervolume_after_add(self, n_points=1000, n_tests=10):
        ref_point = [1, 1, 1, 1]

        pop_size = 100
        n_gen = 4
        points = get_non_dominated_points(pop_size * n_gen, n_dim=4)

        for gen in range(1, n_gen + 1):
            print(f"gen: {gen}")
            moa_true = MOArchive4d(points[:(gen * pop_size)], ref_point)
            true_hv = moa_true.hypervolume

            moa_add = MOArchive4d([], ref_point)
            for i in range(gen * pop_size):
                moa_add.add(points[i])

            moa_add_list = MOArchive4d([], ref_point)
            for i in range(gen):
                moa_add_list.add_list(points[i * pop_size:(i + 1) * pop_size])

            self.assertAlmostEqual(moa_add.hypervolume, true_hv, places=6)
            self.assertAlmostEqual(moa_add_list.hypervolume, true_hv, places=6)

    def test_dominates(self):
        moa = get_small_test_archive()

        # test that the points that are already in the archive are dominated
        for p in moa.points:
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
        for p in moa.points:
            self.assertEqual([p], moa.dominators(p))
            self.assertEqual(1, moa.dominators(p, number_only=True))

        # test other dominated points
        pass

    def test_distance_to_hypervolume_area(self):
        moa = MOArchive4d()
        self.assertEqual(0, moa.distance_to_hypervolume_area([1, 1, 1, 1]))

        moa.reference_point = [2, 2, 2, 2]
        # for points in the hypervolume area, the distance should be 0
        self.assertEqual(0, moa.distance_to_hypervolume_area([0, 0, 0, 0]))
        self.assertEqual(0, moa.distance_to_hypervolume_area([1, 1, 1, 1]))
        self.assertEqual(0, moa.distance_to_hypervolume_area([2, 2, 2, 2]))
        self.assertEqual(0, moa.distance_to_hypervolume_area([0, 1, 2, 2]))

        # for points outside the hypervolume area, the distance should be the Euclidean distance
        # to the hypervolume area
        self.assertEqual(1, moa.distance_to_hypervolume_area([2, 2, 3, 2]))
        self.assertEqual(1, moa.distance_to_hypervolume_area([2, 0, 3, 2]))
        self.assertEqual(10, moa.distance_to_hypervolume_area([0, 0, 0, 12]))

        self.assertAlmostEqual(math.sqrt(2), moa.distance_to_hypervolume_area([0, 3, 3, 0]), places=6)
        self.assertAlmostEqual(math.sqrt(2), moa.distance_to_hypervolume_area([2, 3, 3, 2]), places=6)
        self.assertAlmostEqual(math.sqrt(4), moa.distance_to_hypervolume_area([3, 3, 3, 3]), places=6)
        self.assertAlmostEqual(math.sqrt(7**2 * 4), moa.distance_to_hypervolume_area([9, 9, 9, 9]), places=6)

    def test_distance_to_pareto_front_compare_2d(self):
        # first make a pseudo 4D pareto front and compare it to 2D pareto front
        n_points = 100
        n_test_points = 100
        # set random seed
        points = get_stacked_points(n_points, ['random', 'random', 0, 0])

        moa4d = MOArchive4d(points, reference_point=[1, 1, 1, 1])
        moa2d = MOArchive2D([[p[0], p[1]] for p in points], reference_point=[1, 1])
        moa4d_no_ref = MOArchive4d(points)

        permutations = [[0, 1, 2, 3], [1, 2, 0, 3], [2, 0, 1, 3], [3, 2, 1, 0], [2, 3, 0, 1]]
        for permutation in permutations:
            perm_points = permute_points(points, permutation)
            moa4d_perm = MOArchive4d(perm_points, reference_point=[1, 1, 1, 1])

            new_points = get_stacked_points(n_test_points, ['random', 'random', 1, 1])
            for point in new_points:
                d2 = moa2d.distance_to_pareto_front(point[:2])
                d4 = moa4d.distance_to_pareto_front(point)
                d4_no_ref = moa4d_no_ref.distance_to_pareto_front(point)
                d4_perm = moa4d_perm.distance_to_pareto_front(permute_points([point], permutation)[0])
                self.assertAlmostEqual(d2, d4, places=8)
                self.assertAlmostEqual(d4, d4_no_ref, places=8)
                self.assertAlmostEqual(d4, d4_perm, places=8)

    def test_distance_to_pareto_front_compare_3d(self):
        # first make a pseudo 4D pareto front and compare it to 3D pareto front
        n_points = 100
        n_test_points = 10
        # set random seed
        points = get_stacked_points(n_points, ['random', 'random', 'random', 0])

        moa4d = MOArchive4d(points, reference_point=[1, 1, 1, 1])
        moa3d = MOArchive3d([[p[0], p[1], p[2]] for p in points], reference_point=[1, 1, 1])
        moa4d_no_ref = MOArchive4d(points)

        permutations = [[0, 1, 2, 3], [1, 2, 3, 0], [2, 0, 1, 3], [3, 2, 1, 0], [2, 3, 0, 1]]
        for permutation in permutations:
            perm_points = permute_points(points, permutation)
            moa4d_perm = MOArchive4d(perm_points, reference_point=[1, 1, 1, 1])

            new_points = get_stacked_points(n_test_points, ['random', 'random', 'random', 1])
            for point in new_points:
                d3 = moa3d.distance_to_pareto_front(point[:3])
                d4 = moa4d.distance_to_pareto_front(point)
                d4_no_ref = moa4d_no_ref.distance_to_pareto_front(point)
                d4_perm = moa4d_perm.distance_to_pareto_front(permute_points([point], permutation)[0])
                self.assertAlmostEqual(d3, d4, places=8)
                self.assertAlmostEqual(d4, d4_no_ref, places=8)
                self.assertAlmostEqual(d4, d4_perm, places=8)

    def test_distance_to_pareto_front(self):
        # first make a pseudo 4D pareto front and compare it to 3D pareto front
        n_points_archive = 100
        n_test_points = 50
        n_points_sampled = 1000
        # set random seed
        points = get_non_dominated_points(n_points_archive, n_dim=4)
        moa = MOArchive4d(points, reference_point=[1, 1, 1, 1])

        for i in range(n_test_points):
            point = get_random_points(1, 4)[0]
            while not moa.dominates(point):
                point = get_random_points(1, 4)[0]
            distance = moa.distance_to_pareto_front(point)

            min_dist = 2
            for j in range(n_points_sampled):
                sample = [p + random.gauss(0, distance) for p in point]
                while moa.dominates(sample):
                    sample = [p + random.gauss(0, distance) for p in point]

                dist = math.sqrt(sum([(p - s) ** 2 for p, s in zip(point, sample)]))
                if dist < min_dist:
                    min_dist = dist
                self.assertTrue(distance <= dist)

    def test_remove(self, n_points=100, n_points_remove=50):
        points = [[1, 2, 3, 4], [2, 3, 4, 1], [3, 4, 1, 2]]
        moa_remove = MOArchive4d(points, reference_point=[6, 6, 6, 6])
        moa_remove.remove([1, 2, 3, 4])
        self.assertEqual(len(moa_remove.points), 2)
        self.assertSetEqual(list_to_set(moa_remove.points), list_to_set(points[1:]))
        self.assertEqual(moa_remove.hypervolume,
                         MOArchive4d(points[1:], reference_point=[6, 6, 6, 6]).hypervolume)

        points = get_non_dominated_points(n_points, n_dim=4)

        remove_idx = list(range(n_points_remove))
        keep_idx = [i for i in range(n_points) if i not in remove_idx]

        moa_true = MOArchive4d([points[i] for i in keep_idx], reference_point=[1, 1, 1, 1])
        moa_remove = MOArchive4d(points, reference_point=[1, 1, 1, 1])
        for i in remove_idx:
            moa_remove.remove(points[i])
        moa_add = MOArchive4d([], reference_point=[1, 1, 1, 1])
        for i in keep_idx:
            moa_add.add(points[i])

        # assert that the points are the same in all archives and the hypervolume is the same
        self.assertEqual(len(moa_add.points), len(moa_true.points))
        self.assertEqual(len(moa_remove.points), len(moa_true.points))

        self.assertSetEqual(list_to_set(moa_remove.points), list_to_set(moa_true.points))
        self.assertSetEqual(list_to_set(moa_add.points), list_to_set(moa_true.points))

        self.assertEqual(moa_remove.hypervolume, moa_true.hypervolume)
        self.assertEqual(moa_add.hypervolume, moa_true.hypervolume)

        moa = MOArchive4d([[1, 2, 3, 4], [2, 3, 4, 1], [3, 4, 1, 2]],
                          reference_point=[6, 6, 6, 6])
        moa.add([1, 1, 1, 1])
        moa.remove([1, 1, 1, 1])
        self.assertEqual(len(moa.points), 0)

    def test_contributing_hypervolume(self):
        points = [list(p) for p in itertools.permutations([1, 2, 3, 4])]
        moa = MOArchive4d(points, reference_point=[5, 5, 5, 5])
        for p in points:
            self.assertEqual(moa.contributing_hypervolume(list(p)), 1)

        points = get_stacked_points(100, [0, 'random', 'random', 'random'])

        moa = MOArchive4d(points, reference_point=[1, 1, 1, 1])
        moa3d = MOArchive3d([[p[1], p[2], p[3]] for p in points], reference_point=[1, 1, 1])
        for p in moa3d.points:
            self.assertAlmostEqual(moa.contributing_hypervolume([0] + p),
                                   moa3d.contributing_hypervolume(p), places=8)

    def test_hypervolume_improvement(self):
        points = [list(p) for p in itertools.permutations([1, 2, 3, 4])]
        moa = MOArchive4d(points, reference_point=[5, 5, 5, 5])
        self.assertEqual(moa.hypervolume_improvement([1, 2, 3, 4]), 0)
        self.assertEqual(moa.hypervolume_improvement([2, 3, 4, 1]), 0)
        self.assertEqual(moa.hypervolume_improvement([3, 4, 1, 2]), 0)
        self.assertEqual(moa.hypervolume_improvement([4, 4, 4, 4]),
                         -moa.distance_to_pareto_front([4, 4, 4, 4]))

        self.assertEqual(moa.hypervolume_improvement([1, 1, 1, 1]), 131)
        self.assertEqual(moa.hypervolume_improvement([2, 2, 2, 2]), 20)
        self.assertEqual(moa.hypervolume_improvement([3, 3, 3, 3]), 1)

        points = get_stacked_points(100, [0, 'random', 'random', 'random'])
        new_points = get_random_points(100, 3)
        moa = MOArchive4d(points, reference_point=[1, 1, 1, 1])
        moa3d = MOArchive3d([[p[1], p[2], p[3]] for p in points], reference_point=[1, 1, 1])

        for p in new_points:
            hv_imp2d = float(moa3d.hypervolume_improvement(p))
            if hv_imp2d > 0:
                self.assertAlmostEqual(hv_imp2d, moa.hypervolume_improvement([0] + p), places=8)
            else:
                self.assertAlmostEqual(hv_imp2d, moa.hypervolume_improvement([1] + p), places=8)


if __name__ == '__main__':
    unittest.main()
