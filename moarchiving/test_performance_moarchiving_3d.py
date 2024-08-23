from moarchiving3d import MOArchive3d
from moarchiving_utils import my_lexsort
from point_sampling import get_non_dominated_points
import matplotlib.pyplot as plt
import pandas as pd

import time
import numpy as np
import os


def test_add(pop_size=100, n_gen=10):
    ref_point = [1, 1, 1]

    times_one_by_one = []
    times_all_at_once = []
    times_gen_by_gen = []
    print("TEST HYPERVOLUME AFTER ADD")
    print(f"{'num points':10} | {'all at once':10} | {'one by one':10} | {'gen by gen':10} |")

    points = get_non_dominated_points(pop_size * n_gen)
    points = points.tolist()

    for gen in range(1, n_gen + 1):
        t0 = time.time()
        moa_true = MOArchive3d(points[:(gen * pop_size)], ref_point)
        true_hv = moa_true.hypervolume
        t1 = time.time()

        moa_add = MOArchive3d([], ref_point)
        for i in range(gen * pop_size):
            moa_add.add(points[i])
        t2 = time.time()

        moa_add_gen = MOArchive3d([], ref_point)
        for i in range(gen):
            moa_add_gen.add_list(points[(i * pop_size):((i + 1) * pop_size)])
        t3 = time.time()

        times_all_at_once.append(t1 - t0)
        times_one_by_one.append(t2 - t1)
        times_gen_by_gen.append(t3 - t2)

        print(f"{gen * pop_size:10} | {t1 - t0:.8f} | {t2 - t1:.8f} | {t3 - t2:.8f} |")

    x = list(range(pop_size, pop_size * (n_gen + 1), pop_size))
    df = pd.DataFrame({"all_at_once": times_all_at_once,
                       "one_by_one": times_one_by_one,
                       "gen_by_gen": times_gen_by_gen}, index=x)
    # add current date and time to the file name
    date = time.strftime("%m%d-%H%M%S")
    f_name = f"test_results/add_{date}.csv"
    df.to_csv(f_name)


def plot_add_results():
    # get the latest file with the results
    f_names = os.listdir("test_results")
    f_names = [f for f in f_names if "add" in f]
    f_names.sort()
    f_name = f_names[-1]

    df = pd.read_csv(f"test_results/{f_name}", index_col=0)

    # use polyval to fit a quadratic polynomial to the data
    p_one_by_one = np.polyfit(df.index, df["one_by_one"], 2)
    p_gen_by_gen = np.polyfit(df.index, df["gen_by_gen"], 2)
    p_all_at_once = np.polyfit(df.index, df["all_at_once"], 2)

    # plot the data and the fitted polynomials
    fig, ax = plt.subplots()
    ax.set_xlabel("Number of nondominated points")
    ax.set_ylabel("Time [s]")
    # style: -o
    ax.plot(df.index, df["one_by_one"], 'o', label="one by one", color='tab:orange')
    ax.plot(df.index, np.polyval(p_one_by_one, df.index), '--', color='tab:orange', alpha=0.4,
            label=f"{p_one_by_one[0]:.2E} x^2 + O(x)")

    ax.plot(df.index, df["gen_by_gen"], 'o', label="gen by gen", color='tab:red')
    ax.plot(df.index, np.polyval(p_gen_by_gen, df.index), '--', color='tab:red', alpha=0.4,
            label=f"{p_gen_by_gen[0]:.2E} x^2 + O(x)")

    ax.plot(df.index, df["all_at_once"], 'o', label="all at once", color='tab:blue')
    ax.plot(df.index, np.polyval(p_all_at_once, df.index), '--', color='tab:blue', alpha=0.4,
            label=f"{p_all_at_once[0]:.2E} x^2 + O(x)")

    plt.legend()
    plt.title(f"Adding points to archive - {f_name[4:-4]}")
    plt.show()


def test_kink_points():
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


def test_lexsort():
    print("TEST LEXSORT")
    print(f"{'num points':10} | {'my lexsort':10} | {'np lexsort':10} |")
    for n in range(7):
        pts = np.random.rand(10 ** n, 3)
        t0 = time.time()
        my_lexsort([pts[:, i] for i in range(3)])
        t1 = time.time()
        np.lexsort([pts[:, i] for i in range(3)])
        t2 = time.time()

        print(f"{10**n:10} | {t1-t0:.8f} | {t2-t1:.8f} |")


def test_contributing_hypervolume():
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


def test_hypervolume_improvement():
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


if __name__ == "__main__":
    test_add(n_gen=20)
    plot_add_results()
    # test_kink_points()
    # test_lexsort()
    # test_contributing_hypervolume()
    test_hypervolume_improvement()
