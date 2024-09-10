from moarchiving3d import MOArchive3d
from moarchiving_utils import my_lexsort
from point_sampling import get_non_dominated_points
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd

import time
import numpy as np
import os


def plot_performance(f_name=None, plot_function="add", poly_degree=2, xlabel="Archive size",
                     ylabel="Time [s]", title=""):
    if f_name is None:
        f_names = os.listdir("test_results")
        f_names = [f for f in f_names if plot_function in f]
        f_names.sort()
        f_name = f_names[-1]

    df = pd.read_csv(f"test_results/{f_name}", index_col=0)

    colors = list(mcolors.TABLEAU_COLORS.keys())

    fig, ax = plt.subplots()
    for i, col in enumerate(df.columns):
        p = np.polyfit(df.index, df[col], poly_degree)
        ax.plot(df.index, df[col], 'o', label=col, color=colors[i])
        ax.plot(df.index, np.polyval(p, df.index), '--', color=colors[i], alpha=0.4,
                label=f"{p[0]:.2E} x^{poly_degree} + O(x^{poly_degree-1})")

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.legend()
    plt.title(f"{plot_function}: ({f_name[(len(plot_function)+1):-4]}) \n{title}")
    plt.show()


def test_add(pop_size=100, n_gen=10):
    ref_point = [1, 1, 1]

    times_one_by_one = []
    times_all_at_once = []
    times_gen_by_gen = []
    recompute_every_gen = []
    print("TEST HYPERVOLUME AFTER ADD")
    print(f"{'num points':10} | {'all at once':10} | {'one by one':10} | {'gen by gen':10} "
          f"| {'recompute':10} |")

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

        for g in range(gen):
            moa_add_gen2 = MOArchive3d(points[:(g * pop_size)], ref_point)
        t4 = time.time()

        times_all_at_once.append(t1 - t0)
        times_one_by_one.append(t2 - t1)
        times_gen_by_gen.append(t3 - t2)
        recompute_every_gen.append(t4 - t3)

        print(f"{gen * pop_size:10} | {t1 - t0:.8f} | {t2 - t1:.8f} | {t3 - t2:.8f} "
              f"| {t4 - t3:.8f} |")

    x = list(range(pop_size, pop_size * (n_gen + 1), pop_size))
    df = pd.DataFrame({"all_at_once": times_all_at_once,
                       "one_by_one": times_one_by_one,
                       "recompute_every_gen": recompute_every_gen,
                       "gen_by_gen": times_gen_by_gen}, index=x)
    # add current date and time to the file name
    date = time.strftime("%m%d-%H%M%S")
    f_name = f"test_results/add_{date}.csv"
    df.to_csv(f_name)


def test_kink_points(include_tea=False):
    print("TEST KINK POINTS")
    test_n_points = list(range(500, 5001, 500))
    df = pd.DataFrame()
    for pareto_type in ['spherical', 'linear']:
        print(f"{pareto_type} pareto front")
        print(f"num points | non-dom p |  moa init  |   alg tea  |   alg new  |")
        time_tea = []
        time_new = []
        for n_points in test_n_points:
            # read the data points and the reference point from the file
            data_points = get_non_dominated_points(n_points, mode=pareto_type)
            infos = [str(p) for p in data_points.tolist()]
            ref_point = [1, 1, 1]

            # calculate the hypervolume using the new implementation

            t0 = time.time()
            moa = MOArchive3d(data_points, ref_point, infos)
            t1 = time.time()
            if include_tea:
                kink_points_tea = moa._get_kink_points_tea()
            t2 = time.time()
            kink_points = moa._get_kink_points()
            t3 = time.time()
            non_dom_p = len(moa.points_list)

            time_tea.append(t2-t1)
            time_new.append(t3-t2)

            print(f"{n_points:10} | {non_dom_p:9} | {t1-t0:.8f} | {t2-t1:.8f} | {t3-t2:.8f} |")
        if include_tea:
            df[f"tea_{pareto_type}"] = time_tea
        df[f"new_{pareto_type}"] = time_new
    df.index = test_n_points

    date = time.strftime("%m%d-%H%M%S")
    f_name = f"test_results/kink_points_{date}.csv"
    df.to_csv(f_name)


def test_lexsort():
    n_test_points = list(range(10000, 100001, 10000))
    df = pd.DataFrame()
    time_np = []
    time_my = []

    print("TEST LEXSORT")
    print(f"{'num points':10} | {'my lexsort':10} | {'np lexsort':10} |")
    for n in n_test_points:
        pts = np.random.rand(n, 3)
        t0 = time.time()
        my_lexsort([pts[:, i] for i in range(3)])
        t1 = time.time()
        np.lexsort([pts[:, i] for i in range(3)])
        t2 = time.time()

        time_my.append(t1-t0)
        time_np.append(t2-t1)
        print(f"{n:10} | {t1-t0:.8f} | {t2-t1:.8f} |")
    df["my_lexsort"] = time_my
    df["np_lexsort"] = time_np
    df.index = n_test_points

    date = time.strftime("%m%d-%H%M%S")
    f_name = f"test_results/lexsort_{date}.csv"
    df.to_csv(f_name)


def test_contributing_hypervolume():
    df = pd.DataFrame()
    n_points_test = list(range(500, 5001, 500))
    n = 20

    print("TEST CONTRIBUTING HYPERVOLUME")
    for pareto_type in ['spherical', 'linear']:
        times = []
        print(f"{pareto_type} pareto front")
        print(f"{'archive s':10} | {'naive':10} |")
        for n_points_archive in n_points_test:
            data_points = get_non_dominated_points(n_points_archive, mode=pareto_type)
            moa = MOArchive3d(data_points, reference_point=[1, 1, 1])

            new_points = [p.tolist() for p in data_points[:n]]
            t0 = time.time()
            hv1 = [moa.contributing_hypervolume(p) for p in new_points]
            t1 = time.time()
            t = (t1 - t0) / n
            times.append(t)
            print(f"{n_points_archive:10} | {t:.8f} |")

        df[f"naive_{pareto_type}"] = times
    df.index = n_points_test

    date = time.strftime("%m%d-%H%M%S")
    f_name = f"test_results/contributing_hypervolume_{date}.csv"
    df.to_csv(f_name)


def test_hypervolume_improvement(include_naive=False):
    df = pd.DataFrame()
    archive_sizes = list(range(100, 1001, 100))

    print("TEST HYPERVOLUME IMPROVEMENT")
    for pareto_type in ['spherical', 'linear']:
        print(f"{pareto_type} pareto front")
        print(f"{'archive s':10} | {'mila':10} | {'naive':10} |")
        n_points_test = 100
        results_naive = []
        results_mila = []
        for n_points_archive in archive_sizes:
            data_points = get_non_dominated_points(n_points_archive, mode=pareto_type)
            moa = MOArchive3d(data_points, reference_point=[1, 1, 1])

            new_points = get_non_dominated_points(n_points_test, mode=pareto_type)
            new_points = [p.tolist() for p in new_points]
            t0 = time.time()
            hv1 = [moa.hypervolume_improvement(p) for p in new_points]
            t1 = time.time()
            print("t0-t1", t1-t0, end=" ")

            hv2 = [moa.hypervolume_improvement_naive(p) for p in new_points]
            t2 = time.time()
            print("t1-t2", t2-t1)

            results_naive.append((t2-t1) / n_points_test)
            results_mila.append((t1-t0) / n_points_test)
            print(f"{n_points_archive:10} | {(t1-t0) / n_points_test:.8f} "
                  f"| {(t2-t1) / n_points_test:.8f} |")

        df[f"mila_{pareto_type}"] = results_mila
        if include_naive:
            df[f"naive_{pareto_type}"] = results_naive
    df.index = archive_sizes

    date = time.strftime("%m%d-%H%M%S")
    f_name = f"test_results/hypervolume_improvement_{date}.csv"
    df.to_csv(f_name)


def test_hypervolume_calculation():
    df = pd.DataFrame()
    archive_sizes = list(range(10000, 100001, 10000))

    print("TEST HYPERVOLUME CALCULATION")
    for pareto_type in ['spherical', 'linear']:
        print(f"{pareto_type} pareto front")
        print(f"{'archive s':10} | {'hv calc':10} |")
        results = []
        for n_points_archive in archive_sizes:
            data_points = get_non_dominated_points(n_points_archive, mode=pareto_type)
            moa = MOArchive3d(data_points, reference_point=[1, 1, 1])

            t0 = time.time()
            moa.compute_hypervolume()
            t1 = time.time()
            t = t1 - t0
            results.append(t)
            print(f"{n_points_archive:10} | {t:.8f} |")
        df[f"set_hv_{pareto_type}"] = results
    df.index = archive_sizes

    date = time.strftime("%m%d-%H%M%S")
    f_name = f"test_results/hypervolume_calculation_{date}.csv"
    df.to_csv(f_name)


if __name__ == "__main__":
    test_add(n_gen=20)
    plot_performance(plot_function="add", title="(cumulative time to add points)")

    # test_kink_points()
    # plot_performance(plot_function="kink_points", poly_degree=1,
    #                  title=r"($\approx$ time to calculate distance to pareto front for one point)")

    # test_lexsort()
    # plot_performance(plot_function="lexsort", poly_degree=1)

    # test_contributing_hypervolume()
    # plot_performance(plot_function="contributing_hypervolume",
    #                  title="(time to calculate contributing hv for one point from archive)")

    # test_hypervolume_improvement(include_naive=True)
    # plot_performance(plot_function="hypervolume_improvement",
    #                  title="(time to calculate hypervolume improvement for one point not in archive)")

    # test_hypervolume_calculation()
    # plot_performance(plot_function="hypervolume_calculation",
    #                  title="(time to calculate hv for already existing archive structure)", poly_degree=1)