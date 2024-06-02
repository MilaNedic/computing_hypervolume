# Incrementally Computing the Hypervolume of a Set of n-D Points for n=3 and 4
This repository contains the description and corresponding files for the "Incrementally computing the hypervolume of a set of n-D points for n=3 and 4" project.

This is a project for the master's subject "Matematika z računalnikom" at University of Ljubljana, Faculty of Mathematics and Physics. 

## Description
The hypervolume of a set of n-D points is often used in multi-objective optimization and serves as a measure of tracking the progress of optimization algorithms.

The goal of this project is to transfer the most computationally efficient implementation of the incremental hypervolume computation for 3-D and 4-D spaces, which is written in C, into Python.

## Repository Structure
The repository is structured as follows:
- The *moarchiving* folder consists of my implementation of the hypervolume problem in three and four dimensions in Python.
  - The `hv_plus.py` contains all the auxiliary funtions as well as the main functions for computing the hypervolume in both three and four dimensions.
  - Example tests for the auxiliary functions are written in the `hv_plus_tests.py` file, which can be run by simply downloading both files into the same folder and then running the `hv_plus_tests.py` file.
  - Additional tests for the hyperovlume in four dimensions are available in `hv4d_test.py` and are executed by running the file.
  - An example test for the three dimensional case, which can be found at [https://github.com/apguerreiro/HVC], is implemented in `hv3d_test_original.py`. After running this Python file, the computed hypervolume is printed in the terminal (and equals to the original result from C). A visual representation for this example can be found in the *visualization* folder (one can either run the `hv3d_example_original.m` script or simply open the MATLAB figure `hv3d_example_original.fig`).
  - Additional three dimensional examples are available in `hv3d_test_01.py`, `hv3d_test_02.py`, ..., `hv3d_test_10.py`. A visual representation of `hv3d_test_01.py` is available in the *visualization* folder (by opening either `hv3d_example_01.m` or `hv3d_example_01.fig`).
  - Tests for time-efficiency for the three and four dimensional case are available in `hv3d_test_time.py` (for *hv3dplus*) and `hv4d_test_time_R.py` (for *hv4dplus-R*)/`hv4d_test_time_U.py`(for *hv4dplus-U*), respectively. Plots are saved in the *plots* subfolder. Test files are generated using `generate_points.py` and are saved in the *tests* subfolder.
- The *related* folder is a copy of the `HVC` repository, available at [https://github.com/apguerreiro/HVC]. Here, the original implementation is available as well as example cases (additional examples have been aded to the examples folder). The code has been slightly modified for testing purposes and comparing my Python implementation to the original one.
- The final report for the project can be found in the *final_report* folder (the project has not been yet completed at the time of wiritng the final report).

## Requirements
- Python (version 3.12.0 has been used) with the following libraries: numpy, sortedcontainers and functools.
- C (for testing/comparison purposes only).
