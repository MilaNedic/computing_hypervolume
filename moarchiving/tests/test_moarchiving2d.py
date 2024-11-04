from moarchiving.moarchiving2d import BiobjectiveNondominatedSortedList as MOArchive2d

import unittest
import random
import math

inf = float('inf')


def list_to_set(lst):
    return set([tuple(p) for p in lst])


class MyTestCase(unittest.TestCase):
    def test_hypervolume_easy(self):
        """ test the hypervolume calculation for a simple case """
        points = [[1, 2], [2, 1]]
        moa = MOArchive2d(points, reference_point=[3, 3], infos=["A", "B"])
        self.assertEqual(moa.hypervolume, 3)

    def test_infos_non_dominated(self):
        """ test if the infos are stored correctly - if the points are non dominated,
        the infos should be the same"""
        points = [
            [1, 2],
            [2, 1],
            [1.3, 1.7],
            [1.5, 1.5]
        ]
        infos = [str(p) for p in points]

        moa = MOArchive2d(points, [3, 3], infos=infos)
        # assert that the infos are stored in the same order as the points
        self.assertEqual([str(p[:2]) for p in moa.points], moa.infos)
        # assert that all the points in the archive are non dominated and thus have the same info
        self.assertSetEqual(set([str(p) for p in points]), set(moa.infos))

    def test_infos_dominated(self):
        """ test if the infos about dominated points are removed """
        points = [
            [1, 3],
            [3, 2],
            [2, 3],
            [3, 1]
        ]
        infos = ["A", "B", "C", "D"]

        moa = MOArchive2d(points, [6, 6, 6], infos=infos)
        # assert that only points A and D are stored in the archive
        self.assertSetEqual({"A", "D"}, set(moa.infos))

    def test_in_domain(self):
        """ test if the in_domain function works correctly """
        ref_point = [6, 6, 6]
        moa = MOArchive2d([[1, 1]], ref_point)

        # test if the points are in the domain
        self.assertTrue(moa.in_domain([1, 2]))
        self.assertTrue(moa.in_domain([5.9, 5.9]))
        # test if the point is not in the domain
        self.assertFalse(moa.in_domain([7, 8]))
        self.assertFalse(moa.in_domain([6, 6]))
        self.assertFalse(moa.in_domain([0, 6]))

    def test_add(self):
        """ test if the add_points function works correctly """
        ref_point = [6, 6]
        start_points = [[1, 3], [5, 1]]
        moa = MOArchive2d(start_points, ref_point)

        # add point that is not dominated and does not dominate any other point
        u1 = [3, 2]
        moa.add(u1)
        self.assertSetEqual(list_to_set(start_points + [u1]), list_to_set(moa.points))

        # add point that is dominated by another point in the archive
        u2 = [4, 4]
        moa.add(u2)
        self.assertSetEqual(list_to_set(start_points + [u1]), list_to_set(moa.points))

        # add point that dominates another point in the archive
        u3 = [2, 2]
        moa.add(u3)
        self.assertSetEqual(list_to_set(start_points + [u3]), list_to_set(moa.points))

    def test_dominates(self):
        """ Test the dominates function """
        ref_point = [6, 6]
        points = [[1, 5], [5, 1], [3, 3]]
        moa = MOArchive2d(points, ref_point)

        # test that the points that are already in the archive are dominated
        for p in points:
            self.assertTrue(moa.dominates(p))

        # test other dominated points
        self.assertTrue(moa.dominates([5, 5]))
        self.assertTrue(moa.dominates([3, 4]))

        # test non dominated points
        self.assertFalse(moa.dominates([3, 2]))
        self.assertFalse(moa.dominates([2, 4]))
        self.assertFalse(moa.dominates([1, 1]))

    def test_copy_MOArchive(self):
        """ Test the copy function of the MOArchive3d class """
        points = [[1, 3], [2, 2], [3, 1]]
        moa = MOArchive2d(points, reference_point=[6, 6])
        moa_copy = moa.copy()

        self.assertEqual(moa.hypervolume, moa_copy.hypervolume)

        moa.add([1.5, 1.5])
        moa_copy.add([0.5, 5])

        self.assertNotEqual(moa.hypervolume, moa_copy.hypervolume)
        self.assertEqual(len(moa.points), 3)
        self.assertEqual(len(moa_copy.points), 4)

    def test_hypervolume_plus(self):
        """ test the hypervolume_plus indicator """
        moa = MOArchive2d(reference_point=[1, 1])
        self.assertEqual(moa.hypervolume_plus, inf)

        moa.add([2, 2])
        self.assertEqual(moa.hypervolume_plus, math.sqrt(2))

        moa.add_list([[0, 5], [1, 2], [3, 2]])
        self.assertEqual(moa.hypervolume_plus, 1)

        moa.add([1, 1])
        self.assertEqual(moa.hypervolume_plus, 0)

        moa.add([0.5, 0.5])
        self.assertEqual(moa.hypervolume_plus, -moa.hypervolume)

        moa = MOArchive2d(reference_point=[1, 1])
        prev_hv_plus = moa.hypervolume_plus
        for i in range(1000):
            point = [10 * random.random(), 10 * random.random()]
            moa.add(point)
            self.assertLessEqual(moa.hypervolume_plus, prev_hv_plus)
            prev_hv_plus = moa.hypervolume_plus


if __name__ == '__main__':
    unittest.main()
