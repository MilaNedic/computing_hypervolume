from moarchiving3d import MOArchive3d, DLNode
from moarchiving2d import BiobjectiveNondominatedSortedList as MOArchive2D
from hv_plus import calc_hypervolume_3D
from point_sampling import spherical_front, linear_front
import matplotlib.pyplot as plt

import time
import unittest
import numpy as np
import os


def list_to_set(lst):
    return set([tuple(p) for p in lst])


def get_non_dominated_points(n_points, mode='spherical'):
    if mode == 'spherical':
        return np.array(spherical_front(1, n_points, normalized=False))
    elif mode == 'linear':
        return np.array(linear_front(1, n_points, normalized=False))


class MyTestCase(unittest.TestCase):
    def test_hypervolume(self):
        points = [[1, 2, 3], [2, 3, 1], [3, 1, 2]]
        moa = MOArchive3d(points, reference_point=[4, 4, 4])
        self.assertEqual(moa.hypervolume, 13)

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
            moa = MOArchive3d(data_points, ref_point, infos)
            hv_new = moa.hypervolume

            # calculate the hypervolume using the old implementation
            hv_old = calc_hypervolume_3D(data_points, ref_point)

            # compare the hypervolumes
            print(f"{f_name:20} | {hv_new:.8f} | {hv_old:.8f} |")

            # assert hyper volumes are equal
            self.assertAlmostEqual(hv_new, hv_old, places=8)
            # assert infos are stored correctly
            self.assertEqual([str(p[:3]) for p in moa.points_list], moa.infos_list)

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
        self.assertEqual([str(p[:3]) for p in moa.points_list], moa.infos_list)
        # assert that all the points in the archive are non dominated and thus have the same info
        self.assertSetEqual(set([str(p) for p in points]), set(moa.infos_list))

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
        self.assertSetEqual({"A", "D"}, set(moa.infos_list))

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
        self.assertSetEqual(list_to_set(start_points + [u1]), list_to_set(moa.points_list))

        # add point that is dominated by another point in the archive
        u2 = [4, 5, 2]
        moa.add(u2)
        self.assertSetEqual(list_to_set(start_points + [u1]), list_to_set(moa.points_list))

        # add point that dominates another point in the archive
        u3 = [3, 1, 2]
        moa.add(u3)
        self.assertSetEqual(list_to_set(start_points[:2] + [u1, u3]), list_to_set(moa.points_list))

    def test_hypervolume_after_add(self, n_points=1000, n_tests=10):
        ref_point = [1, 1, 1]

        for t in range(n_tests):
            np.random.seed(t)
            points = np.round(np.random.rand(n_points, 3), 3).tolist()
            infos = [str(p) for p in range(n_points)]
            moa = MOArchive3d(points, ref_point, infos=infos)
            true_hv = moa.hypervolume

            moa_add = MOArchive3d(points[:1], ref_point, infos=infos[:1])
            for i in range(1, n_points):
                moa_add.add(points[i], infos[i])

            self.assertAlmostEqual(moa_add.hypervolume, true_hv, places=6)

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

        self.assertAlmostEqual(np.sqrt(2), moa.distance_to_hypervolume_area([0, 3, 3]), places=6)
        self.assertAlmostEqual(np.sqrt(2), moa.distance_to_hypervolume_area([2, 3, 3]), places=6)
        self.assertAlmostEqual(np.sqrt(3), moa.distance_to_hypervolume_area([3, 3, 3]), places=6)
        self.assertAlmostEqual(np.sqrt(147), moa.distance_to_hypervolume_area([9, 9, 9]), places=6)

    def test_kink_points(self):
        print("TEST KINK POINTS")
        for pareto_type in ['spherical', 'linear']:
            print(f"{pareto_type} pareto front")
            print(f"num points | non-dom p |  moa init  |   alg tea  |   alg new  |")
            test_n_points = [2**i for i in range(1, 11)]

            for n_points in test_n_points:
                # read the data points and the reference point from the file
                data_points = get_non_dominated_points(n_points, mode=pareto_type)
                infos = [str(p) for p in data_points.tolist()]
                ref_point = [1, 1, 1]

                # calculate the hypervolume using the new implementation

                t0 = time.time()
                moa = MOArchive3d(data_points, ref_point, infos)
                t1 = time.time()
                kink_points_tea = moa._get_kink_points_tea()
                t2 = time.time()
                kink_points = moa._get_kink_points()
                t3 = time.time()
                non_dom_p = len(moa.points_list)

                print(f"{n_points:10} | {non_dom_p:9} | {t1-t0:.8f} | {t2-t1:.8f} | {t3-t2:.8f} |")

                self.assertSetEqual(list_to_set(kink_points_tea), list_to_set(kink_points))

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
        points = np.hstack([np.random.rand(n_points, 2), np.zeros((n_points, 1))])

        moa3d = MOArchive3d(points, reference_point=[1, 1, 1])
        moa2d = MOArchive2D(points[:, :2], reference_point=[1, 1])
        moa3d_no_ref = MOArchive3d(points)

        new_points = np.hstack([np.random.rand(n_test_points, 2), np.ones((n_test_points, 1))])
        for point in new_points:
            d2 = moa2d.distance_to_pareto_front(point[:2].tolist())
            d3 = moa3d.distance_to_pareto_front(point.tolist())
            d3_no_ref = moa3d_no_ref.distance_to_pareto_front(point.tolist())
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

        self.assertEqual(len(moa.points_list), 4)
        self.assertEqual(len(moa_copy.points_list), 3)

        self.assertFalse(moa.hypervolume == moa_copy.hypervolume)

    def test_remove(self, n_points=100, n_points_remove=50):
        points = [[1, 2, 3], [2, 3, 1], [3, 1, 2]]
        moa_remove = MOArchive3d(points, reference_point=[6, 6, 6])
        moa_remove.remove([1, 2, 3])
        self.assertEqual(len(moa_remove.points_list), 2)
        self.assertSetEqual(list_to_set(moa_remove.points_list), list_to_set(points[1:]))
        self.assertEqual(moa_remove.hypervolume,
                         MOArchive3d(points[1:], reference_point=[6, 6, 6]).hypervolume)

        points = get_non_dominated_points(n_points)

        remove_idx = np.random.choice(range(n_points), n_points_remove, replace=False)
        keep_idx = [i for i in range(n_points) if i not in remove_idx]

        moa_true = MOArchive3d(points[keep_idx, :], reference_point=[1, 1, 1])
        moa_remove = MOArchive3d(points, reference_point=[1, 1, 1])
        for i in remove_idx:
            moa_remove.remove(points[i].tolist())
        moa_add = MOArchive3d([], reference_point=[1, 1, 1])
        for i in keep_idx:
            moa_add.add(points[i].tolist())

        # assert that the points are the same in all archives and the hypervolume is the same
        self.assertEqual(len(moa_add.points_list), len(moa_true.points_list))
        self.assertEqual(len(moa_remove.points_list), len(moa_true.points_list))

        self.assertSetEqual(list_to_set(moa_remove.points_list), list_to_set(moa_true.points_list))
        self.assertSetEqual(list_to_set(moa_add.points_list), list_to_set(moa_true.points_list))

        self.assertEqual(moa_remove.hypervolume, moa_true.hypervolume)
        self.assertEqual(moa_add.hypervolume, moa_true.hypervolume)

        moa = MOArchive3d([[1, 2, 3], [2, 3, 1], [3, 1, 2]], reference_point=[6, 6, 6])
        moa.add([1, 1, 1])
        moa.remove([1, 1, 1])
        self.assertEqual(len(moa.points_list), 0)

    def test_lexsort(self):
        pts3d = np.random.rand(100, 3)
        pts4d = np.random.rand(100, 4)

        result_my = MOArchive3d.my_lexsort((pts3d[:, 0], pts3d[:, 1], pts3d[:, 2]))
        result_numpy = np.lexsort((pts3d[:, 0], pts3d[:, 1], pts3d[:, 2]))
        for r1, r2 in zip(result_my, result_numpy):
            self.assertEqual(r1, r2)

        result_my = MOArchive3d.my_lexsort((pts4d[:, 0], pts4d[:, 1], pts4d[:, 2], pts4d[:, 3]))
        result_numpy = np.lexsort((pts4d[:, 0], pts4d[:, 1], pts4d[:, 2], pts4d[:, 3]))
        for r1, r2 in zip(result_my, result_numpy):
            self.assertEqual(r1, r2)

        print(f"{'num points':10} | {'my lexsort':10} | {'np lexsort':10} |")
        for n in range(2, 7):
            pts = np.random.rand(10 ** n, 3)
            t0 = time.time()
            MOArchive3d.my_lexsort([pts[:, i] for i in range(3)])
            t1 = time.time()
            np.lexsort([pts[:, i] for i in range(3)])
            t2 = time.time()

            print(f"{10**n:10} | {t1-t0:.8f} | {t2-t1:.8f} |")

    def test_contributing_hypervolume(self):
        points = [[1, 2, 3], [2, 3, 1], [3, 1, 2]]
        moa = MOArchive3d(points, reference_point=[4, 4, 4])
        self.assertEqual(moa.contributing_hypervolume([1, 2, 3]), 3)
        self.assertEqual(moa.contributing_hypervolume([2, 3, 1]), 3)
        self.assertEqual(moa.contributing_hypervolume([3, 1, 2]), 3)

        points = np.hstack([np.random.rand(100, 2), np.zeros((100, 1))])
        moa = MOArchive3d(points, reference_point=[1, 1, 1])
        moa2d = MOArchive2D(points[:, :2], reference_point=[1, 1])
        for p in moa2d:
            self.assertAlmostEqual(moa.contributing_hypervolume(p + [0]),
                                   moa2d.contributing_hypervolume(p), places=8)

        # test speed of the naive and paper implementation
        print("TEST CONTRIBUTING HYPERVOLUME")
        for pareto_type in ['spherical', 'linear']:
            print(f"{pareto_type} pareto front")
            print(f"{'archive s':10} | {'naive':10} |")
            n_points_test = 1000
            for n_points_archive in [2 ** i for i in range(10)]:
                data_points = get_non_dominated_points(n_points_archive)
                moa = MOArchive3d(data_points, reference_point=[1, 1, 1])

                new_points = np.random.rand(n_points_test, 3)
                new_points = [p.tolist() for p in new_points]
                t0 = time.time()
                hv1 = [moa.contributing_hypervolume(p) for p in new_points]
                t1 = time.time()
                print(f"{n_points_archive:10} | {t1-t0:.8f} |")

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

        points = np.hstack([np.random.rand(100, 2), np.zeros((100, 1))])
        new_points = np.random.rand(100, 2)
        moa = MOArchive3d(points, reference_point=[1, 1, 1])
        moa2d = MOArchive2D(points[:, :2], reference_point=[1, 1])

        hv_start = moa.hypervolume
        for p in new_points:
            p = p.tolist()
            hv_imp2d = float(moa2d.hypervolume_improvement(p))
            if hv_imp2d > 0:
                self.assertAlmostEqual(hv_imp2d, moa.hypervolume_improvement(p + [0]), places=8)
            else:
                self.assertAlmostEqual(hv_imp2d, moa.hypervolume_improvement(p + [1]), places=8)

        # make sure this doesn't change the hypervolume of the archive
        hv_end = moa.hypervolume
        self.assertAlmostEqual(hv_start, hv_end, places=8)

        # test speed of the naive and paper implementation
        print("TEST HYPERVOLUME IMPROVEMENT")
        fig = plt.figure()
        for pareto_type in ['spherical', 'linear']:
            print(f"{pareto_type} pareto front")
            print(f"{'archive s':10} | {'mila':10} | {'naive':10} |")
            n_points_test = 1000
            archive_sizes = [2 ** i for i in range(7)]
            results_naive = []
            results_mila = []
            for n_points_archive in archive_sizes:
                data_points = get_non_dominated_points(n_points_archive)
                moa = MOArchive3d(data_points, reference_point=[1, 1, 1])

                new_points = np.random.rand(n_points_test, 3)
                new_points = [p.tolist() for p in new_points]
                t0 = time.time()
                hv1 = [moa.hypervolume_improvement(p) for p in new_points]
                t1 = time.time()
                hv2 = [moa.hypervolume_improvement_naive(p) for p in new_points]
                t2 = time.time()

                results_naive.append(t2-t1)
                results_mila.append(t1-t0)
                print(f"{n_points_archive:10} | {t1-t0:.8f} | {t2-t1:.8f} |")

            plt.plot(archive_sizes, results_mila, label=f"mila {pareto_type}")
            plt.plot(archive_sizes, results_naive, label=f"naive {pareto_type}")

        plt.legend()
        plt.title("Hypervolume improvement")
        plt.show()

    def test_get_non_dominated_points(self):
        n_points = 1000
        for mode in ['spherical', 'linear']:
            points = get_non_dominated_points(n_points, mode=mode)
            self.assertEqual(len(points), n_points)
            moa = MOArchive3d(points, reference_point=[1, 1, 1])
            self.assertEqual(len(moa.points_list), n_points)
            self.assertSetEqual(list_to_set(points), list_to_set(moa.points_list))


if __name__ == '__main__':
    unittest.main()