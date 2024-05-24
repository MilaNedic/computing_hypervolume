# Incrementally Computing the Hypervolume of a Set of n-D Points for n=3 and 4
This repository contains the description and corresponding files for the " Incrementally computing the hypervolume of a set of n-D points for n=3 and 4" project.

This is a project for the master's subject "Matematika z računalnikom" at University of Ljubljana, Faculty of Mathematics and Physics. 

## Description
The hypervolume of a set of n-D points is often used in multi-objective optimization and serves as a measure of tracking the progress of optimization algorithms.

The goal of this project is to transfer the most computationally efficient implementation of the incremental hypervolume computation for 3-D and 4-D spaces, which is written in C, into Python.

## Repository Structure
The repository is structured as follows:
- The *moarchiving* folder consists of my implementation of the hypervolume problem in three and four dimensions in Python. The `hv_plus.py` contains all the auxiliary funtions as well as the main functions for computing the hypervolume in both three and four dimensions. Example tests for the auxiliary functions are written in the `hv_plus_tests.py` file, which can be run by simply downloading both files into the same folder and then running the `hv_plus_tests.py` file. Additional tests for the hyperovlume in four dimensions are available in `hv4d_test.py` and are executed by running the file. A test of time-efficieny is available in `hv4d_test_time.py`. An example test for the three dimensional case, which can be found at [https://github.com/apguerreiro/HVC], is implemented in `hv3d_test.py`. After running this Python file, the computed hypervolume is printed in the terminal (and equals to the original result from C). A visual representation for this example can be found in the *visualization* folder (one can either run the `hv3d_example_original.m` script or simply open the MATLAB figure `hv3d_example_original.fig`).
- The *related* folder is a copy of the `HVC` repository, available at [https://github.com/apguerreiro/HVC]. Here, the original implementation is available as well as example cases. The code has been slightly modified for testing purposes and comparing my Python implementation to the original one.
- The final report for the project can be found in the *final_report* folder.
- Visual examples for the three dimentional data can be found in the *visualization* folder. It contains MATLAB scripts and corresponding figures of points in 3-D.  
