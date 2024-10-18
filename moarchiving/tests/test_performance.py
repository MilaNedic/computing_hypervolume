from moarchiving.moarchive import MOArchive
from moarchiving.moarchiving_utils import my_lexsort
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
        # make polynomial fit ignoring the nan values
        y = df[col]
        # shorten the data to the first nan value
        if np.isnan(y).any():
            idx = np.where(np.isnan(y))[0][0]
            y = y[:idx]
        x = df.index[:len(y)]

        p = np.polyfit(x, y, poly_degree)
        ax.plot(x, y, 'o', label=col, color=colors[i])
        ax.plot(x, np.polyval(p, x), '--', color=colors[i], alpha=0.4,
                label=f"{p[0]:.2E} x^{poly_degree} + O(x^{poly_degree-1})")

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.legend()
    plt.title(f"{plot_function}: ({f_name[(len(plot_function)+1):-4]}) \n{title}")
    plt.show()


def test_add(pop_size=100, n_gen=10, n_dim=3, time_limit=10):
    ref_point = [1] * n_dim

    times_one_by_one = [0]
    times_all_at_once = [0]
    times_gen_by_gen = [0]
    recompute_every_gen = [0]
    print("TEST HYPERVOLUME AFTER ADD", n_dim)
    print(f"{'num points':10} | {'all at once':10} | {'one by one':10} | {'gen by gen':10} "
          f"| {'recompute':10} |")

    points = get_non_dominated_points(pop_size * n_gen, n_dim=n_dim)
    points = points.tolist()

    for gen in range(1, n_gen + 1):
        t0 = time.time()

        if times_all_at_once[-1] is None or times_all_at_once[-1] > time_limit:
            times_all_at_once.append(None)
        else:
            moa_true = MOArchive(points[:(gen * pop_size)], ref_point, n_obj=n_dim)

        t1 = time.time()

        if times_one_by_one[-1] is None or times_one_by_one[-1] > time_limit:
            times_one_by_one.append(None)
        else:
            moa_add = MOArchive([], ref_point, n_obj=n_dim)
            for i in range(gen * pop_size):
                moa_add.add(points[i])

        t2 = time.time()

        if times_gen_by_gen[-1] is None or times_gen_by_gen[-1] > time_limit:
            times_gen_by_gen.append(None)
        else:
            moa_add_gen = MOArchive([], ref_point, n_obj=n_dim)
            for i in range(gen):
                moa_add_gen.add_list(points[(i * pop_size):((i + 1) * pop_size)])

        t3 = time.time()

        if recompute_every_gen[-1] is None or recompute_every_gen[-1] > time_limit:
            recompute_every_gen.append(None)
        else:
            for i in range(gen):
                moa_add_gen2 = MOArchive(points[:((i+1) * pop_size)], ref_point, n_obj=n_dim)

        t4 = time.time()

        if times_all_at_once[-1] is not None:
            times_all_at_once.append(t1 - t0)
        if times_one_by_one[-1] is not None:
            times_one_by_one.append(t2 - t1)
        if times_gen_by_gen[-1] is not None:
            times_gen_by_gen.append(t3 - t2)
        if recompute_every_gen[-1] is not None:
            recompute_every_gen.append(t4 - t3)

        print(f"{gen * pop_size:10} | {t1 - t0:.8f} | {t2 - t1:.8f} | {t3 - t2:.8f} "
              f"| {t4 - t3:.8f} |")

    x = [0] + list(range(pop_size, pop_size * (n_gen + 1), pop_size))
    df = pd.DataFrame({"all_at_once": times_all_at_once,
                       "one_by_one": times_one_by_one,
                       "recompute_every_gen": recompute_every_gen,
                       "gen_by_gen": times_gen_by_gen}, index=x)
    # add current date and time to the file name
    date = time.strftime("%m%d-%H%M%S")
    f_name = f"test_results/add_{n_dim}D_{date}.csv"
    df.to_csv(f_name)


def test_kink_points(pop_size=100, n_gen=20, n_dim=3, time_limit=10):
    print("TEST KINK POINTS")
    test_n_points = list(range(pop_size, pop_size * n_gen + 1, pop_size))
    df = pd.DataFrame()
    times = {
        "kink_spherical": [],
        "kink_linear": [],
        "init_spherical": [],
        "init_linear": []
    }
    for pareto_type in ['spherical', 'linear']:
        print(f"{pareto_type} pareto front")
        print(f"num points |  moa init  |   alg new  |")
        for n_points in test_n_points:
            # read the data points and the reference point from the file
            data_points = get_non_dominated_points(n_points, mode=pareto_type, n_dim=n_dim)
            infos = [str(p) for p in data_points.tolist()]
            ref_point = [1] * n_dim

            # calculate the hypervolume using the new implementation

            t0 = time.time()
            moa = MOArchive(data_points, ref_point, infos)

            t1 = time.time()

            kink_points = moa._get_kink_points()
            t2 = time.time()

            times[f"kink_{pareto_type}"].append(t2 - t1)
            times[f"init_{pareto_type}"].append(t1 - t0)
            print(f"{n_points:10} | {t1-t0:.8f} | {t2-t1:.8f} |")

            if t2 - t1 > time_limit:
                break

    max_len = max(len(times["kink_spherical"]), len(times["kink_linear"]))
    for key in times:
        if len(times[key]) < max_len:
            times[key] += [None] * (max_len - len(times[key]))
        df[key] = times[key]

    df.index = test_n_points[:max_len]

    date = time.strftime("%m%d-%H%M%S")
    f_name = f"test_results/kink_points_{n_dim}D_{date}.csv"
    df.to_csv(f_name)


def test_lexsort(n_dim=3):
    n_test_points = list(range(10000, 100001, 10000))
    df = pd.DataFrame()
    time_np = []
    time_my = []

    print("TEST LEXSORT")
    print(f"{'num points':10} | {'my lexsort':10} | {'np lexsort':10} |")
    for n in n_test_points:
        pts = np.random.rand(n, n_dim)
        t0 = time.time()
        my_lexsort([pts[:, i] for i in range(n_dim)])
        t1 = time.time()
        np.lexsort([pts[:, i] for i in range(n_dim)])
        t2 = time.time()

        time_my.append(t1-t0)
        time_np.append(t2-t1)
        print(f"{n:10} | {t1-t0:.8f} | {t2-t1:.8f} |")
    df["my_lexsort"] = time_my
    df["np_lexsort"] = time_np
    df.index = n_test_points

    date = time.strftime("%m%d-%H%M%S")
    f_name = f"test_results/lexsort_{n_dim}D_{date}.csv"
    df.to_csv(f_name)


def test_contributing_hypervolume(pop_size=500, n_gen=10, n_dim=3, n_reps=10, time_limit=10):
    df = pd.DataFrame()
    n_points_test = list(range(pop_size, pop_size * n_gen + 1, pop_size))

    times = {
        "naive_spherical": [],
        "naive_linear": []
    }

    print("TEST CONTRIBUTING HYPERVOLUME")
    for pareto_type in ['spherical', 'linear']:
        print(f"{pareto_type} pareto front")
        print(f"{'archive s':10} | {'naive':10} |")
        for n_points_archive in n_points_test:
            data_points = get_non_dominated_points(n_points_archive, mode=pareto_type, n_dim=n_dim)
            moa = MOArchive(data_points, reference_point=[1] * n_dim, n_obj=n_dim)

            new_points = [p.tolist() for p in data_points[:n_reps]]
            t0 = time.time()
            hv1 = [moa.contributing_hypervolume(p) for p in new_points]
            t1 = time.time()
            times[f"naive_{pareto_type}"].append((t1 - t0) / n_reps)
            print(f"{n_points_archive:10} | {times[f'naive_{pareto_type}'][-1]:.8f} |")

            if t1 - t0 > time_limit:
                break

    max_len = max(len(times["naive_spherical"]), len(times["naive_linear"]))
    for key in times:
        if len(times[key]) < max_len:
            times[key] += [None] * (max_len - len(times[key]))
        df[key] = times[key]
    df.index = n_points_test[:max_len]

    date = time.strftime("%m%d-%H%M%S")
    f_name = f"test_results/contributing_hypervolume_{n_dim}D_{date}.csv"
    df.to_csv(f_name)


def test_hypervolume_improvement(n_gen=10, pop_size=100, time_limit=10, n_dim=3, n_reps=10):
    df = pd.DataFrame()
    archive_sizes = list(range(pop_size, pop_size * n_gen + 1, pop_size))

    print("TEST HYPERVOLUME IMPROVEMENT")
    times = {
        "times_spherical": [],
        "times_linear": [],
    }
    for pareto_type in ['spherical', 'linear']:
        print(f"{pareto_type} pareto front")
        print(f"{'archive s':10} | {'hv impr':10} |")
        for n_points_archive in archive_sizes:
            data_points = get_non_dominated_points(n_points_archive, mode=pareto_type, n_dim=n_dim)
            moa = MOArchive(data_points, reference_point=[1] * n_dim)

            new_points = get_non_dominated_points(n_reps, mode=pareto_type, n_dim=n_dim)
            new_points = [p.tolist() for p in new_points]
            t0 = time.time()
            hv1 = [moa.hypervolume_improvement(p) for p in new_points]
            t1 = time.time()

            t = (t1 - t0) / n_reps
            times[f"times_{pareto_type}"].append(t)
            print(f"{n_points_archive:10} | {t:.8f} |")

            if t1 - t0 > time_limit:
                break

    max_len = max(len(times["times_spherical"]), len(times["times_linear"]))
    for key in times:
        if len(times[key]) < max_len:
            times[key] += [None] * (max_len - len(times[key]))
        df[key] = times[key]

    df.index = archive_sizes[:max_len]

    date = time.strftime("%m%d-%H%M%S")
    f_name = f"test_results/hypervolume_improvement_{n_dim}D_{date}.csv"
    df.to_csv(f_name)


def test_hypervolume_calculation(n_dim=3):
    df = pd.DataFrame()
    archive_sizes = list(range(10, 101, 10))

    print("TEST HYPERVOLUME CALCULATION")
    for pareto_type in ['spherical', 'linear']:
        print(f"{pareto_type} pareto front")
        print(f"{'archive s':10} | {'hv calc':10} |")
        results = []
        for n_points_archive in archive_sizes:
            data_points = get_non_dominated_points(n_points_archive, n_dim=n_dim, mode=pareto_type)
            moa = MOArchive(list_of_f_vals=data_points)

            t0 = time.time()
            moa.compute_hypervolume()
            t1 = time.time()
            t = t1 - t0
            results.append(t)
            print(f"{n_points_archive:10} | {t:.8f} |")
        df[f"set_hv_{pareto_type}"] = results
    df.index = archive_sizes

    date = time.strftime("%m%d-%H%M%S")
    f_name = f"test_results/hypervolume_calculation_{n_dim}D_{date}.csv"
    df.to_csv(f_name)


if __name__ == "__main__":
    """ ADD POINTS
    test_add(n_gen=20, pop_size=200, n_dim=3, time_limit=10)
    plot_performance(plot_function="add_3D", title="(cumulative time to add points 3d)")

    test_add(n_gen=20, pop_size=50, n_dim=4)
    plot_performance(plot_function="add_4D", title="(cumulative time to add points 4d)")
    # """

    # """ KINK POINTS
    # test_kink_points(pop_size=500, n_gen=20, n_dim=3, time_limit=10)
    plot_performance(plot_function="kink_points_3D", poly_degree=1,
                     title=r"($\approx$ time to calculate distance to pareto front for one point)")

    # test_kink_points(pop_size=50, n_gen=20, n_dim=4, time_limit=10)
    plot_performance(plot_function="kink_points_4D", poly_degree=2,
                     title=r"($\approx$ time to calculate distance to pareto front for one point)")
    # """

    """ LEXSORT
    test_lexsort(n_dim=3)
    plot_performance(plot_function="lexsort_3D", poly_degree=1)

    test_lexsort(n_dim=4)
    plot_performance(plot_function="lexsort_4D", poly_degree=1)
    # """

    """ CONTRIBUTING HYPERVOLUME
    test_contributing_hypervolume(n_dim=3)
    plot_performance(plot_function="contributing_hypervolume_3D",
                     title="(time to calculate contributing hv for one point from archive)")

    test_contributing_hypervolume(n_dim=4, pop_size=100, n_gen=10, time_limit=10)
    plot_performance(plot_function="contributing_hypervolume_4D",
                     title="(time to calculate contributing hv for one point from archive)")
    # """

    """ HYPERVOLUME IMPROVEMENT
    test_hypervolume_improvement(n_gen=20, pop_size=1000, time_limit=10)
    plot_performance(plot_function="hypervolume_improvement_3D",
                     title="(time to calculate hypervolume improvement for one point not in archive)")

    test_hypervolume_improvement(n_gen=20, pop_size=100, time_limit=10, n_dim=4)
    plot_performance(plot_function="hypervolume_improvement_4D",
                     title="(time to calculate hypervolume improvement for one point not in archive)")

    # """
